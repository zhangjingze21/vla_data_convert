"""
Script Json to Lerobot.

# --raw-dir     Corresponds to the directory of your JSON dataset
# --repo-id     Your unique repo ID on Hugging Face Hub
# --robot_type  The type of the robot used in the dataset (e.g., Unitree_Z1_Single, Unitree_Z1_Dual, Unitree_G1_Dex1, Unitree_G1_Dex3, Unitree_G1_Brainco, Unitree_G1_Inspire)
# --push_to_hub Whether or not to upload the dataset to Hugging Face Hub (true or false)

python unitree_lerobot/utils/convert_unitree_json_to_lerobot.py \
    --raw-dir $HOME/datasets/g1_grabcube_double_hand \
    --repo-id your_name/g1_grabcube_double_hand \
    --robot_type Unitree_G1_Dex3 \
    --push_to_hub
"""

import os
import cv2
import tqdm
import tyro
import json
import glob
import dataclasses
import shutil
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Literal

from lerobot.constants import HF_LEROBOT_HOME
from lerobot.datasets.lerobot_dataset import LeRobotDataset

from unitree_lerobot.utils.constants import ROBOT_CONFIGS


@dataclasses.dataclass(frozen=True)
class DatasetConfig:
    use_videos: bool = True
    tolerance_s: float = 0.0001
    image_writer_processes: int = 10
    image_writer_threads: int = 5
    video_backend: str | None = None


DEFAULT_DATASET_CONFIG = DatasetConfig()


