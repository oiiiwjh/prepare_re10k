import cv2

video_path = '/home/wjh/prepare_re10k/test_clips/tMjzRi1k4V8/83ceef672f798063.mp4'
# 读取总帧数
cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'Total frames: {total_frames}')

npy_path = '/home/wjh/prepare_re10k/test_pose_npy/83ceef672f798063.npy'
import numpy as np
pose_data = np.load(npy_path)
print(f'Pose data shape: {pose_data.shape}')  # 打印姿态数据