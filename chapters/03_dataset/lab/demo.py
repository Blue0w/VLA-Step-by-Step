"""Inspect a recorded red-mug episode and turn it into training samples."""

import argparse
from pathlib import Path

import h5py
import matplotlib
import numpy as np

from vla_step.dataset import ACTION_NAMES, action_statistics, make_sample, read_image, split_episodes

matplotlib.use("Agg")
from matplotlib import pyplot as plt


SAMPLE_FILE = Path(__file__).resolve().parents[1] / "media/libero90-red-mug-left-sample.hdf5"


def show_field(name: str, item: h5py.Group | h5py.Dataset) -> None:
    if isinstance(item, h5py.Dataset):
        print(f"  {name:<24} {str(item.shape):<20} {item.dtype}")


def plot_episode(demo: h5py.Group, t: int, output: Path) -> None:
    figure = plt.figure(figsize=(10, 8), layout="constrained")
    grid = figure.add_gridspec(4, 3, height_ratios=(2, 1, 1, 1))
    for column, (index, label) in enumerate((
        (0, "Start"),
        (t - 1, "Selected observation"),
        (len(demo["actions"]) - 1, "End"),
    )):
        axis = figure.add_subplot(grid[0, column])
        axis.imshow(read_image(demo, index))
        axis.set_title(f"{label} (obs {index})")
        axis.set_axis_off()

    # Group the seven curves by purpose and mark the action chosen in the parameter cell.
    actions = demo["actions"][()]
    for row, components in enumerate((range(3), range(3, 6), range(6, 7)), start=1):
        axis = figure.add_subplot(grid[row, :])
        for component in components:
            axis.plot(actions[:, component], label=ACTION_NAMES[component])
        axis.axvline(t, color="black", linestyle="--", linewidth=1)
        axis.legend(loc="upper right", ncol=len(components))
    axis.set_xlabel("Action index")

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=130)
    plt.close(figure)


def show_training_preview(data: h5py.Group, demo_ids: list[str], horizon: int) -> None:
    if len(demo_ids) < 2:
        print("\nUse at least two episodes to see the train/validation split.")
        return
    train, validation = split_episodes(demo_ids)
    mean, scale = action_statistics(data, train)
    first_demo, second_demo = data[train[0]], data[train[-1]]
    first = make_sample(first_demo, 1, horizon)
    second = make_sample(second_demo, min(2, len(second_demo["actions"]) - 1), horizon)
    images = np.stack([first.image, second.image])
    states = np.stack([first.state, second.state])
    actions = np.stack([first.actions, second.actions])
    masks = np.stack([first.action_mask, second.action_mask])
    instructions = [first.instruction, second.instruction]

    print(f"\nTrain episodes: {train}\nValidation episodes: {validation}")
    print(f"Batch: image {images.shape}, state {states.shape}, instructions {len(instructions)}, "
          f"actions {actions.shape}, mask {masks.shape}")
    # Normalize one genuine action using the training episodes, then recover it.
    original = actions[0, 0]
    normalized = (original - mean) / scale
    recovered = normalized * scale + mean
    print("One action:", original)
    print("Normalized:", normalized)
    print("Recovered:", recovered)
    print(f"Max round-trip error: {np.max(np.abs(original - recovered)):.2e}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=SAMPLE_FILE)
    parser.add_argument("--demo-id", default="demo_0")
    parser.add_argument("--t", type=int, help="Action index. Negative indices count from the end.")
    parser.add_argument("--horizon", type=int, default=1, help="Number of actions per sample (K).")
    parser.add_argument("--output", type=Path, default=Path("outputs/chapter03/trajectory.png"))
    args = parser.parse_args()

    np.set_printoptions(precision=4, suppress=True)
    with h5py.File(args.data, "r") as file:
        data = file["data"]
        demo_ids = sorted(data.keys(), key=lambda key: int(key.split("_")[-1]))
        if args.demo_id not in demo_ids:
            parser.error(f"Choose --demo-id from: {', '.join(demo_ids)}.")
        demo = data[args.demo_id]
        total = len(demo["actions"])
        t = total // 2 if args.t is None else args.t
        if t < 0:
            t += total
        try:
            sample = make_sample(demo, t, args.horizon)
        except ValueError as error:
            parser.error(str(error))

        print(f"File: {args.data.name} · Episodes: {len(demo_ids)}")
        print(f"/data/{args.demo_id} · {total} recorded steps")
        demo.visititems(show_field)
        print(f"\nInstruction: {sample.instruction}")
        print(f"Observation obs[{t - 1}] → action index {t}")
        print(f"Image shape: {sample.image.shape}")
        print(f"State (position, orientation, two finger positions) {sample.state.shape}: {sample.state}")
        print(f"Observed joint angles (rad): {demo['obs/joint_states'][t - 1]}")
        print(f"Action columns: {', '.join(ACTION_NAMES)}")
        print(f"Action block {sample.actions.shape}:\n{sample.actions}")
        print(f"Action mask: {sample.action_mask.tolist()}")
        plot_episode(demo, t, args.output)
        print(f"Saved: {args.output}")
        show_training_preview(data, demo_ids, args.horizon)


if __name__ == "__main__":
    main()
