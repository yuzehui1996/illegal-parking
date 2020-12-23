# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: process_RGB.py
@time: 2020/12/15
"""

import os
import csv
import cv2


csv_file = '/nfs/volume-95-7/temporal-shift-module/labeling_results/videos_1201_500_TSM.csv'
frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1201_500/padding_frames'
new_frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1201_500/new_padding_frames'
if not os.path.exists(new_frames_root):
    os.mkdir(new_frames_root)

cur_train_data_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/with_1127/train.txt'
added_train_data_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/videos_1201_500/train.txt'

with open(cur_train_data_txt, 'r') as f:
    lines = f.readlines()

fw = open(added_train_data_txt, 'w')
for line in lines:
    fw.write(line)  # add prev training data lines

with open(csv_file, 'r') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        if i == 0:
            continue
        file_key = row[7]
        video_name = file_key.split('.')[0]

        if row[10] == '':
            continue

        results = int(row[10])
        assert results in [0, 1, 2]

        if results == 2:
            continue

        label = results
        path = os.path.join(frames_root, video_name)

        num_frames = len(os.listdir(path))
        if num_frames < 8:
            continue

        if not os.path.exists(os.path.join(new_frames_root, video_name)):
            os.mkdir(os.path.join(new_frames_root, video_name))

        for pic in os.listdir(os.path.join(frames_root, video_name)):
            pic_path = os.path.join(frames_root, video_name, pic)
            img = cv2.imread(pic_path)
            np_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(new_frames_root, video_name, pic), np_img)

        new_padding_path = os.path.join(new_frames_root, video_name)
        print(video_name)
        assert num_frames == len(os.listdir(new_padding_path))
        fw.write(new_padding_path + ' ' + str(num_frames) + ' ' + str(label) + '\n')  # add new training data lines

fw.close()