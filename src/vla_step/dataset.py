"""Read and slice the original LIBERO HDF5 demonstration format used in Chapter 03."""

from dataclasses import dataclass
import json

import h5py
import numpy as np


ACTION_NAMES = ("dx", "dy", "dz", "rx", "ry", "rz", "gripper")


@dataclass(frozen=True)
class Sample:
    image: np.ndarray
    state: np.ndarray
    instruction: str
    actions: np.ndarray
    action_mask: np.ndarray


def read_image(demo: h5py.Group, frame_index: int) -> np.ndarray:
    image = demo["obs/agentview_rgb"][frame_index]
    if demo.parent.attrs.get("macros_image_convention") == "opengl":
        image = image[::-1].copy()
    return image


def make_sample(demo: h5py.Group, t: int, horizon: int) -> Sample:
    """Pair the observation before action t with up to horizon consecutive actions."""
    actions = demo["actions"]
    if actions.ndim != 2 or actions.shape[1] != len(ACTION_NAMES):
        raise ValueError("Expected an action array with shape (T, 7).")
    if not 1 <= t < len(actions):
        raise ValueError(f"Choose an action index from 1 to {len(actions) - 1}.")
    if horizon < 1:
        raise ValueError("The action horizon must be positive.")

    # The original exporter writes obs[i] after applying actions[i].
    observation_index = t - 1
    observation = demo["obs"]
    state = np.concatenate([
        observation[key][observation_index]
        for key in ("ee_pos", "ee_ori", "gripper_states")
    ]).astype(np.float32)
    instruction = json.loads(demo.parent.attrs["problem_info"])["language_instruction"]

    # Repeat the final available action to keep a fixed shape. The mask marks real labels.
    real_actions = actions[t : t + horizon].astype(np.float32)
    real_count = len(real_actions)
    action_block = np.repeat(real_actions[-1:], horizon, axis=0)
    action_block[:real_count] = real_actions
    return Sample(
        image=read_image(demo, observation_index),
        state=state,
        instruction=instruction,
        actions=action_block,
        action_mask=np.arange(horizon) < real_count,
    )


def split_episodes(demo_ids: list[str], seed: int = 0) -> tuple[list[str], list[str]]:
    """Hold out whole episodes from one task file."""
    if len(demo_ids) < 2:
        raise ValueError("At least two episodes are needed for a train/validation split.")
    shuffled = np.random.default_rng(seed).permutation(sorted(demo_ids)).tolist()
    validation_count = max(1, len(demo_ids) // 5)
    return shuffled[validation_count:], shuffled[:validation_count]


def action_statistics(data: h5py.Group, train_ids: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Compute action normalization statistics from real training targets."""
    actions = np.concatenate([data[demo_id]["actions"][1:] for demo_id in train_ids])
    mean, scale = actions.mean(axis=0), actions.std(axis=0)
    scale[scale == 0] = 1
    mean[-1], scale[-1] = 0, 1  # Keep the gripper command on its original scale.
    return mean, scale
