from flask import request, jsonify
import os
from stableDiffusion.null_make_image import make_ai_image
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)




def init_utils(app):
    @app.route('/make_null_to_images', methods=['POST'])
    def null2Images():
        request_json = request.get_json()  # 使用 get_json 方法是一个更好的选择
        project_name = request_json.get('projectName')
        root_path = os.environ['root']
        if project_name:
            image_directory = os.path.join(root_path, 'dataSpace', project_name, 'images')
            if os.path.exists(image_directory):
                text = request_json.get('text')
                if text:
                    executor.submit(make_ai_image, text, image_directory)
                    return jsonify({'msg': '请求已接收，正在处理'}), 200
                else:
                    return jsonify({'msg': '缺少必要的 text 参数'}), 400
            else:
                return jsonify({'msg': '项目目录不存在'}), 500
        else:
            return jsonify({'msg': '缺少 projectName 参数'}), 400

