# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: add_test_data.py
@time: 2020/12/05
"""
import os
import csv
import random

cur_test_txt = ''

csv_file = '/nfs/volume-95-7/temporal-shift-module/labeling_results/videos_1201_5000_TSM.csv'
frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1201_5000/padding_frames'
name_list = []

stop_cnt, run_cnt = 0, 0

fw = open('/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/videos_1201_500/test3.txt', 'w')

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

        # if label in [0, 1]:
        #     name_list.append((video_name, label))
        #     if label == 0:
        #         run_cnt += 1
        #     elif label == 1:
        #         stop_cnt += 1
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

fw.close()

# print(run_cnt, stop_cnt)
# print(len(name_list))
#
# run_cnt, stop_cnt = 0, 0
# test_name_list = random.sample(name_list, 635)
# print(len(test_name_list))
#
# remain_name_list = list(set(name_list) - set(test_name_list))
# print(len(remain_name_list))
#
# fw = open('./test2.txt', 'w')
# for name, label in test_name_list:
#     path = os.path.join(frames_root, name)
#     num_frames = len(os.listdir(path))
#     assert label in [0, 1]
#     assert num_frames >= 8
#
#     fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')
#
#     if label == 0:
#         run_cnt += 1
#     elif label == 1:
#         stop_cnt += 1
#
# print('test2.txt', run_cnt, stop_cnt)
# fw.close()
#
# fw = open('./remain.txt', 'w')
# for name, label in remain_name_list:
#     path = os.path.join(frames_root, name)
#     num_frames = len(os.listdir(path))
#     assert label in [0, 1]
#     assert num_frames >= 8
#
#     fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')
#
#     if label == 0:
#         run_cnt += 1
#     elif label == 1:
#         stop_cnt += 1
#
# print('remain.txt', run_cnt, stop_cnt)
# fw.close()

# with open('./remain.txt', 'r') as f:
#     lines = f.readlines()
#
# line_list = []
# for line in lines:
#     line = line.strip()
#     line_split = line.split(' ')
#     label = int(line_split[-1])
#     assert label in [0, 1]
#     line_list.append(line)
#
# print(len(line_list))
# val_line_list = random.sample(line_list, 500)
# train_line_list = list(set(line_list) - set(val_line_list))
#
# fw = open('./train.txt', 'w')
# for line in train_line_list:
#     fw.write(line + '\n')
# fw.close()
#
#
# fw = open('./val.txt', 'w')
# for line in val_line_list:
#     fw.write(line + '\n')
# fw.close()





