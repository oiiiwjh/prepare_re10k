#!/bin/bash

tag=test # set to 'train' or 'test' accordingly

base_dir=/path/to/re10k_hf
tgt_dir=/path/to/processed_re10k_dir


video_folder=${base_dir}/video_highquality_${tag}
pose_folder=${base_dir}/${tag}_pose
caption_path=${base_dir}/${tag}_captions.json


pose_npy_folder=${tgt_dir}/${tag}_pose_npy
clips_folder=${tgt_dir}/${tag}_clips
pose_json=${tgt_dir}/${tag}_pose.json
save_csv=${tgt_dir}/${tag}_metadata.csv

# -----------------------------------------------------------------------------
echo "unzip video files if not done yet..."
for file in ${video_folder}/*.zip; do
    unzip -n "$file" -d ${video_folder}
done
echo "unzip pose.zip if not done yet..."
if [ ! -d "${pose_folder}" ]; then
    unzip -n ${base_dir}/${tag}_pose.zip -d ${pose_folder}
fi
# -----------------------------------------------------------------------------
echo "Gathering pose files..."
python gather_realestate.py --pose_folder ${pose_folder} \
    --save_path ${pose_json}
# -----------------------------------------------------------------------------
echo "Extracting video clips..."
python get_realestate_clips.py --video_root ${video_folder} \
    --save_path ${clips_folder} --video2clip_json ${pose_json} \
    --clip_txt_path ${pose_folder} \
    --num_workers 16
# -----------------------------------------------------------------------------
echo "Generating CSV file..."
python generate_realestate_csv.py --clips_folder ${clips_folder} \
    --caption_path ${caption_path} --pose_folder ${pose_folder} --pose_npy_folder ./npy \
    --clips_info ${pose_json} --save_csv ${save_csv}
