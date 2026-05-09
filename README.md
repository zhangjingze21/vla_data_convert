# vla_data_convert

This repo is a lightweight package for converting Unitree JSON dataset dumps into LeRobot format.

## Included files

- `run.sh`
- `unitree_lerobot/utils/sort_and_rename_folders.py`
- `unitree_lerobot/utils/convert_unitree_json_to_lerobot.py`
- `unitree_lerobot/utils/constants.py`

Other folders/files in this checkout are not required for this conversion flow.

## Quick start

`run.sh` is a template file with placeholders:

```bash
source <path_to_conda_profile>/anaconda3/etc/profile.d/conda.sh
conda activate <conda_env>

python <path_to_repo>/unitree_lerobot/utils/sort_and_rename_folders.py --data_dir <path_to_data>/data/
python <path_to_repo>/unitree_lerobot/utils/convert_unitree_json_to_lerobot.py --raw-dir <path_to_data>/ --repo-id <repo_id> --robot_type <robot_type>
cp -r "<path_to_hf_home>/unitree_lerobot/"* <path_to_output>
```

## Placeholder meanings

- `<path_to_conda_profile>`: root of conda installation (for example `/home/user/anaconda3`)
- `<conda_env>`: conda env name (for example `humanoidvla`)
- `<path_to_repo>`: repo absolute path
- `<path_to_data>`: raw data root containing a `data/` directory
- `<repo_id>`: target HF repo id
- `<robot_type>`: one of `Unitree_G1_Inspire_wholebody`, `Unitree_G1_Dex3`, etc.
- `<path_to_hf_home>`: huggingface lerobot cache root (for example `/home/user/.cache/huggingface/lerobot`)
- `<path_to_output>`: final output directory

## What this repo is not

This repo is intended for conversion only in this workflow. H5 converters, robot replay/inference tools, and visualizers are intentionally excluded from the required path.

## Recommended workflow

1. Fill all placeholders in `run.sh`.
2. Run `bash run.sh`.
3. Resulting converted data appears in `<path_to_output>`.