class JsonDataset:
    def __init__(self, data_dirs: Path, robot_type: str) -> None:
        """
        Initialize the dataset for loading and processing HDF5 files containing robot manipulation data.

        Args:
            data_dirs: Path to directory containing training data
        """
        assert data_dirs is not None, "Data directory cannot be None"
        assert robot_type is not None, "Robot type cannot be None"
        self.data_dirs = data_dirs
        self.robot_type = robot_type
        self.json_file = "data.json"

        # Initialize paths and cache
        self._init_paths()
        self._init_cache()
        self.json_state_data_name = ROBOT_CONFIGS[robot_type].json_state_data_name
        self.json_action_data_name = ROBOT_CONFIGS[robot_type].json_action_data_name
        self.camera_to_image_key = ROBOT_CONFIGS[robot_type].camera_to_image_key

    def _init_paths(self) -> None:
        """Initialize episode and task paths."""

        self.episode_paths = []
        self.task_paths = []

        for task_path in glob.glob(os.path.join(self.data_dirs, "*")):
            if os.path.isdir(task_path):
                episode_paths = glob.glob(os.path.join(task_path, "*"))
                if episode_paths:
                    self.task_paths.append(task_path)
                    self.episode_paths.extend(episode_paths)

        self.episode_paths = sorted(self.episode_paths)
        self.episode_ids = list(range(len(self.episode_paths)))

    def __len__(self) -> int:
        """Return the number of episodes in the dataset."""
        return len(self.episode_paths)

    def _init_cache(self) -> list:
        """Initialize data cache if enabled."""

        self.episodes_data_cached = []
        valid_episode_paths = []
        for episode_path in tqdm.tqdm(self.episode_paths, desc="Loading Cache Json"):
            json_path = os.path.join(episode_path, self.json_file)
            try:
                with open(json_path, encoding="utf-8") as jsonf:
                    data = json.load(jsonf)
                    self.episodes_data_cached.append(data)
                    valid_episode_paths.append(episode_path)
            except json.JSONDecodeError:
                print(f"Warning: Skipping corrupted JSON file: {json_path}")
            except Exception as e:
                print(f"Warning: Error reading {json_path}: {e}")
        
        # Update episode_paths to only include valid ones
        self.episode_paths = valid_episode_paths
        self.episode_ids = list(range(len(self.episode_paths)))

        print(f"==> Cached {len(self.episodes_data_cached)} episodes")

        return self.episodes_data_cached

    def _append_pelvis_xyz_delta(self, action: np.ndarray) -> np.ndarray:
        """Append pelvis xyz delta relative to the first frame for whole-body G1 data."""
        if self.robot_type != "Unitree_G1_Inspire_wholebody" or len(action) == 0:
            return action

        pelvis_xyz = action[:, 7:10]
        pelvis_xyz_delta = pelvis_xyz - pelvis_xyz[0:1]
        return np.concatenate([action, pelvis_xyz_delta.astype(np.float32)], axis=1)

    def _parse_indexing(self, key_part: str) -> tuple[str, list]:
        """
        Parse a key with indexing/slicing like 'mocap_body_pos[0][0]' or 'mocap_root_lin_vel[0][:2]'
        
        Returns:
            tuple: (base_key, list of indices/slices)
        """
        import re
        # Extract the base key and all indexing operations
        match = re.match(r'([^\[]+)((?:\[[^\]]+\])*)', key_part)
        if not match:
            return key_part, []
        
        base_key = match.group(1)
        indexing_str = match.group(2)
        
        if not indexing_str:
            return base_key, []
        
        # Parse all [xxx] operations
        indices = []
        for idx_match in re.finditer(r'\[([^\]]+)\]', indexing_str):
            idx_str = idx_match.group(1)
            if ':' in idx_str:
                # It's a slice
                parts = idx_str.split(':')
                start = int(parts[0]) if parts[0] else None
                stop = int(parts[1]) if len(parts) > 1 and parts[1] else None
                indices.append(slice(start, stop))
            else:
                # It's an index
                indices.append(int(idx_str))
        
        return base_key, indices

    def _extract_data(self, episode_data: dict, key: str, parts: list[str]) -> np.ndarray:
        """
        Extract data from episode dictionary for specified parts.

        Args:
            episode_data: Dictionary containing episode data
            key: Data key to extract ('states' or 'actions')
            parts: List of parts to include ('left_arm', 'right_arm')

        Returns:
            Concatenated numpy array of the requested data
        """
        # import ipdb; ipdb.set_trace()
        result = []
        # Keys that should be retrieved from the previous action when extracting state
        # prev_action_keys = {"left_hand.qpos", "right_hand.qpos", "head_servo.qpos"}

        for i, sample_data in enumerate(episode_data["data"]):
            data_array = np.array([], dtype=np.float32)
            for part in parts:
                
                # Determine source sample and key
                current_sample_data = sample_data
                current_key = key

                # Check if we need to retrieve from previous action
                # if key == "states" and part in prev_action_keys:
                #     # Use previous frame's action (or current if first frame)
                #     idx = max(0, i - 1)
                #     current_sample_data = episode_data["data"][idx]
                #     current_key = "actions"

                key_parts = part.split(".")
                qpos = None
                
                for part_idx, key_part in enumerate(key_parts):
                    # Parse the key and any indexing/slicing operations
                    base_key, indices = self._parse_indexing(key_part)

                    if qpos is None:
                        # For the first key_part, search in multiple locations
                        if current_key in current_sample_data and base_key in current_sample_data[current_key] and current_sample_data[current_key][base_key] is not None:
                            # First try: in current_sample_data[current_key]
                            qpos = current_sample_data[current_key][base_key]
                        elif base_key in current_sample_data and current_sample_data[base_key] is not None:
                            # Second try: directly in current_sample_data
                            qpos = current_sample_data[base_key]
                        else:
                            # Fallback: check in 'states' or 'actions' explicitly
                            found = False
                            # Prioritize current_key, then the other
                            fallback_keys = [current_key] + [k for k in ['states', 'actions'] if k != current_key]
                            
                            for other_key in fallback_keys:
                                if other_key in current_sample_data and base_key in current_sample_data[other_key] and current_sample_data[other_key][base_key] is not None:
                                    qpos = current_sample_data[other_key][base_key]
                                    found = True
                                    break
                            if not found:
                                raise ValueError(f"Cannot find '{base_key}' for part: {part} in sample_data")
                    else:
                        # For subsequent key_parts, navigate within the current qpos
                        if isinstance(qpos, dict) and base_key in qpos:
                            qpos = qpos[base_key]
                        else:
                            raise ValueError(f"Cannot navigate to '{base_key}' in part: {part}")

                    # Apply all indexing/slicing operations in order
                    for idx_or_slice in indices:
                        if isinstance(qpos, (list, dict)):
                            qpos = np.array(qpos) if isinstance(qpos, list) else qpos
                        
                        if isinstance(idx_or_slice, slice):
                            # Apply slice
                            qpos = np.array(qpos)[idx_or_slice]
                        else:
                            # Apply index
                            qpos = qpos[idx_or_slice]

                if qpos is None:
                    raise ValueError(f"qpos is None for part: {part}")
                
                # Convert to flat numpy array
                if isinstance(qpos, list):
                    qpos = np.array(qpos, dtype=np.float32).flatten()
                elif isinstance(qpos, np.ndarray):
                    qpos = qpos.astype(np.float32).flatten()
                else:
                    qpos = np.array([qpos], dtype=np.float32).flatten()
                    
                data_array = np.concatenate([data_array, qpos])
            result.append(data_array)
        return np.array(result)

    def _parse_images(self, episode_path: str, episode_data) -> dict[str, list[np.ndarray]]:
        """Load and stack images for a given camera key. Implements Frame Interpolation (Forward Fill)."""

        images = defaultdict(list)

        keys = episode_data["data"][0]["colors"].keys()
        cameras = [key for key in keys if "depth" not in key]

        for camera in cameras:
            image_key = self.camera_to_image_key.get(camera)
            if image_key is None:
                continue

            last_valid_img = None
            
            for sample_data in episode_data["data"]:
                relative_path = sample_data["colors"].get(camera)
                current_img = None

                if relative_path:
                    image_path = os.path.join(episode_path, relative_path)
                    if os.path.exists(image_path):
                        loaded_img = cv2.imread(image_path)
                        if loaded_img is not None:
                            current_img = cv2.cvtColor(loaded_img, cv2.COLOR_BGR2RGB)

                if current_img is not None:
                    # We found a valid image
                    last_valid_img = current_img
                    images[image_key].append(current_img)
                elif last_valid_img is not None:
                    # Missing image: COPY previous valid image (Forward Fill)
                    # This keeps video length consistent but image static for this frame
                    images[image_key].append(last_valid_img)
                else:
                    # Missing start of episode: Append None for now, fill later
                    images[image_key].append(None)
            
            # Post-processing: Handle missing frames at the start (Backward Fill)
            # Use 'any' with identity check to avoid numpy array equality ambiguity
            if any(img is None for img in images[image_key]):
                first_valid_idx = -1
                for i, img in enumerate(images[image_key]):
                    if img is not None:
                        first_valid_idx = i
                        break
                
                if first_valid_idx > 0:
                    # Fill start gaps with the first valid image found
                    first_img = images[image_key][first_valid_idx]
                    for i in range(first_valid_idx):
                        images[image_key][i] = first_img
                elif first_valid_idx == -1:
                    print(f"Warning: No valid images found for camera {camera} in {episode_path}")
                    # If absolutely no images, we might need to populate with zeros or skip
                    # For now, let's fill with black images to prevent crash, assuming 640x480
                    pad_img = np.zeros((480, 640, 3), dtype=np.uint8)
                    images[image_key] = [pad_img] * len(episode_data["data"])

        return images

    def get_item(
        self,
        index: int | None = None,
    ) -> dict:
        """Get a training sample from the dataset."""

        file_path = np.random.choice(self.episode_paths) if index is None else self.episode_paths[index]
        episode_data = self.episodes_data_cached[index]

        # Load state and action data
        action = self._extract_data(episode_data, "actions", self.json_action_data_name)
        action = self._append_pelvis_xyz_delta(action)
        state = self._extract_data(episode_data, "states", self.json_state_data_name)
        episode_length = len(state)
        state_dim = state.shape[1] if len(state.shape) == 2 else state.shape[0]
        action_dim = action.shape[1] if len(action.shape) == 2 else state.shape[0]

        # Load task description
        task = episode_data.get("text", {}).get("goal", "")

        # Load camera images
        cameras = self._parse_images(file_path, episode_data)

        # Since we interpolated images, we trust state length and assume alignment
        # num_frames = len(state)
        # Any size mismatch should be handled (e.g. if json has more entries than image folder scan implies? 
        # But here parse_images loops over json data, so lengths should match 1:1)

        # Extract camera configuration
        cam_height, cam_width = next(img for imgs in cameras.values() if imgs for img in imgs if img is not None).shape[:2]
        data_cfg = {
            "camera_names": list(cameras.keys()),
            "cam_height": cam_height,
            "cam_width": cam_width,
            "state_dim": state_dim,
            "action_dim": action_dim,
        }

        return {
            "episode_index": index,
            "episode_length": episode_length,
            "state": state,
            "action": action,
            "cameras": cameras,
            "task": task,
            "data_cfg": data_cfg,
        }


