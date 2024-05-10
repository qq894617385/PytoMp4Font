import os


def list_subdirectories(directory):
    """
    列出指定目录下的所有子目录名称。

    :param directory: 要遍历的目录的路径。
    :return: 包含所有子目录名称的列表。
    """
    # 确保目录是存在的
    if not os.path.exists(directory):
        print(f"指定的目录不存在: {directory}")
        return []

    # os.listdir(directory) 返回指定路径下的文件和目录列表
    # os.path.isdir(os.path.join(directory, name)) 检查指定路径是否为目录
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return subdirectories


