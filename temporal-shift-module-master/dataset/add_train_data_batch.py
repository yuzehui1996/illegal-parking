# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: add_train_data.py
@time: 2020/12/09
"""
import os
import csv

csv_files = os.listdir('/nfs/volume-95-7/temporal-shift-module/labeling_results/1218_new_data')
# mission_names = []

cur_train_data_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/videos_1201_500/train_added_videos_1201_5500.txt'
added_train_data_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/1218/train.txt'

with open(cur_train_data_txt, 'r') as f:
    lines = f.readlines()

fw = open(added_train_data_txt, 'w')
for line in lines:
    fw.write(line)  # add prev training data lines

for i, csv_file in enumerate(csv_files):
    csv_file = os.path.join('/nfs/volume-95-7/temporal-shift-module/labeling_results/1218_new_data', csv_file)
    # csv_file = '/nfs/volume-95-7/temporal-shift-module/labeling_results/videos_1201_5500_TSM.csv'
    # frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1201_5500/padding_frames'
    names = csv_file.split('/')[-1].split('.')[0]
    frames_root = os.path.join('/nfs/volume-95-7/temporal-shift-module/dataset/', names, 'padding_frames')

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)

        for i, row in enumerate(reader):
            if i == 0:
                continue
            file_key = row[7]
            video_name = file_key.split('.')[0]
            print(video_name)

            if row[10] == '':
                continue

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
                fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')  # add new training data lines

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