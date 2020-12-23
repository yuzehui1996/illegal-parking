# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: guangda_online_detect.py
@time: 2020/12/21
"""
import os
import cv2
import base64
import json
import requests
import shutil
import numpy as np

frames_root = '/nfs/volume-95-7/illegal_parking/scripts/lFYFpRW8/frames'
save_root = './guangda_detect'
if not os.path.exists(save_root):
    os.mkdir(save_root)
else:
    shutil.rmtree(save_root)
    os.mkdir(save_root)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def draw_boxes(img, bbox, offset=(0,0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        cv2.rectangle(img, (x1, y1), (x2, y2), [255,0,255], 3)

    return img


size = cv2.imread(os.path.join(frames_root, "%04d.jpg" % 0)).shape  # 需要转为视频的图片的尺寸
video = cv2.VideoWriter('/nfs/volume-95-7/illegal_parking/scripts/guangda_detect_vis.mp4', cv2.VideoWriter_fourcc('M', 'P', '4', '2'), 25, (size[1], size[0]))


for fi in range(len(os.listdir(frames_root))):
    frame_id = fi
    imgpath = os.path.join(frames_root, '%04d.jpg' % fi)
    image_data = open(imgpath, 'rb').read()
    f_str = base64.b64encode(image_data)

    data = {'img': None, 'frame_idx': int(frame_id)}
    # print(type(data))
    # print(type(f_str))
    data['img'] = f_str

    json_str = json.dumps(data, cls=MyEncoder)

    url = "http://10.88.151.9:6617/v0/model/pytorch/predict"

    headers = {"Content-Type": "application/json"}
    res = requests.post(url=url, headers=headers,
                        data=json_str, timeout=(3.05, 15))
    print(res.text)
    res_json = eval(res.text)

    img = cv2.imread(imgpath)
    bboxs = []

    for item in res_json['data']:
        left, top, right, bot = item['info']['location']['left'],item['info']['location']['top'],item['info']['location']['right'],item['info']['location']['bot']
        bboxs.append([int(left), int(top), int(right), int(bot)])

    drawed_img = draw_boxes(img, bboxs)
    cv2.imwrite(os.path.join(save_root, '%04d.jpg' % fi), drawed_img)
    video.write(drawed_img)

video.release()
