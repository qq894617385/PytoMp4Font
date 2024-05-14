from congMovice.sound import make_sound
from congMovice.captions import create_video_from_json


def main_create(projectName):
    # 当前文件夹目录
    workSpacePath = projectName

    # 生成声音文件
    make_sound(workSpacePath)
    # 根据json 生成视频
    create_video_from_json(workSpacePath)
    print('视频背景图片制作完成')

    return
