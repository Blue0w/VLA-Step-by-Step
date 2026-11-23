"""Render the LIBERO cup scene before and after applying a control command."""

import argparse
from contextlib import closing
from pathlib import Path

import numpy as np
from PIL import Image

from vla_step.environment import CUP_TASKS, CupEnvironment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=CUP_TASKS, default="left", help="Target plate for the red mug.")
    parser.add_argument("--image-size", type=int, default=256, help="Camera image width and height in pixels.")
    parser.add_argument("--steps", type=int, default=1, help="Repeat the action for this many steps.")
    parser.add_argument(
        "--action", nargs=7, type=float, default=[0.25, 0, 0, 0, 0, 0, -1],
        metavar=("DX", "DY", "DZ", "RX", "RY", "RZ", "GRIPPER"),
        help="Seven control values in [-1, 1].",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter01"))
    args = parser.parse_args()
    if args.image_size < 1 or args.steps < 1:
        parser.error("--image-size and --steps must be positive.")
    if not all(-1 <= value <= 1 for value in args.action):
        parser.error("--action values must be in [-1, 1].")

    # 前三项控制末端平移，接着三项控制朝向，最后一项控制夹爪。
    action = np.array(args.action, dtype=np.float32)
    with closing(CupEnvironment(side=args.side, image_size=args.image_size)) as env:
        before = env.reset()  # 回到初始场景，并读取第一帧画面和机械臂状态。
        # 每次 step 发送同一条动作。仿真结束时，保留最后一次观测。
        for step in range(1, args.steps + 1):
            after, _, done, _ = env.step(action)
            if done:
                break

        print(f"Task: {env.instruction}")
        print(f"Camera image (height, width, channels): {before.rgb.shape}")
        print(f"Gripper joint positions: {before.gripper_position}")
        print(f"Action: {action}")
        print(f"Steps executed: {step}")
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
