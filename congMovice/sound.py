import os
from datetime import datetime
import torch
from TTS.api import TTS
from pymediainfo import MediaInfo

print('正在初始化数据.....加载数据模型中')

# Set up TTS environment
os.environ.setdefault('TTS_HOME', os.getcwd())
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

print(f'加载完成....{device}')


def get_media_duration(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            return track.duration


def make_sound(textArr, workSpacePath):
    print('开始生成Ai语音')
    current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
    outputPath = os.path.join(current_directory, 'sounds')
    mp3List = []
    start = 0

    for index, text in enumerate(textArr):
        span_name = str(index) + '.mp3'
        current_time = datetime.now()
        outputName = os.path.join(outputPath, span_name)
        last_file = tts.tts_to_file(text=text, speaker_wav="voicelist/cn-sx.wav", speed=0.8, language="zh-cn",
                                    file_path=outputName)

        duration = get_media_duration(last_file)
        current_time1 = datetime.now()
        delta = current_time1 - current_time
        print(f"生成时间: {delta}, 文件名: {outputName}, 长度：{duration}")
        mp3List.append({
            "start": start,
            "sound": span_name,
            "duration": duration,
            "text": text
        })
        start += duration

    print('AI 语音完成')
    return mp3List
