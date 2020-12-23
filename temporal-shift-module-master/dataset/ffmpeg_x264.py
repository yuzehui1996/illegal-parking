# coding: utf-8
import os
import shutil

video_root = '/nfs/volume-95-7/temporal-shift-module/dataset/video_1130_2000/videos'
save_root = '/nfs/volume-95-7/temporal-shift-module/dataset/video_1130_2000/videos_x264'
txt_path = '/nfs/volume-95-7/temporal-shift-module/dataset/video_1130_2000/videos_1130_2000.txt'

if not os.path.exists(save_root):
	os.mkdir(save_root)
else:
	shutil.rmtree(save_root)
	os.mkdir(save_root)


fw = open(txt_path, 'w')
for video in os.listdir(video_root):
	if video.endswith('.mp4'):
		print(video)
		video_path = os.path.join(video_root, video)
		save_path = os.path.join(save_root, video)
		cmd = 'ffmpeg -i %s -vcodec libx264  %s' % (video_path, save_path)
		os.system(cmd)

		fw.write(save_path + '\n')

fw.close()