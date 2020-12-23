# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: from_txt_vis_track.py
@time: 2020/12/08
"""
import os
import cv2

txt_file = '/nfs/volume-95-7/illegal_parking/scripts/kebo_input_track_output.txt'
frames_root = '/nfs/volume-95-7/illegal_parking/test/Yolov5_DeepSort_Pytorch/kebo_test_sample_track_results/20201127103512_781877826285486080_242_445834_'

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)

def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)

def draw_boxes(img, bbox, identities=None, offset=(0,0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(img, (x1, y1), (x1 + t_size[0] + 3, y1 + t_size[1] + 4), color, -1)
        cv2.putText(img, label, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
    return img


with open(txt_file, 'r') as f:
    lines = f.readlines()

frame_dict = {}
id_list = []

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

    if frame_idx not in frame_dict.keys():
        frame_dict[frame_idx] = []

    frame_dict[frame_idx].append((id, left, top, right, bottom))

print('kebo_track_results_id_num: %d' % len(list(set(id_list))))

size = cv2.imread(os.path.join(frames_root, "%03d.jpg" % 0)).shape  # 需要转为视频的图片的尺寸
video = cv2.VideoWriter('./vis.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (size[1], size[0]))

for fi in frame_dict.keys():
    img = cv2.imread(os.path.join(frames_root, '%03d.jpg' % fi))

    ids = []
    bboxs = []
    for item in frame_dict[fi]:
        cur_id = item[0]
        cur_bbox = [item[1], item[2], item[3], item[4]]

        ids.append(cur_id)
        bboxs.append(cur_bbox)

    drawed_img = draw_boxes(img=img, bbox=bboxs, identities=ids)
    video.write(drawed_img)

video.release()
cv2.destroyAllWindows()