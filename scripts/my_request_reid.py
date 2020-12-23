# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: my_request.py
@time: 2020/11/19
"""
import traceback
import cv2
import sys
import time
import requests
import json
import base64



def face_detect():
    headers = {'Content-type': 'application/json'}
    http_url = 'http://10.186.1.125:8044/v0/model/pytorch/predict'
    # http_url = 'http://10.187.6.234:8080/v0/model/pytorch/predict'
    # http_url = 'http://10.88.129.116:6475/v0/model/pytorch/predict'
    dict_data = {
        "frame_idx": 0,
        "data":
            [
                {
                    "index": 0,
                    "info":{
                        "location":{
                            "bot": 814,
                            "left": 0,
                            "right": 463,
                            "top": 516,

                        }

                    },
                    "pred":0.85,
                },

                {
                    "index": 1,
                    "info":{
                        "location":{
                            "bot": 519 + 139,
                            "left": 704,
                            "right": 704 + 169,
                            "top": 519,
                        }
                    },
                    "pred":0.85,
                },
                #
                # {
                #     "car_index": 2,
                #     "info": {
                #         "location": {
                #             "bottom": 519 + 139,
                #             "left": 704,
                #             "right": 704 + 169,
                #             "top": 519,
                #         }
                #     },
                #     "pred":0.85,
                # },
            ],
        "ori_img": None
    }
    try:
        ori_img = '/nfs/volume-95-7/illegal_parking/dataset/wenzhou_frames_1_new/1/1_1.jpg'
        image = cv2.imread(ori_img)
        # np_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # _, data_raw = cv2.imencode('.jpg', np_img)
        _, data_raw = cv2.imencode('.jpg', image)

        data_ = data_raw.tobytes()
        data_ = base64.b64encode(data_)
        dict_data['ori_img'] = data_
        data = json.dumps(dict_data)
        detect_start_time = time.time()
        res = requests.post(http_url, data=data, headers=headers)
        detect_time = int((time.time() - detect_start_time))
        code = int(res.status_code)
        # if code != 200:
        #     status = 1
        #     error_code = 4
        #     return
        print('####################################')

        print(code)
        # info = eval(res.text)
        info = res.text
        print(info)
        print(detect_time)
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


if __name__=='__main__':
    face_detect()


