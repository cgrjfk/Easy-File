# EncryptionFactory.py
from AESEncryption import AESEncryptionHandler
from RSAEncryption import RSAEncryptionHandler

'''
加密文件工厂创建类
'''


class EncryptionHandlerFactory:
    @staticmethod
    def create_handler(handler_type):
        if handler_type == 'AES':
            return AESEncryptionHandler()
        elif handler_type == 'RSA':
            return RSAEncryptionHandler()
        else:
            raise ValueError(f"不支持的加密类型: {handler_type}")
