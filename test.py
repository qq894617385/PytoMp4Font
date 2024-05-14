from congMovice.sound import make_sound, sound_factory_init
from congMovice.video import make_background_video
from congMovice.captions import create_video_from_json
from congMovice.backgroundMusic import mp3_combine
import os
import math

# 当前文件夹目录
current_directory = os.getcwd()

workSpacePath = 'raw'

# sound_factory_init()
# # 生成声音文件
# mp3List = make_sound(workSpacePath)

create_video_from_json(workSpacePath)

# # 根据语音总的长度生成,总的视频预览图
# print(mp3List)
# # 计算总时间
# total_time = 0
#
# for item in mp3List:
#     total_time = total_time + item['duration']
#
# total_time = math.floor(total_time / 1000)
#
# print(f"总时间{total_time}")
# # 合成背景图片
# make_background_video(total_time, workSpacePath)
# print('视频背景图片制作完成')
#
# mp3_combine(workSpacePath)
# print('合成MP3完成')
#
# print('开始补充字幕')
# create_captions(mp3List, workSpacePath, total_time)
# print('全部完成....！')
