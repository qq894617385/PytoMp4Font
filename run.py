from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
import os
from server.movie_factory import init_movie_factory
from server.utils import init_utils
from server.mysocket import init_webSocket, get_socketio


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)
    root_path = os.path.join(flask_app.root_path, 'static')
    # 初始化
    os.environ.setdefault('root', root_path)
    print(f'环境:{root_path} ')
    init_movie_factory(flask_app)
    init_webSocket(flask_app)
    init_utils(flask_app)

    print(f'socketio start:{get_socketio()}')

    # 使用 after_request 钩子来统一修改正常的响应格式
    @flask_app.after_request
    def modify_response(response):
        # 检查内容类型是否为 JSON
        if response.content_type == "application/json" and response.status_code == 200:
            # 尝试获取 JSON 数据，如果失败则保持原样返回
            try:
                data = response.get_json()
                new_response = jsonify(code=0, data=data)
                return new_response
            except ValueError:
                # 如果不是 JSON 格式，则直接返回原响应
                return response
        # 对于非 JSON 响应，直接返回原响应
        return response

    # 注册全局错误处理器
    register_error_handlers(flask_app)

    return flask_app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        """捕获所有异常，返回JSON格式的错误响应"""
        response = jsonify(code=500, msg=str(error))
        response.status_code = 500
        return response


if __name__ == '__main__':
    app = create_app()

    from congMovice.sound import sound_factory_init
    from stableDiffusion.null_make_image import init_make_ai_image

    # 初始化Ai绘图
    init_make_ai_image()

    # 初始化音效工厂
    sound_factory_init()

    app.run(port=5000, threaded=True)
