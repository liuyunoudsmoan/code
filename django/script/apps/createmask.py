import os
from PIL import Image
import requests


from lib.options import BaseOptions


def process_jpg_files(folder_path):
    # 获取文件夹中所有的 JPG 文件列表
    jpg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]

    for file in jpg_files:
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, file)

        # 调用 Remove.bg API 移除背景
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(file_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'aynoitcGZW41x3PepjUhni1N'},
        )

        if response.status_code == requests.codes.ok:
            # 保存移除背景后的图像
            output_path = os.path.join(folder_path, f"output_{file}")
            with open(output_path, 'wb') as out:
                out.write(response.content)

            # 打开透明背景图像
            input_image = Image.open(output_path)

            # 创建一个新的图像，大小和透明背景图像一致，背景为黑色
            output_image = Image.new("RGB", input_image.size, (0, 0, 0))

            # 获取透明背景图像的像素数据
            pixels = input_image.load()

            # 遍历每个像素
            for i in range(input_image.size[0]):
                for j in range(input_image.size[1]):
                    # 获取当前像素的RGBA值
                    r, g, b, a = pixels[i, j]

                    # 如果透明度大于0，说明是人体部分，将其替换为白色
                    if a > 0:
                        output_image.putpixel((i, j), (255, 255, 255))

            # 保存结果图像为 PNG 格式
            mask_path = os.path.join(folder_path, f"{file.split('.')[0]}_mask.png")
            output_image.save(mask_path, format='PNG')

            print(f"Processed file: {file}")
        else:
            print(f"Error processing file: {file}")


def delete_output_files(folder_path):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件夹中的每个文件
    for file in files:
        # 检查文件名是否以 "output" 开头并且是文件（不是文件夹）
        if file.startswith("output") and os.path.isfile(os.path.join(folder_path, file)):
            # 构建文件的完整路径并删除
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            print(f"Deleted file: {file}")



opt = BaseOptions().parse()
# 调用函数并传入文件夹路径
folder_path = '/img'
process_jpg_files(folder_path)
delete_output_files(folder_path)