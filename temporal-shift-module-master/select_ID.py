# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: select_ID.py
@time: 2020/12/07
"""
import cv2
import os
import base64
import json
import time
import requests

ID_dict = {}
headers = {'Content-type': 'application/json'}
http_url = 'http://10.187.6.234:8080/v0/model/pytorch/predict'
frames_root = '/nfs/volume-95-7/temporal-shift-module/select_ID/frames'

# with open('./select_ID/track_results.txt', 'r') as f:
#     lines = f.readlines()
#
# for line in lines:
#     line = line.strip()
#     line_split = line.split(' ')
#     frame_idx = line_split[0]
#     ID = line_split[1]
#     left = int(line_split[2])
#     top = int(line_split[3])
#     right = int(line_split[4])
#     bottom = int(line_split[5])
#
#     if ID not in ID_dict.keys():
#         ID_dict[ID] = []
#     ID_dict[ID].append((frame_idx, left, top, right, bottom))
#
# print(len(ID_dict.keys()))
#
# stop_num = 0
# stop_car_ID = []
#
# for id in ID_dict.keys():
#     input_data = {'info':[]}
#
#     for item in ID_dict[id]:
#         frame_idx = int(item[0])
#         left = int(item[1])
#         top = int(item[2])
#         right = int(item[3])
#         bottom = int(item[4])
#
#         img = cv2.imread(os.path.join(frames_root, '%03d.jpg' % frame_idx))
#         img = img[top:bottom, left:right]
#
#         np_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         _, data_raw = cv2.imencode('.jpg', np_img)
#         data_ = data_raw.tobytes()
#         data_ = base64.b64encode(data_)
#
#         cur_info = {
#             "frame_idx":frame_idx,
#             "img": data_
#         }
#
#         input_data['info'].append(cur_info)
#
#     if len(input_data['info']) < 8:
#         continue
#
#     data = json.dumps(input_data)
#     print("data ready!")
#     detect_start_time = time.time()
#     # res = requests.post(http_url, data=data, headers=headers)
#     # detect_time = int((time.time() - detect_start_time) * 1000)
#     # code = int(res.status_code)
#     # info = eval(res.text)
#     # print(info)
#
#     # if info['status'] == 1:
#     #     stop_num += 1
#     #     stop_car_ID.append(id)
#
#
#
#     print('####################################')
#     # time.sleep(1)
#
# print(stop_num)
# print(stop_car_ID)


#################### for wangyan

# stop_car_ID = ['215', '134', '139', '224', '289', '288', '8', '282', '261', '128', '56', '295', '292', '293', '311', '196', '252', '276', '69', '80', '81', '255', '300', '305', '306', '245', '246', '240', '101', '339', '60', '66', '176', '250', '174', '254', '182', '183', '180', '164', '94', '162', '11', '272', '152', '232', '48', '41', '320', '146', '206', '208', '71', '70']
kebo_stop_car_ID = [8, 11, 30, 48, 56, 66, 70, 71, 80, 81, 94, 101, 107, 117, 125, 139, 146, 152, 162, 164, 174, 180, 196, 202, 208, 209, 224, 232, 233, 240, 246, 250, 252, 254, 255, 261, 272, 276, 282, 288, 289, 292, 293, 295, 300, 305, 306, 311, 320, 339]
# for car_id in kebo_stop_car_ID:
#     if str(car_id) not in stop_car_ID:
#         print(car_id)


match_dict = {
    "data":[
    ]
}

with open('./select_ID/track_results.txt', 'r') as f:
    lines = f.readlines()

frame_dict = {}
for line in lines:
    line = line.strip()
    line_split = line.split(' ')
    frame_idx = int(line_split[0])
    ID = line_split[1]
    left = int(line_split[2])
    top = int(line_split[3])
    right = int(line_split[4])
    bottom = int(line_split[5])

    if frame_idx not in frame_dict.keys():
        frame_dict[frame_idx] = []

    frame_dict[frame_idx].append((ID, left, top, right, bottom))


for fi in frame_dict.keys():

    match_dict = {
        "data": [],
        "frame_idx":fi,
    }
    index = 0

    for item in frame_dict[fi]:
        id = int(item[0])
        left = item[1]
        top = item[2]
        right = item[3]
        bottom = item[4]

        if id in kebo_stop_car_ID:
            cur_match_data = {
                "index": index,
                "car_ID": id,
                'info': {
                    "location": {
                        "bot": bottom,
                        "left": left,
                        "right": right,
                        "top": top,
                    },
                    "pred": 0.9,
                    "value": 1,
                }
            }

            match_dict['data'].append(cur_match_data)
            index += 1
            print(fi, index)

    if len(match_dict['data']) > 0:
        with open(os.path.join('./select_ID/for_match/', '%d.json' % fi), 'w') as f1:
            json.dump(match_dict, f1, indent=4, separators=(',', ':'))
