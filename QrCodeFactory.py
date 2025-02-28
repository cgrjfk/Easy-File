
import qrcode

from QrCode import QRCodeGenerator

'''
二维码工厂类 实现二维码的创建
'''


class QRCodeFactory:
    @staticmethod
    def create_qr_generator(data_text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10,
                            border=4):
        return QRCodeGenerator(data_text, version, error_correction, box_size, border)
