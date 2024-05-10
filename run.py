from flask import Flask, request, jsonify, after_this_request
import os

def create_app():
    flask_app = Flask(__name__)

    from server.movie_factory import init_movie_factory
    init_movie_factory(flask_app)

    # 注册全局错误处理器
    register_error_handlers(flask_app)

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

    return flask_app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        """捕获所有异常，返回JSON格式的错误响应"""
        # 可以根据需要更细分错误类型
        response = jsonify(code=500, msg=str(error))
        response.status_code = 500
        return response


if __name__ == '__main__':
    app = create_app()
    os.environ.setdefault('root', os.getcwd())
    # from congMovice.sound import sound_factory_init
    #
    # sound_factory_init()

    app.run(debug=True)
