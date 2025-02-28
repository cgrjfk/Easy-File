import os
import time
from concurrent.futures import ThreadPoolExecutor, wait

from AbsImage import absImage
from PIL import Image
from MultiThreaded import multiThreaded
from PIL import ImageFile

# 遇到文件损坏的直接跳过
ImageFile.LOAD_TRUNCATED_IMAGES = True

'''
图片格式转换类
初始化时少使用参数，调用方法时参数使用，尽量不使用内部属性，防止重新实例化对象，确保对象始终可以重复使用
'''


# 图片格式转化类


class imageFormat(absImage):
    # 初始化函数
    def __init__(self, *args):
        self.is_open = multiThreaded.get_is_multi()

    '''
    @:param input_path 输入文件地址
    @:param output_path 输出文件地址
    @:param args 在这个类中 输入为图片格式参数
    '''

    def imageProcess(self, inp_path, out_path, *args):  # 处理图片函数
        information_list = []  # 保存的处理后的图片地址
        if len(args) != 1:
            raise ValueError("必须提供一个图像格式参数")
        image_format = args[0]
        if os.path.isdir(out_path):
            if os.path.isfile(inp_path):
                # 如果输入路径是文件，则转换单个文件
                information_list = self.convert_single_file(inp_path, out_path, image_format)
                # information_list = list(dict.fromkeys(information_list))  # 去除重复项
                return information_list
            elif os.path.isdir(inp_path):
                # 如果输入路径是文件夹，则转换文件夹中的所有文件
                information_list = self.convert_folder_file(inp_path, out_path, image_format)
                # information_list = list(dict.fromkeys(information_list))
                return information_list
            else:
                # 如果都不是就报错
                raise ValueError(f"这个{inp_path}既不是文件也不是文件夹.")
        else:
            raise ValueError(f"输出地址{out_path}必须为文件夹[ImageFormat.py]")
            # 转化为单个文件

    '''
    @:param input_path 输入文件地址
    @:param output_path 输出文件地址
    @:param image_format  输入为图片格式参数
    '''

    # 转化单个图片

    # 转化为多个文件
    # 转化为多个文件
    def convert_folder_file(self, in_path, out_path, image_format):
        output_paths = []  # 保存输出文件路径的列表
        # print(self.is_open)
        if self.is_open:
            futures = []  # 存储任务的Future对象列表
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                # 遍历输入文件夹中的所有文件
                for filename in os.listdir(in_path):
                    file_path = os.path.join(in_path, filename)
                    # 检查文件是否为图片文件
                    if self.is_image_file(file_path):
                        future = executor.submit(self.convert_single_file, file_path, out_path, image_format)
                        futures.append(future)  # 将任务的Future对象添加到列表中

            # 等待所有任务完成并获取结果
            wait(futures)
            for future in futures:
                output_paths.append(future.result())  # 获取任务的返回值，即输出文件路径

        else:
            # 遍历文件夹中的所有文件
            for root, _, files in os.walk(in_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 检查文件是否为图片文件
                    if self.is_image_file(file_path):
                        output_paths.append(self.convert_single_file(file_path, out_path, image_format))

        return output_paths  # 返回保存文件夹的列表

    @staticmethod
    def convert_single_file(in_path, out_path, image_format):
        # 检查输入文件是否存在
        if not os.path.exists(in_path):
            print(f"输入文件不存在: {in_path}")
            return []

        # Pillow支持的格式
        supported_formats = {
            'JPEG': 'jpeg', 'PNG': 'png', 'GIF': 'gif', 'BMP': 'bmp', 'JPG': 'jpg',
            'TIFF': 'tiff', 'PPM': 'ppm', 'ICO': 'ico', 'WEBP': 'webp'
        }

        # 检查目标格式是否受支持
        if image_format.upper() not in supported_formats.keys():
            print(f"不支持的格式: {image_format}")
            return []

        try:
            with Image.open(in_path) as img:
                # 转换格式
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGB")
                # 获取输出文件名和扩展名
                filename = os.path.basename(in_path)
                file_root = os.path.splitext(filename)[0]
                # 构造输出文件路径
                output_file_path = os.path.join(out_path, file_root + '.' +
                                                supported_formats.get(image_format.upper()))
                output_file_path = os.path.abspath(output_file_path)  # 获取绝对路径
                output_file_path = os.path.normpath(output_file_path)  # 标准化路径格式
                print(output_file_path)
                # 转换图像格式并保存 在输入jpg时，转化为jpeg文件 这个是因为PIL只支持转化为jpeg文件，但是可以用jpg文件的格式存储
                if image_format == "jpg":
                    img.save(output_file_path, format='JPEG')
                else:
                    img.save(output_file_path, format=image_format)
                print(f"图片已成功转换并保存到: {output_file_path}")
                return [output_file_path]  # 返回包含单个元素的列表
        except Exception as e:
            print(f"处理图像时出错: {e}")
            return []

    @staticmethod
    def is_image_file(file_path):
        # 定义图片文件的常见扩展名
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ppm', '.ico', '.webp']

        # 获取文件扩展名
        _, file_extension = os.path.splitext(file_path)

        # 将扩展名转换为小写，并检查是否在图片扩展名列表中
        if file_extension.lower() in image_extensions:
            return True
        else:
            return False
