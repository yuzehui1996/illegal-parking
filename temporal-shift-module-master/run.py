# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: run.py
@time: 2020/11/02
"""

import os
from time import sleep

# pretrained_model = ['TSM_kinetics_RGB_resnet50_shift8_blockres_avg_segment8_e50.pth',
#                     'TSM_kinetics_RGB_resnet50_shift8_blockres_avg_segment16_e50.pth']
#
# # pretrained_model = ['TSM_kinetics_RGB_resnet50_shift8_blockres_avg_segment8_e50.pth']
#
# for model in pretrained_model:
#     pretrain_path = os.path.join('pretrained', model)
#     pretrain_seg = model.split('_')[7][7:]
#     cmd = 'python main.py --tune_from=%s --store_name=%s > ./train_log/%s.log' % (pretrain_path, 'wenzhou+yuetan_pretrain_%s_ext0.2' % pretrain_seg, 'wenzhou+yuetan_pretrain_%s_ext0.2' % pretrain_seg)
#     os.system(cmd)
#     sleep(10)

cmd1 = 'python ./dataset/add_train_data_batch.py'
cmd2 = 'python main.py > ./train_log/1218.log 2>&1'

os.system(cmd1)
os.system(cmd2)