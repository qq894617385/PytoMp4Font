from moviepy.editor import *
import os


def create_captions(textArr, workSpacePath, total_time):
    current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
    imageMovie = os.path.join(current_directory, "video", "output.mp4")
    video = VideoFileClip(imageMovie).subclip(0, total_time)

    # 加载背景音乐
    mp3_total_name = os.path.join(current_directory, "video", "combined.mp3")
    bg_music = AudioFileClip(mp3_total_name)
    print("添加配音完成")
    # 创建字幕剪辑列表
    clips = [video]
    for value in textArr:
        start = value['start'] / 1000  # 起始时间，以秒为单位
        duration = value['duration'] / 1000  # 持续时间，以秒为单位
        text = value['text']
        txt_clip = (TextClip(text, fontsize=20, color='white', bg_color='black', font='SimHei')
                    .set_position(("center", video.h - 100)).set_start(start).set_duration(duration))
        clips.append(txt_clip)

    # 创建一个包含所有剪辑的CompositeVideoClip
    result = CompositeVideoClip(clips).set_audio(bg_music)

    allOutputFile = os.path.join(current_directory, "output", "last.mp4")
    result.write_videofile(allOutputFile, fps=25)
    print('输出last文件')

    # 关闭资源
    video.close()
    bg_music.close()
    result.close()
    return allOutputFile
