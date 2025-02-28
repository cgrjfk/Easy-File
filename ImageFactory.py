from ImageFormat import imageFormat
from ImageCompressor import imageCompressor
from ImageOCR import imageOCR

'''
图片处理工厂类，创建图片处理类
一旦外观界面点击 创建一个工厂类
'''


class imageFactory:
    # def __init__(self):  # 导入一个抽象的类的属性 然后使用里氏代换原则

    @staticmethod
    def create_image_factory(select_types):
        if select_types == '格式转化':
            return imageFormat()
        elif select_types == '图片压缩':
            return imageCompressor()
        elif select_types == 'OCR提取':
            return imageOCR()
        else:
            return False

