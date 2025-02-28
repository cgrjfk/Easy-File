# pdf转化为word
import os
import subprocess
import time

from pdf2docx import Converter
from AbsFile import absFile  # 导入抽象类
from MultiThreaded import multiThreaded  # 导入唯一实例
from concurrent.futures import ThreadPoolExecutor, wait


class pdf_to_word(absFile):
    # 初始化类
    def __init__(self, max_workers=os.cpu_count(), progress_callback=None):
        self.isTrue = multiThreaded.get_is_multi()  # 通过唯一实例判断是否启用多线程
        self.max_workers = max_workers
        self.progress_callback = progress_callback  # 进度更新的回调函数

    # 转换单个文件
    def convert_single_file(self, input_path, output_path):
        # 检查是否有权限写入文件，没有就请求权限
        self.check_and_request_permission(output_path)
        # 获取输入文件的文件名（不包括扩展名）
        filename = os.path.basename(input_path)
        file_root = os.path.splitext(filename)[0]

        # 构造输出文件路径
        output_file_path = os.path.join(output_path, file_root + ".docx")

        # 打开并转换PDF文件
        cv = Converter(input_path)
        cv.convert(output_file_path, start=0, end=None)
        cv.close()
        if self.progress_callback:
            self.progress_callback(100)  # 单个文件直接完成100%
        print(f"文件已成功转换并保存到: {output_file_path}")
        return [output_file_path]

    # 转化多个文件
    def convert_folder_file(self, input_path, output_path):
        output_paths = []
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        self.check_and_request_permission(output_path)

        if self.isTrue:
            futures = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
                total_files = len(pdf_files)
                for index, filename in enumerate(pdf_files):
                    input_file = os.path.join(input_path, filename)
                    future = executor.submit(self.convert_single_file, input_file, output_path)
                    futures.append(future)
                    if self.progress_callback:
                        progress = int((index + 1) / total_files * 100)
                        self.progress_callback(progress)
            wait(futures)
            for future in futures:
                output_paths.extend(future.result())
        else:
            pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
            total_files = len(pdf_files)
            for index, filename in enumerate(pdf_files):
                in_path = os.path.join(input_path, filename)
                output_paths.extend(self.convert_single_file(in_path, output_path))
                if self.progress_callback:
                    progress = int((index + 1) / total_files * 100)
                    self.progress_callback(progress)
        return output_paths

    # 判断是否为单个文件还是一个文件夹的文件，然后调用以上方式进行转换
    def judge_single_folder(self, input_path, output_path):
        out_path = []
        if os.path.isfile(input_path):
            # 如果输入路径是文件，则转换单个文件
            out_path = self.convert_single_file(input_path, output_path)
            return out_path
        elif os.path.isdir(input_path):
            # 如果输入路径是文件夹，则转换文件夹中的所有文件
            out_path = self.convert_folder_file(input_path, output_path)
            return out_path
        else:
            # 如果都不是就报错
            raise ValueError(f"这个{input_path}既不是文件也不是文件夹.")

    # 请求写入的权限，否则无法写入
    def check_and_request_permission(self, output_path):
        # 检查当前用户是否有写入权限
        if os.access(output_path, os.W_OK):
            print(f"当前用户已经对{output_path}有写入权限。")
        else:
            print(f"当前用户没有对{output_path}的写入权限，尝试请求权限...")
            try:
                # 使用 icacls 命令授予当前用户完全控制权限
                username = os.getlogin()
                command = f'icacls "{output_path}" /grant {username}:(OI)(CI)F /T'
                subprocess.run(command, shell=True, check=True)
                print(f"权限请求成功，现在{output_path}具有写入权限。")
            except subprocess.CalledProcessError as e:
                print(f"权限请求失败: {e}")

'''
# 示例用法
pdf_file = r"E:\测试\文件接收文件夹" # 输入的PDF文件路径
docx_file = r"E:\测试"  # 输出的Word文件路
pdf_to_word_K = pdf_to_word()
print(pdf_to_word_K.isTrue)
start_time = time.time()
# 自动判断是否为文件还是文件夹
pdf_to_word_K.judge_single_folder(pdf_file, docx_file)
end_time = time.time()
print(end_time - start_time)

# 多线程运行时间 8.808996438980103
# 单线程运行时间 12.80504298210144
# 使用多线程在测试的例子中快了45%左右
'''