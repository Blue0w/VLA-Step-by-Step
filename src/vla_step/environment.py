"""The LIBERO cup scene and the observations used by the tutorial."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np


CUP_TASKS = {
    "left": "LIVING_ROOM_SCENE5_put_the_red_mug_on_the_left_plate",
    "right": "LIVING_ROOM_SCENE5_put_the_red_mug_on_the_right_plate",
}


@dataclass
class Observation:
    rgb: np.ndarray
    eef_position: np.ndarray
    eef_quaternion: np.ndarray
    gripper_position: np.ndarray
    joint_position: np.ndarray


class CupEnvironment:
    """Load a LIBERO-90 cup task without loading demonstration data."""

    def __init__(
        self, side: str = "left", image_size: int = 256, seed: int = 0, *,
        controller: str = "OSC_POSE",
    ):
        from libero.libero import get_libero_path
        from libero.libero.envs import OffScreenRenderEnv
        from robosuite.macros import IMAGE_CONVENTION

        task_file = (
            Path(get_libero_path("bddl_files")) / "libero_90" / f"{CUP_TASKS[side]}.bddl"
        )
        self._env = OffScreenRenderEnv(
            bddl_file_name=str(task_file),
            controller=controller,
            camera_names=["agentview"],
            camera_heights=image_size,
            camera_widths=image_size,
            hard_reset=False,
        )
        self._env.seed(seed)
        self.instruction = self._env.language_instruction
        self._flip_image = IMAGE_CONVENTION == "opengl"

    def _observation(self, raw: dict) -> Observation:
        rgb = raw["agentview_image"]
        if self._flip_image:
            rgb = rgb[::-1]
        return Observation(
            rgb=rgb.copy(),
            eef_position=raw["robot0_eef_pos"].copy(),
            eef_quaternion=raw["robot0_eef_quat"].copy(),
            gripper_position=raw["robot0_gripper_qpos"].copy(),
            joint_position=raw["robot0_joint_pos"].copy(),
        )

    def reset(self, initial_state: np.ndarray | None = None) -> Observation:
        raw = self._env.reset()
        if initial_state is not None:
            raw = self._env.set_init_state(initial_state)
        return self._observation(raw)

    def get_sim_state(self) -> np.ndarray:
        return self._env.get_sim_state().copy()

    def step(self, action: np.ndarray) -> tuple[Observation, float, bool, dict]:
        raw, reward, done, info = self._env.step(action)
        return self._observation(raw), reward, done, info

    def close(self) -> None:
        self._env.close()
