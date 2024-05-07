import os
import cv2
from PIL import Image
import numpy as np
import math


def make_background_video(total_time, workSpacePath):
    current_directory = os.path.join(os.getcwd(), 'dataSpace', workSpacePath)
    # 获取存放图片的文件
    imagePath = os.path.join(current_directory, 'images')

    output_directory = os.path.join(current_directory, 'video')
    video_name = 'output.mp4'

    mean_height = 0
    mean_width = 0

    # 获取图片列表，仅包括图片文件
    image_files = [f for f in os.listdir(imagePath) if f.endswith((".jpg", ".jpeg", ".png"))]
    num_of_images = len(image_files)

    for file in image_files:
        im = Image.open(os.path.join(imagePath, file))
        width, height = im.size
        mean_width += width
        mean_height += height

    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    for file in os.listdir('.'):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            im = Image.open(os.path.join(imagePath, file))

            width, height = im.size

    # 计算每张图片停留时间

    video_secs = math.ceil(total_time / num_of_images)
    print(video_secs)

    # 生成视频函数
    def generate_video():

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        images = [img for img in os.listdir(imagePath)
                  if img.endswith(".jpg") or
                  img.endswith(".jpeg") or
                  img.endswith("png")]
        # 获取图片资源库的长度
        num_images = len(images)

        print(images)

        frame = cv2.imread(os.path.join(imagePath, images[0]))

        # 设置输出路径
        output_path = os.path.join(output_directory, video_name)

        # 获取视频针
        height, width, layers = frame.shape

        video = cv2.VideoWriter(output_path, fourcc, 1.0, (width, height))
        print('正在输出视频')
        for i, image_name in enumerate(images):
            image_path = os.path.join(imagePath, image_name)
            image = cv2.imread(image_path)

            for _ in range(video_secs):
                video.write(image)

        cv2.destroyAllWindows()
        video.release()  # releasing the video generated

    generate_video()
    print('输出完成')
