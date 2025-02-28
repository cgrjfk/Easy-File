import os
import time
import concurrent.futures
import pytesseract
from PIL import Image
from AbsImage import absImage
from MultiThreaded import multiThreaded

'''
图片OCR识别类，使用tesseract模型可以识别中文和，英文和数字
'''


class imageOCR(absImage):
    # 初始化函数
    def __init__(self, *args):
        self.is_open = multiThreaded.get_is_multi()

    '''
    @:param input_path 输入文件地址
    @:param output_path 输出文件地址
    @:param args 在这个类中 输入为识别文字语言 支持chi_sim,eng
    '''

    def imageProcess(self, in_path, out_path, *args):  # 处理图片函数
        if len(args) != 1:
            raise ValueError("必须提供一个语言格式")
        language = args[0]
        word_list_image = []  # 返回一个识别文字列表
        path_list_image = []  # 返回一个地址识别列表
        if os.path.isdir(out_path):
            if os.path.isfile(in_path):
                # 如果输入路径是文件，则转换单个文件
                word_list_image, path_list_image = self.convert_single_file(in_path, out_path, language)
                return word_list_image, path_list_image
            elif os.path.isdir(in_path):
                # 如果输入路径是文件夹，则转换文件夹中的所有文件
                word_list_image, path_list_image = self.convert_folder_file(in_path, out_path, language)
                return word_list_image, path_list_image
            else:
                # 如果都不是就报错
                return False
                # raise ValueError(f"这个{in_path}既不是文件也不是文件夹.")

        else:
            return False
            # raise ValueError(f"输出地址{out_path}必须为文件夹[imageOCR.py]")

            # 转化为单个文件

    # 识别单个文件
    def convert_single_file(self, in_path, out_path, language):
        # 设置识别exe的地址
        pytesseract.pytesseract.tesseract_cmd = r"./OCRModel/tesseract.exe"
        # 检查输入文件是否存在且为图片
        if not os.path.exists(in_path) or not self.is_image_file(in_path):
            print(f"输入文件不存在: {in_path}")
            return False  # 传递False ，让界面接口给出弹窗
        # OCR支持的格式
        supported_language = {
            'chi_sim', 'eng'
        }
        # 检查目标格式是否受支持
        if language not in supported_language:
            print(f"不支持的语言: {language}")
            return False  # 传递False ，让界面接口给出弹窗

        try:
            with Image.open(in_path) as image:
                # 使用Tesseract进行OCR
                text = pytesseract.image_to_string(image, lang=language)
                # print(text)  # 单元测试时使用
                # 获取每一行文本并保存到列表中
                word_list_single = [text]  # re.split(r'[。！？；.]', text)  # 这里使用了常见的中英文标点符号作为分隔符
                path_list_single = []  # 保存输出地址
                # 获取输出文件名和扩展名
                filename = os.path.basename(in_path)
                file_root = os.path.splitext(filename)[0]
                # 构造输出文件路径
                output_file_path = os.path.join(out_path, file_root + '.txt')
                output_file_path = os.path.abspath(output_file_path)  # 获取绝对路径
                output_file_path = os.path.normpath(output_file_path)  # 标准化路径格式
                # 写到输出文件地址里面
                with open(output_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                path_way = "图片已成功识别并保存到:" + str(output_file_path)
                # print(f"图片已成功识别并保存到: {output_file_path}")  # 单元测试时使用**
                path_list_single.append(path_way)
                return word_list_single, path_list_single  # 返回识别的文字以及识别后文本的保存地址
        except Exception as e:
            print(f"处理图像时出错: {e}")
            return False  # 错误返回False 让接口界面弹出错误弹窗

    # 识别文件夹中的文件
    def convert_folder_file(self, in_path, out_path, language):
        text_list = []  # 创建一个空列表用于存储提取的文本
        path_list = []  # 创建一个空列表用于存储保存后的地址
        if self.is_open:
            # 多线程模式下工作
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_file = {
                    executor.submit(self.convert_single_file, os.path.join(root, file), out_path, language): file
                    for root, _, files in os.walk(in_path)
                    for file in files
                    if self.is_image_file(os.path.join(root, file))}

                for future in concurrent.futures.as_completed(future_to_file):
                    file = future_to_file[future]
                    try:
                        text, output_file_path = future.result()
                        text_list.append(text)  # 将提取的文本添加到列表中
                        path_list.append(output_file_path)  # 将保存后的地址添加到列表中
                    except Exception as exc:
                        print(f'文件 {file} 生成时出现异常: {exc}')
            return text_list, path_list  # 返回包含所有文本提取结果和保存地址的列表

        else:
            # 单线程模式下工作
            for root, _, files in os.walk(in_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 检查文件是否为图片文件
                    if self.is_image_file(file_path):
                        text, path = self.convert_single_file(file_path, out_path, language)
                        text_list.append(text)  # 将提取的文本添加到列表中
                        path_list.append(path)
            return text_list, path_list  # 返回包含所有文本提取结果的列表 以及所有的文件保存的地址

    # 检测是否为图片
    def is_image_file(self, file_path):
        try:
            # 尝试使用 Pillow 加载文件，如果成功则说明是图片文件
            with Image.open(file_path) as img:
                return True
        except Exception as e:
            return False


# ------------------单元测试----------------------
'''
image_path = r"E:\测试文件夹"
out_path = r"E:\接收文件夹"
start_time = time.time()
imgOCR = imageOCR()  # 实例化对象
word_list, path_list = imgOCR.imageProcess(image_path, out_path, 'chi_sim')
end_time = time.time()
print("是否开启多线程:" + str(imgOCR.is_open))
print("total time:" + str(end_time - start_time))
# print(word_list)
print(path_list)

# 多线程模式下测试用例处理时间:0.5692629814147949
# 单线程模式下测试用例处理时间:0.5827524662017822
# 在测试用例较少的时候,开不开多线程差距不大
'''
