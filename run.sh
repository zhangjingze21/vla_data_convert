#!/bin/bash
source <path_to_conda_profile>/anaconda3/etc/profile.d/conda.sh
conda activate <conda_env>

python <path_to_repo>/unitree_lerobot/utils/sort_and_rename_folders.py --data_dir <path_to_data>/data/
python <path_to_repo>/unitree_lerobot/utils/convert_unitree_json_to_lerobot.py --raw-dir <path_to_data>/ --repo-id <repo_id> --robot_type <robot_type>
cp -r "<path_to_hf_home>/unitree_lerobot/"* <path_to_output>
