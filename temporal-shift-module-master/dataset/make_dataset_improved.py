# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: make_dataset_improved.py
@time: 2020/12/08
"""
import os
import json
import numpy as np
from PIL import Image
import cv2
import shutil

img_size = (1920, 1080)
fps = 25

frames_root = '/nfs/volume-95-7/illegal_parking/dataset/video_1126_frames'  # extracted frames (interval = 1)
info_root = '/nfs/volume-95-7/illegal_parking/Yolov5_DeepSort_Pytorch/inference/video_1126_info'  # detect and re-id results

save_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1126/frames_ext0.1'  # save padding imgs for train TSM
save_videos_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1126/videos_ext0.1'  # save each car video
prefix = 'img_{:05d}.jpg'

if not os.path.exists(save_root):
    os.mkdir(save_root)
else:
    print("delete saving frames dir")
    shutil.rmtree(save_root)
    os.mkdir(save_root)

if not os.path.exists(save_videos_root):
    os.mkdir(save_videos_root)
else:
    print("delete saving videos dir")
    shutil.rmtree(save_videos_root)
    os.mkdir(save_videos_root)


def split_frames(frame_list):
    start = 0
    ans = []
    for i in range(1, len(frame_list)):
        if abs(frame_list[i] - frame_list[i-1]) >= 10: #帧相隔跨度很大，可能是追踪错误
            ans.append(frame_list[start:i])
            start = i

    ans.append(frame_list[start:])

    return ans


def image_padding(data, dim=3):
    data_out = []
    length = []
    weight = []
    for x in data:
        weidu = x.shape
        length.append(weidu[0])
        weight.append(weidu[1])

    MAX_l = max(length)  # 读取长的最大值
    MAX_W = max(weight)  # 宽的最大值

    for x in data:
        temp_tuple = x.shape  # 获取当前矩阵维度
        length = temp_tuple[0]  # 读取长
        width = temp_tuple[1]  # 读取宽
        pad_length_up = int((MAX_l - length) / 2)
        pad_length_down = int(MAX_l - length - pad_length_up)
        pad_width_left = int((MAX_W - width) / 2)
        pad_width_right = int(MAX_W - width - pad_width_left)
        matrix_pad = []
        if int(dim) == 3:
            matrix_pad = np.pad(x,
                                pad_width=((pad_length_up, pad_length_down),
                                           (pad_width_left, pad_width_right),
                                           (0, 0)  # 三维处理成一维之后就不用了
                                           ),
                                mode="constant", constant_values=(0, 0))
        np.array(matrix_pad).reshape((MAX_l, MAX_W, dim))
        temp_list = []
        temp_list.append(matrix_pad)
        q = np.asarray(temp_list).reshape(MAX_l, MAX_W, dim)
        data_out.append(q)
    out = np.asarray(data_out)
    return out  # 输出是已经处理好的矩阵，例如 （1450，500，500，3）1450张500*500的三通道图片


def crop_car_sequence(extension=0.1):
    for name in os.listdir(info_root):
        # get each mp4 information
        with open(os.path.join(info_root, name, 'frame_has_car_idx.json'), 'r') as f:
            frame_has_car_idx = json.load(f)

        loc_dict = np.load(os.path.join(info_root, name, 'loc_dict.npy')).item()

        for frame_idx in frame_has_car_idx.keys():

            img = Image.open(os.path.join(frames_root, name, '%d_%d.jpg' % (int(frame_idx) + 1, int(frame_idx) + 1)))

            for id in frame_has_car_idx[frame_idx]:

                x1 = loc_dict[int(frame_idx), int(id)][0]
                y1 = loc_dict[int(frame_idx), int(id)][1]
                x2 = loc_dict[int(frame_idx), int(id)][2]
                y2 = loc_dict[int(frame_idx), int(id)][3]

                if x2 - x1 <= 180 or y2 - y1 <= 100:  # too small!
                    continue

                name_id_frames_dir = os.path.join(save_root, name+'#'+str(id))
                if not os.path.exists(name_id_frames_dir):
                    os.mkdir(name_id_frames_dir)

                if extension <= 1:  # scale extension
                    # print("scale ext!")
                    w = x2 - x1
                    h = y2 - y1
                    scale_w_ext = w * extension
                    scale_h_ext = h * extension
                    cropped = img.crop((x1 - scale_w_ext, y1 - scale_h_ext, x2 + scale_w_ext, y2 + scale_h_ext))

                else:  # pixel extension
                    cropped = img.crop((x1 - extension, y1 - extension, x2 + extension, y2 + extension))

                cropped.save(os.path.join(name_id_frames_dir, '%d.jpg' % int(frame_idx)))
                print(name, str(id))


def check():
    for car_folder in os.listdir(save_root):
        imgs_list = os.listdir(os.path.join(save_root, car_folder))

        # 该ID的车，小于8帧
        if len(imgs_list) < 8:
            shutil.rmtree(os.path.join(save_root, car_folder))
            continue

        # 该ID的车，大于8帧
        frames_list = []
        for pic_name in imgs_list:
            fn = int(pic_name.split('.')[0])
            frames_list.append(fn)

        split_frame_list = split_frames(frame_list=frames_list)
        assert len(split_frame_list) > 0

        for fl in split_frame_list:

















if __name__ == '__main__':
    crop_car_sequence(extension=0.1)