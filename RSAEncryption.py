# RSA类
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from AbsEncryption import EncryptionHandlerBase  # 导入抽象加密类
import base64

'''
RSA加密类, RSAEncryptionHandler 类继承了 EncryptionHandlerBase 抽象类，
并提供了生成 RSA 密钥对、使用 RSA 公钥加密文本以及使用 RSA 私钥解密文本的功能。
'''


class RSAEncryptionHandler(EncryptionHandlerBase):
    def __init__(self):
        super().__init__()

    def generate_key_pair(self, key_size=2048):
        """
        生成RSA密钥对。

        参数：
        key_size: int - 密钥长度，默认为2048。

        返回：
        tuple - 包含私钥和公钥的元组。
        """
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def encrypt_text(self, key, plaintext):
        """
        使用RSA公钥加密文本。

        参数：
        key: str - RSA公钥。
        plaintext: str - 明文文本。

        返回：
        str - 加密后的文本。
        """
        key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(key)
        ciphertext = cipher_rsa.encrypt(plaintext.encode('utf-8'))
        encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return encoded_ciphertext

    def decrypt_text(self, key, encoded_ciphertext):
        """
        使用RSA私钥解密文本。

        参数：
        key: str - RSA私钥。
        encoded_ciphertext: str - 加密后的文本。

        返回：
        str - 解密后的明文文本。
        """
        key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(key)
        ciphertext = base64.b64decode(encoded_ciphertext)
        plaintext = cipher_rsa.decrypt(ciphertext).decode('utf-8')
        return plaintext


# 示例用法

'''
if __name__ == '__main__':
    rsa_handler = RSAEncryptionHandler()

    # 生成密钥对
    private_key, public_key = rsa_handler.generate_key_pair()

    # 加密文本
    plaintext = "Hello, this is a secret message."
    encrypted_text = rsa_handler.encrypt_text(public_key, plaintext)
    print("加密后的文本:", encrypted_text)

    # 解密文本
    decrypted_text = rsa_handler.decrypt_text(private_key, encrypted_text)
    print("解密后的文本:", decrypted_text)
'''