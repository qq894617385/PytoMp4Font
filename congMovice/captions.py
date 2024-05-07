from moviepy.editor import *
import os


def mp3_combine(workSpacePath):
    try:
        current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
        directory_path = os.path.join(current_directory, 'sounds')
        mp3_total_name = os.path.join(current_directory, "video", "combined.mp3")

        # 读取所有MP3文件并加载为AudioFileClip对象
        clips = [AudioFileClip(os.path.join(directory_path, f)) for f in os.listdir(directory_path) if
                 f.endswith(".mp3")]

        # 使用concatenate_audio clips合并音频
        final_clip = concatenate_audioclips(clips)

        # 导出合并后的音频文件
        final_clip.write_audiofile(mp3_total_name)

        # 关闭所有的AudioFileClip对象
        for clip in clips:
            clip.close()

    except Exception as e:
        print(f"An error occurred: {e}")
        # 确保所有Clip被关闭
        for clip in clips:
            clip.close()


def create_captions(textArr, workSpacePath, total_time):
    current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
    imageMovie = os.path.join(current_directory, "video", "output.mp4")
    video = VideoFileClip(imageMovie).subclip(0, total_time)

    # 加载背景音乐
    mp3_total_name = os.path.join(current_directory, "video", "combined.mp3")
    bg_music = AudioFileClip(mp3_total_name)

    # 创建字幕剪辑列表
    clips = [video]
    for value in textArr:
        start = value['start'] / 1000  # 起始时间，以秒为单位
        duration = value['duration'] / 1000  # 持续时间，以秒为单位
        text = value['text']
        txt_clip = (TextClip(text, fontsize=24, color='white', bg_color='black', font='SimHei')
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
