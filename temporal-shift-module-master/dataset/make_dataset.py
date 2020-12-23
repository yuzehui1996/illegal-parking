# coding: utf-8
import os
import json
import numpy as np
from PIL import Image
import cv2
import shutil

img_size = (1920, 1080)
fps = 25

frames_root = '/nfs/volume-95-7/illegal_parking/dataset/videos_1202_frames'  # extracted frames (interval = 1)
info_root = '/nfs/volume-95-7/illegal_parking/Yolov5_DeepSort_Pytorch/inference/video_1202_info'  # detect and re-id results

save_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1202/frames_ext0.1'  # save padding imgs for train TSM
save_videos_root = '/nfs/volume-95-7/temporal-shift-module/dataset/videos_1202/videos_ext0.1'  # save each car video
prefix = 'img_{:05d}.jpg'

if not os.path.exists(save_root):
    os.mkdir(save_root)
else:
    print("delete saving frames dir")
    shutil.rmtree(save_root)
    os.mkdir(save_root)


if not os.path.exists(save_videos_root):
    os.mkdir(save_videos_root)
else:
    print("delete saving videos dir")
    shutil.rmtree(save_videos_root)
    os.mkdir(save_videos_root)


def split_frames(frame_list):
    start = 0
    ans = []
    for i in range(1, len(frame_list)):
        if abs(frame_list[i] - frame_list[i-1]) >= 10: #帧相隔跨度很大，可能是追踪错误
            ans.append(frame_list[start:i])
            start = i

    ans.append(frame_list[start:])

    return ans


def image_padding(data, dim=3):
    data_out = []
    length = []
    weight = []
    for x in data:
        weidu = x.shape
        length.append(weidu[0])
        weight.append(weidu[1])

    MAX_l = max(length)  # 读取长的最大值
    MAX_W = max(weight)  # 宽的最大值

    for x in data:
        temp_tuple = x.shape  # 获取当前矩阵维度
        length = temp_tuple[0]  # 读取长
        width = temp_tuple[1]  # 读取宽
        pad_length_up = int((MAX_l - length) / 2)
        pad_length_down = int(MAX_l - length - pad_length_up)
        pad_width_left = int((MAX_W - width) / 2)
        pad_width_right = int(MAX_W - width - pad_width_left)
        matrix_pad = []
        if int(dim) == 3:
            matrix_pad = np.pad(x,
                                pad_width=((pad_length_up, pad_length_down),
                                           (pad_width_left, pad_width_right),
                                           (0, 0)  # 三维处理成一维之后就不用了
                                           ),
                                mode="constant", constant_values=(0, 0))
        np.array(matrix_pad).reshape((MAX_l, MAX_W, dim))
        temp_list = []
        temp_list.append(matrix_pad)
        q = np.asarray(temp_list).reshape(MAX_l, MAX_W, dim)
        data_out.append(q)
    out = np.asarray(data_out)
    return out  # 输出是已经处理好的矩阵，例如 （1450，500，500，3）1450张500*500的三通道图片


