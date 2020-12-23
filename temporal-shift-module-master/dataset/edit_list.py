# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: edit_list.py
@time: 2020/10/31
"""

import os

txt_root = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/wenzhou_yuetan_ext50'
# train_list = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/wenzhou_yuetan_ext50/train.txt'
# val_list = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/balance/val.txt'
# test_list = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/balance/test.txt'

save_txt_root = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/wenzhou_yuetan_ext0.2'

if not os.path.exists(save_txt_root):
    os.mkdir(save_txt_root)

for txt_list in os.listdir(txt_root):
    txt_path = os.path.join(txt_root, txt_list)
    with open(txt_path, 'r') as f:
        lines = f.readlines()

    fw = open(os.path.join(save_txt_root, txt_list), 'w')

    for line in lines:
        line = line.strip()
        line_split = line.split(' ')

        path = line_split[0]
        frames_num = line_split[1]
        label = line_split[2]

        dataset_name = path.split('/')[-3]
        # frames_root = path.split('/')[-2]
        name = path.split('/')[-1]

        if 'wenzhou' in dataset_name:
            prefix = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/scale/frames_scale_20'
            new_path = os.path.join(prefix, name)
        elif 'yuetan' in dataset_name:
            prefix = '/nfs/volume-95-7/temporal-shift-module/dataset/yuetan/scale/frames_scale_20'
            new_path = os.path.join(prefix, name)
        else:
            new_path = None

        assert new_path is not None

        # new_path = path.replace('frames', 'frames_ext_100')
        # if not os.path.exists(new_path):
        #     print(txt_list, name)

        # if len(os.listdir(new_path)) != int(frames_num):
        #     print("error!")

        assert len(os.listdir(new_path)) == int(frames_num)

        fw.write(new_path + ' ' + frames_num + ' ' + label + '\n')

    fw.close()