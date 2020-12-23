# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: add_data.py
@time: 2020/11/02
"""

import os
import csv


csv_file = '/nfs/volume-95-7/temporal-shift-module/labeling_results/yuetan_labeling_results.csv'
frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/yuetan/frames_ext_50'
save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/yuetan/balance/all.txt'

dict1 = dict()
stop_cnt, run_cnt = 0, 0

fw = open(save_txt, 'w')

with open(csv_file, 'r') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        if i == 0:
            continue
        file_key = row[7]
        video_name = file_key.split('.')[0]
        print(video_name)
        results = int(row[10])
        assert results in [0, 1, 2]

        label = results
        path = os.path.join(frames_root, video_name)

        # if label == 0:
        #     run_cnt += 1
        # elif label == 1:
        #     stop_cnt += 1
        num_frames = len(os.listdir(path))
        # dict1[video_name] = [num_frames, label]
        if label != 2:
            fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

        # if num_frames >= 25:
        #     if results == 0:
        #         more_run_list.append(video_name)
        #     elif results == 1:
        #         more_stop_list.append(video_name)
        #
        # elif num_frames < 25 and num_frames >= 8:
        #     if results == 0:
        #         less_run_list.append(video_name)
        #     elif results == 1:
        #         less_stop_list.append(video_name)

# print(run_cnt, stop_cnt)
fw.close()