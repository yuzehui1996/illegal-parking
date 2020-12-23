# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: check_already_video.py
@time: 2020/12/10
"""
import os

videos_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1201_5500/videos'
video_name_list = []
videos_num = 0

for video in os.listdir(videos_root):
    videos_num += 1
    video_name = video.split('#')[0]
    if video_name not in video_name_list:
        video_name_list.append(video_name)

print("Already process video num: %d" % len(list(set(video_name_list))))
print("Total output car video num: %d" % videos_num)