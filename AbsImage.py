from abc import ABC, abstractmethod


# 抽象图片类
class absImage(ABC):
    @abstractmethod
    def __init__(self):  # 初始化函数，*args为未知参数，可能为格式类型，压缩命令，图片大小
        pass

    def imageProcess(self, input_path, output_path, *args):  # 处理图片函数
        pass

    '''def getData(self):  # 返回数据函数
        pass'''
