# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: kebo_track_json_vis.py
@time: 2020/12/21
"""

import json
import os
import cv2

frames_root = './lFYFpRW8/frames/'
kebo_track_output_json = './track_res.json'
with open(kebo_track_output_json, 'r') as f:
    data_dict = json.load(f)

data_out = data_dict['result']['plate_files'][0]['result']['info']
# print(len(data_out))
total_ID_list = []
stop_car_ID = [1, 3, 4, 5, 6, 9, 13, 14, 16, 21, 22, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 42, 44, 46, 48, 51, 54, 58, 62, 67, 69]

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
        if id in stop_car_ID:
            label = '{}{:d}'.format("", id)
            cv2.putText(img, label, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 0, 255], 2)
        else:
            cv2.putText(img, label, (x1, y1 + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)

    return img

frame_dict = {}
for item in data_out:
    frame_idx_ = int(item['frame_idx'])
    frame_idx = frame_idx_ * 2
    carID = item['car_ID']
    total_ID_list.append(int(carID))
    left, top, right, bot = item['location']['left'],item['location']['top'],item['location']['right'],item['location']['bot']

    if frame_idx not in frame_dict:
        frame_dict[frame_idx] = []

    frame_dict[frame_idx].append([carID, left, top, right, bot])

print("total ID: %d" % len(list(set(total_ID_list))))
size = cv2.imread(os.path.join(frames_root, "%04d.jpg" % 0)).shape  # 需要转为视频的图片的尺寸
video = cv2.VideoWriter('./vis.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (size[1], size[0]))

for fi in range(len(os.listdir(frames_root))):
    img = cv2.imread(os.path.join(frames_root, '%04d.jpg' % fi))
    if fi not in frame_dict.keys():
        video.write(img)
        continue

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