def create_empty_dataset(
    repo_id: str,
    robot_type: str,
    mode: Literal["video", "image"] = "video",
    *,
    has_velocity: bool = False,
    has_effort: bool = False,
    dataset_config: DatasetConfig = DEFAULT_DATASET_CONFIG,
) -> LeRobotDataset:
    robot_config = ROBOT_CONFIGS[robot_type]
    motors = robot_config.motors
    cameras = robot_config.cameras
    # Use state_names if available, otherwise fall back to motors
    state_names = robot_config.state_names if robot_config.state_names is not None else motors

    features = {
        "observation.state": {
            "dtype": "float32",
            "shape": (len(state_names),),
            "names": [
                state_names,
            ],
        },
        "action": {
            "dtype": "float32",
            "shape": (len(motors),),
            "names": [
                motors,
            ],
        },
    }

    if has_velocity:
        features["observation.velocity"] = {
            "dtype": "float32",
            "shape": (len(motors),),
            "names": [
                motors,
            ],
        }

    if has_effort:
        features["observation.effort"] = {
            "dtype": "float32",
            "shape": (len(motors),),
            "names": [
                motors,
            ],
        }

    for cam in cameras:
        features[f"observation.images.{cam}"] = {
            "dtype": mode,
            "shape": (480, 640, 3),
            "names": [
                "height",
                "width",
                "channel",
            ],
        }

    if Path(HF_LEROBOT_HOME / repo_id).exists():
        shutil.rmtree(HF_LEROBOT_HOME / repo_id)

    return LeRobotDataset.create(
        repo_id=repo_id,
        fps=30,
        robot_type=robot_type,
        features=features,
        use_videos=dataset_config.use_videos,
        tolerance_s=dataset_config.tolerance_s,
        image_writer_processes=dataset_config.image_writer_processes,
        image_writer_threads=dataset_config.image_writer_threads,
        video_backend=dataset_config.video_backend,
    )


