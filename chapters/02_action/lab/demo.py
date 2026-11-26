"""Compare joint-space and task-space control from the same simulated state."""

import argparse
from contextlib import closing
from pathlib import Path

import numpy as np
from PIL import Image

from vla_step.environment import CupEnvironment


def run_trial(
    controller: str,
    action: np.ndarray,
    steps: int,
    output_dir: Path,
    initial_state: np.ndarray | None = None,
) -> np.ndarray:
    with closing(CupEnvironment(controller=controller)) as env:
        before = env.reset(initial_state)
        starting_state = env.get_sim_state()
        for step in range(1, steps + 1):
            after, _, done, _ = env.step(action)
            if done:
                break

    # 关节角用度显示，末端位移用毫米显示，方便比较两个试验。
    joint_delta = np.degrees(after.joint_position - before.joint_position)
    eef_delta = (after.eef_position - before.eef_position) * 1000
    print(f"\n{controller} · action ({len(action)} values): {action} · steps: {step}")
    print("Joint changes (deg): " + "  ".join(
        f"J{number}={change:+.2f}" for number, change in enumerate(joint_delta, start=1)
    ))
    print("End-effector displacement (mm): " + "  ".join(
        f"{axis}={change:+.2f}" for axis, change in zip("XYZ", eef_delta)
    ))
    for label, observation in (("before", before), ("after", after)):
        Image.fromarray(observation.rgb).save(output_dir / f"{controller}-{label}.png")
    return starting_state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--joint", type=int, choices=range(1, 8), default=2)
    parser.add_argument("--joint-command", type=float, default=0.8)
    parser.add_argument("--z-command", type=float, default=0.8)
    parser.add_argument("--steps", type=int, default=15)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter02"))
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be positive.")
    if not all(-1 <= value <= 1 for value in (args.joint_command, args.z_command)):
        parser.error("--joint-command and --z-command must be in [-1, 1].")

    # 关节空间发送 7 个关节增量 + 1 个夹爪指令。
    joint_action = np.zeros(8, dtype=np.float32)
    joint_action[args.joint - 1] = args.joint_command
    joint_action[-1] = -1
    # 任务空间沿用第 01 章的格式，这里只改变第三项 dz。
    task_action = np.array([0, 0, args.z_command, 0, 0, 0, -1], dtype=np.float32)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    initial_state = run_trial("JOINT_POSITION", joint_action, args.steps, args.output_dir)
    run_trial("OSC_POSE", task_action, args.steps, args.output_dir, initial_state)


if __name__ == "__main__":
    main()
