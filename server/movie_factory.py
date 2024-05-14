from flask import request, send_from_directory, abort, jsonify
from werkzeug.utils import secure_filename

from movie_main import main_create
from concurrent.futures import ThreadPoolExecutor
from congMovice.utils import *
import os

executor = ThreadPoolExecutor(max_workers=5)


def init_movie_factory(app):
    @app.route('/makeMovie', methods=['POST', 'GET'])
    def txt2Video():
        request_json = request.json
        if 'projectName' in request_json:
            main_create(request_json['projectName'])
            return jsonify(code=0, msg="Movie creation initiated successfully.")
        else:
            raise KeyError("The 'projectName' parameter is required but was not provided.")

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

            if os.path.exists(f"{root_path}/dataSpace/{project_name}"):
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

                full_paths = [f'/{project_name}/images/' + file_name for file_name in image_files]

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

    @app.route('/upload_image/<project_name>', methods=['POST'])
    def upload_image(project_name):
        image_directory = os.path.join('dataSpace', project_name, 'images')
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_directory, filename))
            return jsonify({'message': 'File uploaded successfully'}), 201
        return jsonify({'error': 'Invalid file type'}), 400

    @app.route('/delete_image/<project_name>/<filename>', methods=['DELETE'])
    def delete_image(project_name, filename):
        image_path = os.path.join('dataSpace', project_name, 'images', secure_filename(filename))
        if os.path.exists(image_path):
            os.remove(image_path)
            return jsonify({'message': 'Image deleted successfully'}), 200
        return jsonify({'error': 'Image not found'}), 404

    @app.route('/update_text/<project_name>', methods=['POST'])
    def update_text(project_name):
        text_path = os.path.join('dataSpace', project_name, 'text.txt')
        textArr = request.json.get('textArr')

        if textArr is None:
            return jsonify({'error': 'No text provided'}), 400
        with open(text_path, 'w', encoding='utf-8') as file:
            text_content = ''.join(textArr)
            file.write(text_content)
        return jsonify({'message': 'Text updated successfully'}), 200

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
