# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: interval_frames.py
@time: 2020/11/07
"""

import os
import shutil

interval = 3
txt_list = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/wenzhou_yuetan_ext50/test.txt'
save_txt = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/interval_frames/wenzhou_yuetan_ext50/test.txt'
prefix = 'img_{:05d}.jpg'
root = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/interval_frames'

save_root = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/interval_frames/frames_ext_50'
if not os.path.exists(save_root):
    os.mkdir(save_root)
else:
    print("delete exist dir!")
    shutil.rmtree(save_root)
    os.mkdir(save_root)

with open(txt_list, 'r') as f:
    lines = f.readlines()

fw = open(save_txt, 'w')


def copy_dir_interval_frames(src_path, tgt_path, interval=interval):
    cnt = 0

    for i, pic in enumerate(os.listdir(path)):
        if i % interval == 0:
            src = os.path.join(src_path, pic)
            tgt = os.path.join(tgt_path, pic)
            shutil.copy(src, tgt)
            new_pic_name = prefix.format(cnt)

            os.rename(tgt, os.path.join(tgt_path, new_pic_name))

            cnt += 1

    return cnt


for line in lines:
    line = line.strip()
    line_split = line.split(' ')

    path = line_split[0]
    num_frames = line_split[1]

    if int(num_frames) < 8 * interval:
        continue

    label = line_split[2]

    dir = path.split('/')[-2]
    name = path.split('/')[-1]

    src_path = path
    tgt_path = os.path.join(root, dir, name)

    if not os.path.exists(tgt_path):
        os.mkdir(tgt_path)

    new_num_frames = copy_dir_interval_frames(src_path=src_path, tgt_path=tgt_path)

    fw.write(tgt_path + ' ' + str(new_num_frames) + ' ' + str(label) + '\n')
    print(path)


fw.close()

