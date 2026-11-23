"""Render the LIBERO cup scene before and after one control step."""

import argparse
from contextlib import closing
from pathlib import Path

import numpy as np
from PIL import Image

from vla_step.environment import CUP_TASKS, CupEnvironment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=CUP_TASKS, default="left")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter01"))
    args = parser.parse_args()

    with closing(CupEnvironment(side=args.side)) as env:
        before = env.reset()
        # LIBERO uses XYZ, rotation, and gripper commands. Chapter 02 explains the units.
        action = np.array([0.25, 0, 0, 0, 0, 0, -1], dtype=np.float32)
        after, _, _, _ = env.step(action)

        print(f"Task: {env.instruction}")
        print(f"Camera image (height, width, channels): {before.rgb.shape}")
        print(f"Gripper joint positions: {before.gripper_position}")
        print(f"Action: {action}")
        print(f"End-effector position before (m): {before.eef_position}")
        print(f"End-effector position after  (m): {after.eef_position}")
        print(f"Measured displacement (m): {after.eef_position - before.eef_position}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, observation in [("before.png", before), ("after.png", after)]:
        path = args.output_dir / filename
        Image.fromarray(observation.rgb).save(path)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
