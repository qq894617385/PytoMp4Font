from moviepy.editor import *
import os
import json


def create_video_from_json(workSpacePath):
    root_path = os.environ['root']
    current_directory = os.path.join(root_path, 'dataSpace', workSpacePath)
    jsonPath = os.path.join(current_directory, 'index.json')

    # 加载 JSON 文件
    with open(jsonPath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    output_directory = os.path.join(current_directory, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    clips = []

    # 背景音乐和图片目录
    mp3_directory = os.path.join(current_directory, "sounds")

    for idx, item in enumerate(json_data['textArr']):
        text = item['text']
        bg_image_path = os.path.join(current_directory, "images", item['bgi'])

        # 读取配音文件
        mp3_path = os.path.join(mp3_directory, f"{idx}.mp3")
        audio_clip = AudioFileClip(mp3_path)
        audio_duration = audio_clip.duration  # 获取音频持续时间
        print(f"{audio_duration}多少秒")

        # 加载背景图片并设置持续时间为音频持续时间
        bg_image_clip = ImageClip(bg_image_path).set_duration(audio_duration)

        # 获取图像尺寸并根据宽高比调整大小
        img_width, img_height = bg_image_clip.size
        if img_width > img_height:
            scale_factor = 640 / float(img_width)
        else:
            scale_factor = 640 / float(img_height)
        new_size = (int(img_width * scale_factor), int(img_height * scale_factor))

        # 调整图片大小并保持比例
        bg_image_clip = bg_image_clip.resize(new_size)

        # 创建一个640x640的黑色背景
        bg_color_clip = ColorClip(size=(640, 640), color=(0, 0, 0), duration=audio_duration)

        # 将调整后的图片居中放置在黑色背景上
        combined_clip = CompositeVideoClip([bg_color_clip, bg_image_clip.set_position("center")], size=(640, 640))

        # 创建文字剪辑，并设置持续时间为音频持续时间
        txt_clip = TextClip(text, fontsize=24, color='white', bg_color='black', font='SimHei').set_position(
            'center').set_duration(audio_duration)

        # 将文字剪辑合成到背景图片上
        combined_clip = CompositeVideoClip([combined_clip, txt_clip.set_position(('center', 'bottom'))])
        combined_clip = combined_clip.set_audio(audio_clip)  # 设置音频

        clips.append(combined_clip)

    # 合并所有视频剪辑
    final_clip = concatenate_videoclips(clips, method="compose")

    # 输出最终视频
    final_output = os.path.join(output_directory, "final_output.mp4")
    final_clip.write_videofile(final_output, codec='libx264', fps=24)

    # 关闭所有剪辑
    final_clip.close()
    for clip in clips:
        clip.close()
        audio_clip.close()  # 确保关闭音频文件以释放资源

    print("视频已成功生成：", final_output)
