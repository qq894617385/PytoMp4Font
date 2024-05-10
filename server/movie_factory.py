from flask import request, send_from_directory, abort, jsonify
from movie_main import main_create
from concurrent.futures import ThreadPoolExecutor
from congMovice.utils import *
import os

executor = ThreadPoolExecutor(max_workers=5)


def init_movie_factory(app):
    @app.route('/textToAiVideo', methods=['POST', 'GET'])
    def txt2Video():
        request_json = request.json

        if 'textArr' in request_json:
            textArr = request_json['textArr']
        else:
            file_path = f'dataSpace/raw/text.txt'

            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            text = text.replace("，", "。")
            sentences = text.split('。')

            new_data = []
            i = 0
            while i < len(sentences):
                if len(sentences[i]) <= 6:
                    # 如果当前字符串长度小于5，则与后一个字符串合并，并在它们之间加上逗号
                    if i < len(sentences) - 1:
                        merged_string = sentences[i] + ',' + sentences[i + 1]
                        new_data.append(merged_string)
                        i += 1  # 跳过已合并的下一个字符串
                else:
                    new_data.append(sentences[i])
                i += 1
            sentences = new_data
            # 去除空白行
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

            textArr = sentences
        # 将main_create函数放入线程池异步执行
        future = executor.submit(main_create, textArr, 'raw')
        # 等待异步处理完成
        file_path = future.result()
        # return send_file(file_path, as_attachment=True)
        return textArr

    # 获取所有项目名
    @app.route('/getProjectNameList', methods=['POST', 'GET'])
    def getProjectName():
        folders = list_subdirectories("dataSpace")
        return folders

    # 根据项目所在的地址获取相关图片信息
    @app.route('/getProjectDetail', methods=['POST'])
    def getDetailByName():
        request_json = request.json
        root_path = os.environ['root']
        print(root_path)
        if 'projectName' in request_json:
            project_name = request_json['projectName']

            if os.path.exists(f"/images/{root_path}/dataSpace/{project_name}"):
                print("存在文件")
                result = {}

                openPath = os.path.join('dataSpace', project_name)

                images_path = os.path.join(openPath, 'images')

                text_path = os.path.join(openPath, 'text.txt')

                if os.path.exists(text_path) and os.path.isfile(text_path):
                    # 文件存在，读取并打印每一行
                    with open(text_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        result['textArr'] = lines
                else:
                    # 文件不存在，创建一个空的text.txt文件
                    with open(text_path, 'w', encoding='utf-8') as file:
                        print(f"创建了一个空文件: {text_path}")

                # 获取图片数组
                image_files = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".jpeg", ".png"))]

                full_paths = [f'{project_name}/' + file_name for file_name in image_files]

                result['images'] = full_paths

                return result

        return {}

    # 读取图片
    @app.route('/images/<path:filename>')
    def get_image(filename):
        root_path = os.environ['root']
        # 指定你的图片存放路径
        image_directory = os.path.join(root_path, 'dataSpace')
        # 确保文件名安全，防止路径遍历攻击
        if not os.path.isfile(os.path.join(image_directory, filename)):
            abort(404)  # 如果文件不存在，返回 404 错误
        return send_from_directory(image_directory, filename)

    # 新建项目
    @app.route('/create_project', methods=['POST'])
    def create_project():
        project_name = request.json.get('project_name')
        if not project_name:
            return jsonify({'error': 'Project name is required'}), 400
        root_path = os.environ['root']
        project_path = os.path.join(root_path, 'dataSpace', project_name)
        # 检查项目目录是否已存在
        if os.path.exists(project_path):
            return jsonify({'code': -1, 'error': 'Project already exists'}), 409  # 409 Conflict

        try:
            # 创建项目目录
            os.makedirs(project_path, exist_ok=True)

            # 创建子目录
            subfolders = ['images', 'output', 'sounds', 'video']
            for folder in subfolders:
                os.makedirs(os.path.join(project_path, folder), exist_ok=True)

            # 创建一个 text.txt 文件
            text_file_path = os.path.join(project_path, 'text.txt')
            with open(text_file_path, 'w') as f:
                f.write('Initial content of the text file.')

            return jsonify({'message': f'Project {project_name} created successfully'}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    #TODO： 上传对应项目下的images文件夹 下图片

    #TODO： 删除对应项目下的images文件夹 下的图片

    #TODO： 修改对象项目下的 text.txt文件内容


