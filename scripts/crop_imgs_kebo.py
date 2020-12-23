# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: crop_imgs_kebo.py
@time: 2020/12/14
"""
import json
import cv2
import os
import base64
import requests
import time

headers = {'Content-type': 'application/json'}
# http_url = 'http://10.187.6.242:8080/v0/model/pytorch/predict'
# http_url = 'http://10.88.129.116:6481/v0/model/pytorch/predict'
http_url = 'http://10.186.1.125:8044/v0/model/pytorch/predict'

frames_root = '/nfs/volume-95-7/illegal_parking/scripts/4877D7C6EC783C1342FA02F60CA5BDBC_1607917691330'
json_file = './track_map_new.json'
save_imgs_root = '/nfs/volume-95-7/illegal_parking/scripts/81'

with open(json_file, 'r') as f:
    data_dict = json.load(f)

print('total car ID num: %d' % len(data_dict.keys()))

stop_num = 0
stop_car_ID = []

# car_ID = 81
for car_ID in data_dict.keys():

    if len(data_dict[car_ID]) < 8:
        continue

    input_data = {'info': [],
                  'car_ID': int(car_ID),
                  }

    for item in data_dict[str(car_ID)]:
        frame_idx = item['frame_idx']

        left = item['location']['left']
        top = item['location']['top']
        right = item['location']['right']
        bottom = item['location']['bot']

        img = cv2.imread(os.path.join(frames_root, '%04d.jpg' % int(frame_idx)))
        crop_img = img[top:bottom, left:right]

        # cv2.imwrite(os.path.join(save_imgs_root, '%04d.jpg' % int(frame_idx)), crop_img)

        # np_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        np_img = crop_img

        _, data_raw = cv2.imencode('.jpg', np_img)
        data_ = data_raw.tobytes()
        data_ = base64.b64encode(data_)

        cur_info = {
            "frame_idx": int(frame_idx),
            "img": data_
        }

        input_data['info'].append(cur_info)

    data = json.dumps(input_data)
    print("data ready!")
    detect_start_time = time.time()
    res = requests.post(http_url, data=data, headers=headers)
    detect_time = int((time.time() - detect_start_time) * 1000)
    # code = int(res.status_code)
    info = eval(res.text)
    print(info)

    if int(info['status']) == 1:
        stop_num += 1
        stop_car_ID.append(car_ID)

    print('####################################')

print(stop_num)
print(stop_car_ID)




