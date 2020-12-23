# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: make_list.py
@time: 2020/10/28
"""

import os
import random
import shutil
import csv
import random


def random_split_list(alist, ratio, shuffle=True):
    assert sum(ratio) == 10
    k = 10
    _index = list(range(len(alist)))

    if shuffle:
        index = _index.copy()
        random.shuffle(index)

    each_group_num = len(alist) // k
    train_num = each_group_num * ratio[0]
    val_num = each_group_num * ratio[1]
    test_num = each_group_num * ratio[2]

    idx_list = [list(range(train_num)), list(range(val_num)), list(range(test_num))]
    remained = len(alist) - (train_num + val_num + test_num)

    if remained > 0:
        train_num += remained
        idx_list[0] = list(range(train_num))

    ans = idx_list.copy()
    idx_list[0] = index[0:train_num]
    idx_list[1] = index[train_num:train_num+val_num]
    idx_list[2] = index[train_num+val_num:]

    for g in range(3):
        for _, idx in enumerate(idx_list[g]):
            ans[g][_] = alist[idx]

    return ans


csv_file = '/nfs/volume-95-7/temporal-shift-module/labeling_results/wenzhou_labeling_results.csv'
frames_root = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/frames'

cnt = 0

n_more_0 = 0
n_more_1 = 0
n_less_0 = 0
n_less_1 = 0

more_run_list = []
more_stop_list = []

less_run_list = []
less_stop_list = []

dict1 = dict()

with open(csv_file, 'r') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):
        if i == 0:
            continue
        file_key = row[7]
        video_name = file_key.split('.')[0]
        results = int(row[10])
        assert results in [0, 1, 2]

        label = results
        path = os.path.join(frames_root, video_name)
        num_frames = len(os.listdir(path))
        dict1[video_name] = [num_frames, label]

        if num_frames >= 25:
            if results == 0:
                more_run_list.append(video_name)
            elif results == 1:
                more_stop_list.append(video_name)

        elif num_frames < 25 and num_frames >= 8:
            if results == 0:
                less_run_list.append(video_name)
            elif results == 1:
                less_stop_list.append(video_name)


# print(len(more_run_list), len(more_stop_list))
# print(len(less_run_list), len(less_stop_list))

more_run_split = random_split_list(alist=more_run_list, ratio=[8,1,1])
more_stop_split = random_split_list(alist=more_stop_list, ratio=[8,1,1])
less_run_split = random_split_list(alist=less_run_list, ratio=[8,1,1])
less_stop_split = random_split_list(alist=less_stop_list, ratio=[8,1,1])

more_run_train, more_run_val, more_run_test = more_run_split[0], more_run_split[1], more_run_split[2]
more_stop_train, more_stop_val, more_stop_test = more_stop_split[0], more_stop_split[1], more_stop_split[2]
less_run_train, less_run_val, less_run_test = less_run_split[0], less_run_split[1], less_run_split[2]
less_stop_train, less_stop_val, less_stop_test = less_stop_split[0], less_stop_split[1], less_stop_split[2]

# print(len(more_run_train),len(more_run_val),len(more_run_test))

save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/yuetan/balance/train.txt'
fw = open(save_txt, 'a')
for name in more_run_train:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in more_stop_train:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_run_train:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_stop_train:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

fw.close()

save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/balance/val.txt'
fw = open(save_txt, 'a')
for name in more_run_val:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in more_stop_val:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_run_val:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_stop_val:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

fw.close()

save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/balance/test.txt'
fw = open(save_txt, 'a')
for name in more_run_test:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in more_stop_test:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_run_test:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

for name in less_stop_test:
    path = os.path.join(frames_root, name)
    num_frames, label = dict1[name]
    fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')

fw.close()
#
# for name in val_stop_list:
#     path = os.path.join(frames_root, name)
#     num_frames, label = dict1[name]
#     fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')
#
# fw.close()
#
# save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/test.txt'
# fw = open(save_txt, 'w')
# for name in test_run_list:
#     path = os.path.join(frames_root, name)
#     num_frames, label = dict1[name]
#     fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')
#
# for name in test_stop_list:
#     path = os.path.join(frames_root, name)
#     num_frames, label = dict1[name]
#     fw.write(path + ' ' + str(num_frames) + ' ' + str(label) + '\n')
#
# fw.close()
#
