# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: my_request.py
@time: 2020/11/19
"""
import traceback
import cv2
import os
import time
import requests
import json
import base64
from PIL import Image


def face_detect():
    headers = {'Content-type': 'application/json'}
    http_url = 'http://10.186.1.125:8044/v0/model/pytorch/predict'
    # http_url = 'http://10.88.129.116:6481/v0/model/pytorch/predict'

    txt_list = '/nfs/volume-95-7/temporal-shift-module/dataset/txt_list/videos_1201_500/test1.txt'
    # imgs_dir = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/scale/frames_scale_10/133_91_1' # test_list 0
    imgs_dir = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/scale/frames_scale_10/25_17_0'  # test_list_2  1
    # imgs_dir = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/scale/frames_scale_10/1_55_0'  # test_list_3  1

    try:
        with open(txt_list, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            imgs_dir = line.split(' ')[0]

            # total_images = len(os.listdir(imgs_dir))
            imgs_dir = '/nfs/volume-95-7/temporal-shift-module/dataset/wenzhou_200/scale/frames_scale_10/25_17_0'  # test_list_2  1

            dict_data = {
                "info": [],
                "car_ID": 91,
            }

            for i, img in enumerate(os.listdir(imgs_dir)):
                ori_img = os.path.join(imgs_dir, img)
                image = cv2.imread(ori_img)
                # img_cv2pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                # np_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                np_img = image
                # print(np_img.shape)
                _, data_raw = cv2.imencode('.jpg', np_img)
                # if i == 0:
                #     print(data_raw)
                data_ = data_raw.tobytes()
                data_ = base64.b64encode(data_)
                add_data = {
                    "frame_idx": i,
                    "img": data_
                }
                dict_data["info"].append(add_data)

            data = json.dumps(dict_data)
            detect_start_time = time.time()
            print("data ready!")

            res = requests.post(http_url, data=data, headers=headers)
            detect_time = int((time.time() - detect_start_time) * 1000)
            code = int(res.status_code)

            print('####################################')

            info = eval(res.text)
            print(info)
            # fea = info['data'][0]['feature']
            #
            # for i in range(512):
            #     print(fea[i])

            # print(info)
            # # success,no person
            # msg = info['msg']
            # all_result = []
            # if msg != 'success':
            #     print all_result
            # else:
            #     data = info['data']['candidate']
            #     for i in range(len(data)):
            #         location = data[i]['location']
            #         score = data[i]['prob']
            #         top, right, bot, left = float(location['top']) / scale[0], float(location['right']) / scale[1], float(
            #             location['bot']) / scale[0], float(location['left']) / scale[1]
            #
            #         result = [left, top, right, bot, score]
            #         all_result.append(result)
            #     print all_result
            #     print('time cost:', detect_time)
    except Exception:
        traceback.print_exc()
        return None


def kebo_request():
    with open('./tsm_req_kebo.json') as f:
        data_dict = json.load(f)

    # print(data_dict.keys())
    # print(len(data_dict['info']))

    for item in data_dict['info']:
        print(item.keys())


if __name__=='__main__':
    face_detect()
    # kebo_request()


