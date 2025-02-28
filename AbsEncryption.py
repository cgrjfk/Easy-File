from abc import ABC, abstractmethod

'''
抽象加密类
'''


class EncryptionHandlerBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def encrypt_text(self, key, plaintext):
        """
        加密文本的抽象方法。

        参数：
        key: str - 加密密钥。
        plaintext: str - 明文文本。

        返回：
        str - 加密后的文本。
        """
        pass

    @abstractmethod
    def decrypt_text(self, key, encoded_ciphertext):
        """
        解密文本的抽象方法。

        参数：
        key: str - 解密密钥。
        encoded_ciphertext: str - 加密后的文本。

        返回：
        str - 解密后的明文文本。
        """
        pass
