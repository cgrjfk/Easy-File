from abc import ABC, abstractmethod
import qrcode

'''
由于只生成一个图片 不需要开启多线程 抽象二维码类
'''


class AbsQRCodeGenerator(ABC):
    def __init__(self, data_text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        """初始化类"""
        pass

    @abstractmethod
    def generate_qr(self):
        """生成二维码并返回PIL图像对象。"""
        pass

    @abstractmethod
    def save_qr(self, file_path):
        """保存生成的二维码到指定路径。"""
        pass
