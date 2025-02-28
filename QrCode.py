import qrcode
from AbsQrCode import AbsQRCodeGenerator

'''
二维码生成类 生成二维码
'''


class QRCodeGenerator(AbsQRCodeGenerator):
    def __init__(self, data_text, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        """
        初始化二维码生成器。

        参数:
            data: str -- 需要编码成二维码的文本或URL。
            version: int -- 控制二维码的大小，1到40，数字越大，包含的信息越多。
            error_correction: qrcode.constants -- 控制二维码的容错能力。
            box_size: int -- 控制每个小方格的像素数。
            border: int -- 控制边框（默认为4）。
        """
        super().__init__(data_text, version, error_correction, box_size, border)
        self.data = data_text
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border
        self.qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )

    def generate_qr(self):
        """生成二维码并返回PIL图像对象。"""
        self.qr.add_data(self.data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill='black', back_color='white')
        return img

    def save_qr(self, file_path):
        """保存生成的二维码到指定路径。"""
        img = self.generate_qr()
        return img


'''
---------单元测试-------------
if __name__ == "__main__":
    # 示例：创建二维码并保存到文件
    data = "https://www.example.com"
    qr_generator = QRCodeGenerator(data)
    image = qr_generator.save_qr("example_qr.png")
    open(image)
'''