def crop_car_sequence(extension):
    for name in os.listdir(info_root):
        # if name != 'a2':
        #     continue
        # get each mp4 information
        with open(os.path.join(info_root, name, 'car_happen_frame.json'), 'r') as f:
            car_happen_frame_dict = json.load(f)

        loc_dict = np.load(os.path.join(info_root, name, 'loc_dict.npy')).item()

        for car_idx in car_happen_frame_dict.keys():
            car_happen_frame_list = car_happen_frame_dict[car_idx]
            split_frame = split_frames(car_happen_frame_list)
            # print(name, car_idx, split_frame)

            for i, frame_list in enumerate(split_frame):
                if len(frame_list) < 8:
                    continue

                is_left_car = False
                is_whole_screen = False
                imgs_list = []

                for frame_idx in frame_list:
                    x1 = loc_dict[frame_idx, int(car_idx)][0]
                    y1 = loc_dict[frame_idx, int(car_idx)][1]
                    x2 = loc_dict[frame_idx, int(car_idx)][2]
                    y2 = loc_dict[frame_idx, int(car_idx)][3]

                    if (x1 + x2)/2 <= img_size[0] / 2:  # car in the left!
                        is_left_car = True
                        break

                    # if abs(x1+w1 - img_size[0]) <= 10:  # whole screen!
                    #     is_whole_screen = True
                    #     break

                    if x2-x1 <= 180 or y2-y1 <= 100: # too small!
                        continue

                    img = Image.open(os.path.join(frames_root, name, '%d_%d.jpg' % (frame_idx+1, frame_idx+1)))
                    if extension <= 1:  # scale extension
                        # print("scale ext!")
                        w = x2 - x1
                        h = y2 - y1
                        scale_w_ext = w * extension
                        scale_h_ext = h * extension
                        cropped = img.crop((x1-scale_w_ext, y1-scale_h_ext, x2+scale_w_ext, y2+scale_h_ext))

                    else:  # pixel extension
                        cropped = img.crop((x1 - extension, y1 - extension, x2 + extension, y2 + extension))

                    # cropped.save(os.path.join(save_dir, '%d.jpg' % frame_idx))
                    cropped = np.array(cropped)
                    imgs_list.append(cropped)

                if len(imgs_list) >= 8:
                    print(name, car_idx, i)
                    padding_imgs = image_padding(data=imgs_list)
                    save_dir = os.path.join(save_root, "%s_%s_%d" % (name, car_idx, i))
                    if not os.path.exists(save_dir):
                        os.mkdir(save_dir)

                    for ii in range(padding_imgs.shape[0]):
                        A = padding_imgs[ii].reshape(padding_imgs.shape[1], padding_imgs.shape[2], padding_imgs.shape[3])
                        im = Image.fromarray(A)
                        im.save(os.path.join(save_dir, prefix.format(ii)))

                    # make video from frames
                    filelist = os.listdir(save_dir)
                    size = cv2.imread(os.path.join(save_dir, filelist[0])).shape  # 需要转为视频的图片的尺寸
                    video = cv2.VideoWriter(os.path.join(save_videos_root, "%s_%s_%d.mp4" % (name, car_idx, i)),
                                            cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                            (size[1], size[0]))

                    for item in filelist:
                        if item.endswith('.jpg'):
                            frame = cv2.imread(os.path.join(save_dir, item))
                            video.write(frame)

                    video.release()
                    cv2.destroyAllWindows()

                if is_left_car or is_whole_screen:
                    continue


def doing_image_padding():
    root = '/nfs/volume-95-7/temporal-shift-module/dataset/test'
    save_root = '/nfs/volume-95-7/temporal-shift-module/dataset/test_padding'

    for folder in os.listdir(root):
        print(folder)
        imgs_list = []
        index = []
        for pic in os.listdir(os.path.join(root, folder)):
            img = Image.open(os.path.join(root, folder, pic))
            img = np.array(img)
            imgs_list.append(img)
            index.append(pic)

        padding_imgs = image_padding(data=imgs_list)

        if not os.path.exists(os.path.join(save_root, folder)):
            os.mkdir(os.path.join(save_root, folder))

        for i in range(padding_imgs.shape[0]):
            A = padding_imgs[i].reshape(padding_imgs.shape[1], padding_imgs.shape[2], padding_imgs.shape[3])
            im = Image.fromarray(A)
            im.save(os.path.join(save_root, folder, index[i]))


def frame2video(save_root, save_videos_root):
    fps = 25
    for folder in os.listdir(save_root):
        filelist = os.listdir(os.path.join(save_root, folder))
        size = cv2.imread(os.path.join(save_root, folder, filelist[0])).shape # 需要转为视频的图片的尺寸
        video = cv2.VideoWriter(os.path.join(save_videos_root, '%s.mp4' % folder), cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                (size[1], size[0]))

        for item in filelist:
            if item.endswith('.jpg'):
                frame = cv2.imread(os.path.join(save_root, folder, item))
                video.write(frame)

        video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # cnt = 0
    # # crop_car_sequence()
    # # doing_image_padding()
    # root = '/nfs/volume-95-7/temporal-shift-module/dataset/my_dataset_padding_new'
    # for folder in os.listdir(root):
    #     # frame2video(frames_root=os.path.join(root, folder))
    #     if len(os.listdir(os.path.join(root, folder))) >= 25:
    #         frame2video(frames_root=os.path.join(root, folder))
    #         cnt += 1
    #
    # print(cnt)

    crop_car_sequence(extension=0.1)