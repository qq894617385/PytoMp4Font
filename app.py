from flask import Flask, request, send_file, send_from_directory
from main import main_create
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)


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


if __name__ == '__main__':
    app.run(debug=True)
