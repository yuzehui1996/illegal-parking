# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: convert_model.py
@time: 2020/11/25
"""

import torch
from ops.models import TSN


def cvt_model():
    print("===> Loading model")

    model = TSN(2, 8, 'RGB',
              base_model='resnet50',
              consensus_type='avg',
              img_feature_dim=256,
              pretrain='imagenet',
              is_shift=True, shift_div=8, shift_place='blockres',
              non_local=False,
              )

    modelpath = '/nfs/volume-95-7/temporal-shift-module/checkpoint/TSM_videos_1218_RGB_resnet50_shift8_blockres_avg_segment8_e120_pr8_ext0.1/ckpt.best.pth.tar'
    checkpoint = torch.load(modelpath)
    checkpoint = checkpoint['state_dict']

    # base_dict = {('base_model.' + k).replace('base_model.fc', 'new_fc'): v for k, v in list(checkpoint.items())}
    base_dict = {'.'.join(k.split('.')[1:]): v for k, v in list(checkpoint.items())}
    replace_dict = {'base_model.classifier.weight': 'new_fc.weight',
                    'base_model.classifier.bias': 'new_fc.bias',
                    }
    for k, v in replace_dict.items():
        if k in base_dict:
            base_dict[v] = base_dict.pop(k)

    model.load_state_dict(base_dict)

    # 模型转换，Torch Script
    model.cuda()
    model.eval()
    example = torch.rand(1,8,3,224,224).cuda()
    y = model(example)
    print(y.shape)
    traced_script_module = torch.jit.trace(model, example)
    print(traced_script_module.code)
    # traced_script_module = torch.jit.script(model)
    # print(traced_script_module.code)
    # output = traced_script_module(torch.rand(1, 1, 224, 224))
    traced_script_module.save("tsm_with_1218.pt")

    print("Export of model.pt complete!")


def load_pt():
    model = torch.jit.load("./tsm_with_1218.pt")

    # input_example = torch.ones(1, 8, 3, 224, 224)

    input_example = torch.eye(224).cuda()
    input_example = input_example.expand((1, 8, 3, 224, 224)).cuda()

    y = model(input_example)
    print("pt output: ", y)


def load_src_model():
    model = TSN(2, 8, 'RGB',
                base_model='resnet50',
                consensus_type='avg',
                img_feature_dim=256,
                pretrain='imagenet',
                is_shift=True, shift_div=8, shift_place='blockres',
                non_local=False,
                )

    modelpath = '/nfs/volume-95-7/temporal-shift-module/checkpoint/TSM_videos_1218_RGB_resnet50_shift8_blockres_avg_segment8_e120_pr8_ext0.1/ckpt.best.pth.tar'
    checkpoint = torch.load(modelpath)
    checkpoint = checkpoint['state_dict']

    # base_dict = {('base_model.' + k).replace('base_model.fc', 'new_fc'): v for k, v in list(checkpoint.items())}
    base_dict = {'.'.join(k.split('.')[1:]): v for k, v in list(checkpoint.items())}
    replace_dict = {'base_model.classifier.weight': 'new_fc.weight',
                    'base_model.classifier.bias': 'new_fc.bias',
                    }
    for k, v in replace_dict.items():
        if k in base_dict:
            base_dict[v] = base_dict.pop(k)

    model.load_state_dict(base_dict)
    model.eval()

    # example = torch.ones(1, 8, 3, 224, 224)

    example = torch.eye(224)
    example = example.expand((1, 8, 3, 224, 224))

    y = model(example)
    print("src_model output: ", y)


if __name__ == '__main__':
    # cvt_model()
    load_src_model()
    load_pt()