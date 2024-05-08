from pydub import AudioSegment
import os
from natsort import natsorted

def mp3_combine(workSpacePath):
    try:
        current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
        directory_path = os.path.join(current_directory, 'sounds')
        mp3_total_name = os.path.join(current_directory, "video", "combined.mp3")
        bg_music_path = os.path.join(os.getcwd(), 'bgm', "allbgm.mp3")
        bg_volume = -5  # dB

        # 读取所有MP3文件并加载为AudioSegment对象
        clips = [AudioSegment.from_file(os.path.join(directory_path, f)) for f in natsorted(os.listdir(directory_path)) if
                 f.endswith(".mp3")]

        # 合并音频
        final_clip = sum(clips)

        # 载入并调整背景音乐音量
        bg_music = AudioSegment.from_file(bg_music_path).apply_gain(bg_volume)

        # 计算背景音乐需要重复的次数，然后重复背景音乐
        repeat_count = int(final_clip.duration_seconds / bg_music.duration_seconds) + 1
        bg_music = bg_music * repeat_count

        # 设置背景音乐长度与主音频相同
        bg_music = bg_music[:len(final_clip)]

        # 创建一个合成音频剪辑，包括背景音乐和主音频
        final_clip = final_clip.overlay(bg_music)

        # 导出合并后的音频文件
        final_clip.export(mp3_total_name, format="mp3")

    except Exception as e:
        print(f"An error occurred: {e}")

