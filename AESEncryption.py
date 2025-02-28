# AES类
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from AbsEncryption import EncryptionHandlerBase

'''
AESEncryptionHandler加密类:使用AES加密，继承EncryptionHandlerBase
'''


class AESEncryptionHandler(EncryptionHandlerBase):
    def __init__(self):
        super().__init__()

    def encrypt_text(self, key, plaintext):
        plaintext = plaintext.encode('utf-8')

        if len(key) not in [16, 24, 32]:
            raise ValueError('密钥长度必须是16, 24或32字节。')

        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        encoded_ciphertext = base64.b64encode(iv + ciphertext).decode('utf-8')

        return encoded_ciphertext

    def decrypt_text(self, key, encoded_ciphertext):
        if len(key) not in [16, 24, 32]:
            raise ValueError('密钥长度必须是16, 24或32字节。')

        try:
            ciphertext = base64.b64decode(encoded_ciphertext)
            iv = ciphertext[:AES.block_size]
            actual_ciphertext = ciphertext[AES.block_size:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(actual_ciphertext), AES.block_size).decode('utf-8')
            return plaintext
        except Exception as e:
            raise ValueError('解密失败: {}'.format(str(e)))
