import os
from abc import ABC, abstractmethod
from MultiThreaded import multiThreaded


# 抽象文件类
class absFile(ABC):
    @abstractmethod
    # 抽象构造函数
    def __init__(self, max_workers=os.cpu_count()):  # 最大多线程数值为CPU数量
        pass

    @abstractmethod
    # 抽象单个文件转换方式
    def convert_single_file(self, input_path, output_path):
        pass

    @abstractmethod
    #  抽象文件夹转换方式
    def convert_folder_file(self, input_path, output_path):
        pass

    @abstractmethod
    # 判断是否为单个文件还是一个文件夹的文件
    def judge_single_folder(self, input_path, out_path):
        pass