def populate_dataset(
    dataset: LeRobotDataset,
    raw_dir: Path,
    robot_type: str,
) -> LeRobotDataset:
    json_dataset = JsonDataset(raw_dir, robot_type)
    for i in tqdm.tqdm(range(len(json_dataset))):
        episode = json_dataset.get_item(i)

        state = episode["state"]
        action = episode["action"]
        cameras = episode["cameras"]
        # task = episode["task"]
        task = "pick up the green tomato and put to the basket"
        episode_length = episode["episode_length"]

        num_frames = episode_length
        for i in range(num_frames):
            frame = {
                "observation.state": state[i],
                "action": action[i],
            }

            for camera, img_array in cameras.items():
                frame[f"observation.images.{camera}"] = img_array[i]
            dataset.add_frame(frame, task=task)

        dataset.save_episode()

    return dataset


def json_to_lerobot(
    raw_dir: Path,
    repo_id: str,
    robot_type: str,  # e.g., Unitree_Z1_Single, Unitree_Z1_Dual, Unitree_G1_Dex1, Unitree_G1_Dex3, Unitree_G1_Brainco, Unitree_G1_Inspire
    *,
    push_to_hub: bool = False,
    mode: Literal["video", "image"] = "video",
    dataset_config: DatasetConfig = DEFAULT_DATASET_CONFIG,
):
    if (HF_LEROBOT_HOME / repo_id).exists():
        shutil.rmtree(HF_LEROBOT_HOME / repo_id)

    dataset = create_empty_dataset(
        repo_id,
        robot_type=robot_type,
        mode=mode,
        has_effort=False,
        has_velocity=False,
        dataset_config=dataset_config,
    )
    dataset = populate_dataset(
        dataset,
        raw_dir,
        robot_type=robot_type,
    )

    if push_to_hub:
        dataset.push_to_hub(upload_large_folder=True)


def local_push_to_hub(
    repo_id: str,
    root_path: Path,
):
    dataset = LeRobotDataset(repo_id=repo_id, root=root_path)
    dataset.push_to_hub(upload_large_folder=True)


if __name__ == "__main__":
    tyro.cli(json_to_lerobot)
