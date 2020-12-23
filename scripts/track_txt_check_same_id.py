# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: track_txt_check_same_id.py
@time: 2020/12/11
"""

import os
import cv2

def split_frames(frame_list):
    start = 0
    ans = []
    for i in range(1, len(frame_list)):
        if abs(frame_list[i] - frame_list[i-1]) >= 10: #帧相隔跨度很大，可能是追踪错误
            ans.append(frame_list[start:i])
            start = i

    ans.append(frame_list[start:])

    return ans

txt_file = '/nfs/volume-95-7/temporal-shift-module/Yolov5_DeepSort_Pytorch/inference/kebo_test/20201127103512_781877826285486080_242_445834_.txt'

with open(txt_file, 'r') as f:
    lines = f.readlines()

id_list = []
id_frame_idx = dict()


for line in lines:
    line = line.strip()
    line_split = line.split(' ')

    frame_idx = int(line_split[0])
    id = int(line_split[1])
    id_list.append(id)
    left = int(line_split[2])
    top = int(line_split[3])
    right = int(line_split[4])
    bottom = int(line_split[5])

    if id not in id_frame_idx.keys():
        id_frame_idx[id] = []

    id_frame_idx[id].append(frame_idx)


for id in id_frame_idx.keys():
    frame_idx_list = id_frame_idx[id]

    res = split_frames(frame_list=frame_idx_list)

    if len(res) > 1:
        print("same id!")
        print(id, frame_idx_list)

