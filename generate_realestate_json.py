import argparse
import json
import os
import os.path as osp
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser()
    # clips_folder
    parser.add_argument('--clips_folder', default='video_clips')
    # caption_path
    parser.add_argument('--caption_path', default='captions/caption.json')
    # pose_folder
    parser.add_argument('--pose_folder', default='pose_files')
    # clips_info
    parser.add_argument('--clips_info', default='clips_info.json')
    # save_json
    parser.add_argument('--save_json', default='output.json')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    # os.makedirs(args.save_json, exist_ok=True)
    # save_root = args.root_path
    captions = json.load(open(args.caption_path, 'r'))
    captions = {k: v[0] for k, v in captions.items()}
    all_results = []
    
    clips_info = json.load(open(args.clips_info, 'r'))
    for video, clips in clips_info.items():
        for clip_name in clips:
            # print(f'Processing clip: {clip_name}')
            # clip_name = clip['clip_name']
            print(f"{clip_name}.mp4")
            caption = captions.get(f"{clip_name}.mp4", "")
            pose_file = osp.join(args.pose_folder, clip_name + '.txt')
            clip_path = osp.join(args.clips_folder, video, clip_name + '.mp4')
            all_results.append({
                "clip_name": clip_name,
                "clip_path": clip_path,
                "pose_file": pose_file,
                "caption": caption
            })
    print(f'There are {len(all_results)} clips after the processing')
    with open(args.save_json, 'w') as f:
        json.dump(all_results, fp=f)
    print(f'Saved the generated json file to {args.save_json}')
    
# run bash script:
# python prepare_re10k/get_realestate_clips.py \
#   --video_root /path/to/video_root \
#   --save_path /path/to/output_clips \
#   --video2clip_json /path/to/video2clip.json \
#   --clip_txt_path /path/to/clip_txts \
#   --pose
    
#   --num_workers 8