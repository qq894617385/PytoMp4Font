from flask import Flask, request, send_file, send_from_directory
from main import main_create
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)


@app.route('/textToAiVideo', methods=['POST', 'GET'])
def txt2Video():
    request_json = request.json
    textArr = request_json['textArr']

    # 将main_create函数放入线程池异步执行
    future = executor.submit(main_create, textArr, 'test')
    # 等待异步处理完成
    file_path = future.result()

    # return send_file(file_path, as_attachment=True)
    return '完成！'


if __name__ == '__main__':
    app.run(debug=True)
