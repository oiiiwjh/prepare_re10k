import argparse
import json
import os
import os.path as osp
from tqdm import tqdm
import csv
import numpy as np


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
    # save_csv
    parser.add_argument('--save_csv', default='output.json')
    # pose_npy_folder
    parser.add_argument('--pose_npy_folder', default='pose_npy_files')
    parser.add_argument('--delimiter', default=',', help='CSV delimiter')
    return parser.parse_args()



class Camera(object):
    def __init__(self, entry):
        fx, fy, cx, cy = entry[1:5]
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        w2c_mat = np.array(entry[7:]).reshape(3, 4)
        w2c_mat_4x4 = np.eye(4)
        w2c_mat_4x4[:3, :] = w2c_mat
        self.w2c_mat = w2c_mat_4x4
        self.c2w_mat = np.linalg.inv(w2c_mat_4x4)


def transfer_pose_format(pose_file, pose_npy_file):
    with open(pose_file, 'r') as f:
        poses = f.readlines()
    poses = [pose.strip().split(' ') for pose in poses[1:]]
    cam_params = [[float(x) for x in pose] for pose in poses]
    cam_params = [Camera(cam_param) for cam_param in cam_params]
    # choose what you want!
    # cam_w2c = [cam.w2c_mat for cam in cam_params]
    cam_c2w = [cam.c2w_mat for cam in cam_params]
    cam_c2w = np.array(cam_c2w)
    np.save(pose_npy_file, cam_c2w)
    
if __name__ == '__main__':
    args = get_args()
    # os.makedirs(args.save_csv, exist_ok=True)
    # save_root = args.root_path
    captions = json.load(open(args.caption_path, 'r'))
    captions = {k: v[0] for k, v in captions.items()}
    all_results = []
    
    clips_info = json.load(open(args.clips_info, 'r'))
    i = 0
    for video, clips in clips_info.items():
        for clip_name in clips:
            
            # print(f'Processing clip: {clip_name}')
            # clip_name = clip['clip_name']
            print(f"{clip_name}.mp4")
            caption = captions.get(f"{clip_name}.mp4", "")
            pose_file = osp.join(args.pose_folder, clip_name + '.txt')
            pose_npy_file = osp.join(args.pose_npy_folder, clip_name + '.npy')
            os.makedirs(osp.dirname(pose_npy_file), exist_ok=True)
            if i < 10:
                transfer_pose_format(pose_file, pose_npy_file)
            i += 1
            clip_path = osp.realpath(osp.join(osp.expanduser(args.clips_folder), video, clip_name + '.mp4'))
            all_results.append({
                "src_video": video,
                "clip_name": clip_name,
                "clip_path": clip_path,
                "pose_file": pose_file,
                "pose_npy_file": pose_npy_file,
                "caption": caption
            })
    print(f'There are {len(all_results)} clips after the processing')
    # write CSV with columns: clip_name, clip_path, pose_file, caption
    with open(args.save_csv, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=args.delimiter)
        writer.writerow(['src_video', 'clip_name', 'clip_path', 'pose_file', 'pose_npy_file', 'caption'])
        for item in all_results:
            writer.writerow([item.get('clip_name',''), item.get('clip_path',''), item.get('pose_file',''), item.get('pose_npy_file',''), item.get('caption','')])
    print(f'Saved the generated csv file to {args.save_csv}')
    