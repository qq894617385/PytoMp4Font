from diffusers import StableDiffusionPipeline
import torch
from zh_en_translate.zh_to_en import translate_zh_to_en, init_translate_zh_to_en
from datetime import datetime
import os
# 引入socket
from server.mysocket import get_socketio
pipeline = None


def init_make_ai_image():
    global pipeline

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"生成图片方式：{device}")

    root_path = os.environ['root']

    model_cache_dir = os.path.join(root_path, "image_model")

    pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        cache_dir=model_cache_dir
    )

    pipeline = pipeline.to(device)

    init_translate_zh_to_en()


def make_ai_image(des, output_path):
    socketio = get_socketio()
    global pipeline
    prompt = translate_zh_to_en(des)
    print(f"prompt:{prompt}")

    image = pipeline(prompt).images[0]

    # 生成时间戳文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.jpg"

    # 构建完整的文件路径
    full_path = os.path.join(output_path, filename)

    # 保存图像到指定路径
    image.save(full_path)
    print("完成生成图片")

    socketio.emit('update', {'data': f'{des}图片合成完成.'})
