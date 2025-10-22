adapted from
- https://github.com/hehao13/CameraCtrl?tab=readme-ov-file#prepare-camera-trajectory--prompts
- https://github.com/hehao13/CameraCtrl?tab=readme-ov-file#dataset

## Data download (HuggingFace)
https://huggingface.co/datasets/JiaHWang/re10k

The dataset includes:
- video_highquality_train
- video_highquality_test
- test_captions.json / train_captions.json
- test_poses.zip / train_poses.zip

Unzip videos into the corresponding folders. For poses, for example:

unzip test_poses.zip -d ./test_poses
unzip train_poses.zip -d ./train_poses

Extracted videos/clips are expected to be 25 Hz.

## Prepare RE10K dataset (recommended workflow)
This folder contains helper scripts and an example `run.sh` that demonstrates the full preprocessing pipeline. The high-level steps are:

1. Unzip video and pose archives (the example script will skip already-extracted files).
2. Gather pose files into a clips-info JSON using `gather_realestate.py`.
3. Extract clips (frames -> mp4) using `get_realestate_clips.py`.
4. Generate a metadata CSV (one row per clip) using `generate_realestate_csv.py`.

The included `run.sh` sets example variables and runs the pipeline. Update the top of `run.sh` and then run it, or run the commands below manually.

Example (manual) commands — replace paths to match your environment:

base_dir=/path/to/re10k_hf
tag=test # or 'train'

python gather_realestate.py \
	--pose_folder ${base_dir}/${tag}_pose \
	--save_path ${tag}_pose.json

python get_realestate_clips.py \
	--video_root ${base_dir}/video_highquality_${tag} \
	--save_path /path/to/output_clips \
	--video2clip_json ${tag}_pose.json \
	--clip_txt_path ${base_dir}/${tag}_pose \
	--num_workers 16

python generate_realestate_csv.py \
	--clips_folder /path/to/output_clips \
	--caption_path ${base_dir}/${tag}_captions.json \
	--pose_folder ${base_dir}/${tag}_pose \
	--clips_info ${tag}_pose.json \
	--save_csv /path/to/${tag}_metadata.csv

Notes and tips:
- `--num_workers` controls parallelism for clip extraction. Increase to speed up on multi-core machines, but watch memory and disk I/O: each worker opens a separate video handle and stores frames in memory briefly.
- `generate_realestate_csv.py` writes a CSV file. The CSV columns (in order) are: `clip_name`, `clip_path`, `pose_file`, `caption`.
- If you prefer using the helper script, edit `run.sh` variables (`base_dir`, `tgt_dir`, `tag`) and run:

bash run.sh

