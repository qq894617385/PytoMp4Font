# from congMovice.sound import make_sound
# from congMovice.video import make_background_video
# from congMovice.captions import create_captions
from congMovice.backgroundMusic import mp3_combine
import os
import math

# 当前文件夹目录
current_directory = os.getcwd()

# make_background_video(252, 'raw')


# textArr = [
#     '毅哥哥，请你听到此广播后，赶快睡觉！',
#     '不要做无谓的抵抗',
#     '早睡早起身体棒',
#     '我是人工智能合成的语音播报。'
# ]
#
workSpacePath = 'raw'
#
# # 生成声音文件
# mp3List = make_sound(textArr, workSpacePath)
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
mp3_combine(workSpacePath)
# print('合成MP3完成')
#
# print('开始补充字幕')
# create_captions(mp3List, workSpacePath, total_time)
# print('全部完成....！')










