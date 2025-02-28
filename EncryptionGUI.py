import base64
import ctypes
import sys
import warnings

from Crypto.Random import get_random_bytes
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QComboBox, QDesktopWidget, QGridLayout, QHBoxLayout
)

from EncryptionFactory import EncryptionHandlerFactory

'''
子系统测试 文本接口类GUI
'''
# 设置应用程序 ID
appId = "ID"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class EncryptDecryptApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # 初始化UI设计
    def initUI(self):
        self.setWindowTitle('文件加密解密')
        self.setWindowIcon(QIcon('encryption_icon/EncryptionIcon.png'))

        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央

        self.layout = QVBoxLayout()

        # 密钥输入框
        self.key_label = QLabel('密钥:')
        self.layout.addWidget(self.key_label)
        self.key_input = QLineEdit()
        self.layout.addWidget(self.key_input)

        # 加密类型选择框
        self.encryption_type_label = QLabel('选择加密类型:')
        self.layout.addWidget(self.encryption_type_label)
        self.encryption_type_combo = QComboBox()
        self.encryption_type_combo.addItems(['AES', 'RSA'])
        self.encryption_type_combo.currentTextChanged.connect(self.toggle_key_buttons)
        self.layout.addWidget(self.encryption_type_combo)

        # 生成密钥按钮
        self.generate_key_button = QPushButton(QIcon("encryption_icon/key.png"), '生成密钥')
        self.generate_key_button.clicked.connect(self.generate_key)
        self.layout.addWidget(self.generate_key_button)

        # 生成RSA公钥私钥按钮
        self.generate_rsa_keys_button = QPushButton(QIcon("encryption_icon/key.png"), '生成RSA密钥对')
        self.generate_rsa_keys_button.clicked.connect(self.generate_rsa_keys)
        self.layout.addWidget(self.generate_rsa_keys_button)
        self.generate_rsa_keys_button.hide()

        # ----------------水平布局------------------
        # 公钥显示框
        # 创建水平布局对象
        key_display_layout = QHBoxLayout()

        # 公钥显示框
        self.public_key_display = QTextEdit()
        self.public_key_display.setPlaceholderText('公钥文本框')
        self.public_key_display.setReadOnly(True)
        key_display_layout.addWidget(self.public_key_display)
        self.public_key_display.hide()

        # 私钥显示框
        self.private_key_display = QTextEdit()
        self.private_key_display.setPlaceholderText('私钥文本框')
        self.private_key_display.setReadOnly(True)
        key_display_layout.addWidget(self.private_key_display)
        self.private_key_display.hide()

        # 将水平布局添加到主布局中
        self.layout.addLayout(key_display_layout)

        # 明文输入框
        self.plaintext_label = QLabel('明文:')
        self.layout.addWidget(self.plaintext_label)
        self.plaintext_input = QTextEdit()
        self.plaintext_input.setPlaceholderText("明文")
        self.layout.addWidget(self.plaintext_input)
        # 加密按钮
        self.encrypt_button = QPushButton(QIcon("encryption_icon/PrimeLock.png"), '加密文本')
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.layout.addWidget(self.encrypt_button)

        # 密文显示框
        self.ciphertext_label = QLabel('密文:')
        self.layout.addWidget(self.ciphertext_label)
        self.ciphertext_display = QTextEdit()
        self.ciphertext_display.setReadOnly(True)
        self.layout.addWidget(self.ciphertext_display)

        # 解密按钮
        self.decrypt_button = QPushButton(QIcon("encryption_icon/PrimeLockOpen.png"), '解密文本')
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.layout.addWidget(self.decrypt_button)

        # 主题切换按钮
        self.themeToggleBtn = QPushButton(QIcon("encryption_icon/dark.png"), '切换夜间模式', self)
        self.themeToggleBtn.setCheckable(True)
        self.themeToggleBtn.toggled.connect(self.toggle_theme)
        self.layout.addWidget(self.themeToggleBtn)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;   /*更深的整体背景色 */
            }
           /* 设置 QLabel 的字体大小和颜色 */
           QLabel {
               font-size: 25px;
               color: #444; /* 设置字体颜色为深灰色 */
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */
           }

           /* 设置 QLineEdit、QPushButton 和 QComboBox 的字体大小 */
           QLineEdit, QPushButton, QComboBox {
               font-size: 25px;
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */

           }

           /* 设置 QPushButton 的样式 */
           QPushButton {
               background-color: #808B96; /*#C8E9B3 按钮背景色为紫色 */
               /*color: #fff;  按钮文字颜色为白色 */
               border: 1px solid white; /* 去掉边框 */
               padding: 12px 20px; /* 设置内边距 */
               border-radius: 8px; /* 设置圆角 */
               font-family: "Arial", sans-serif
           }

           /* 鼠标悬停时的样式 */
           QPushButton:hover {
               background-color: #5e5e5e; /* 按钮背景色变暗 */
               color: white;
           }

           QTextEdit,QLineEdit{
               border: 1px solid #808B96;  /* 深紫色边框 */
           }
        """)

        self.setLayout(self.layout)

    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角

    # 设计加密模式按钮
    def toggle_key_buttons(self, text):
        if text == 'RSA':
            self.generate_rsa_keys_button.show()
            self.public_key_display.show()
            self.private_key_display.show()
            self.key_label.hide()
            self.key_input.hide()
            self.generate_key_button.hide()
        else:
            self.generate_rsa_keys_button.hide()
            self.public_key_display.hide()
            self.private_key_display.hide()
            self.key_label.show()
            self.key_input.show()
            self.generate_key_button.show()
            # self.setGeometry(800, 400, 800, 600)  # 返回AES的图片大小

    # 生成AES密钥
    def generate_key(self):
        encryption_type = self.encryption_type_combo.currentText()
        if encryption_type == 'AES':
            key_length = 32  # 默认为32字节
            key = get_random_bytes(key_length)
            self.key_input.setText(base64.b64encode(key).decode('utf-8'))

    # 生成RSA密钥
    def generate_rsa_keys(self):
        handler = EncryptionHandlerFactory.create_handler('RSA')
        private_key, public_key = handler.generate_key_pair()
        self.private_key_display.setPlainText(private_key.decode('utf-8'))
        self.public_key_display.setPlainText(public_key.decode('utf-8'))

    # 加密文本函数
    def encrypt_text(self):
        encryption_type = self.encryption_type_combo.currentText()
        handler = EncryptionHandlerFactory.create_handler(encryption_type)
        plaintext = self.plaintext_input.toPlainText()

        try:
            if encryption_type == 'AES':
                key = base64.b64decode(self.key_input.text().encode('utf-8'))
            else:
                key = self.public_key_display.toPlainText().encode('utf-8')

            ciphertext = handler.encrypt_text(key, plaintext)
            self.ciphertext_display.setPlainText(ciphertext)
        except Exception as e:
            QMessageBox.warning(self, '错误', f'加密失败: {str(e)}')

    # 界面文本函数
    def decrypt_text(self):
        encryption_type = self.encryption_type_combo.currentText()
        handler = EncryptionHandlerFactory.create_handler(encryption_type)
        ciphertext = self.ciphertext_display.toPlainText()

        try:
            if encryption_type == 'AES':
                key = base64.b64decode(self.key_input.text().encode('utf-8'))
            else:
                key = self.private_key_display.toPlainText().encode('utf-8')

            plaintext = handler.decrypt_text(key, ciphertext)
            self.plaintext_input.setPlainText(plaintext)
        except Exception as e:
            QMessageBox.warning(self, '错误', f'解密失败: {str(e)}')

    # 设置夜间模式
    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        # 设置各个控件的样式
        self.key_label.setStyleSheet("QLabel { color: white; background-color: #353535;}")  # ***
        self.generate_key_button.setStyleSheet("QPushButton {background-color: #7f8cc4;}")
        self.key_input.setStyleSheet("QLineEdit { color: white; background-color: #252525; }")
        self.encryption_type_label.setStyleSheet("QLabel { color: white; background-color: #353535;}")  # **
        self.encryption_type_combo.setStyleSheet("QComboBox { color: white; background-color: #252525; }")
        self.plaintext_label.setStyleSheet("QLabel { color: white; background-color: #353535;}")  # **
        self.plaintext_input.setStyleSheet("QTextEdit { color: white; background-color: #252525; }")
        self.encrypt_button.setStyleSheet("QPushButton { color: white; background-color: #353535; }")  # #353535
        self.ciphertext_label.setStyleSheet("QLabel { color: white; background-color: #353535;}")
        self.ciphertext_display.setStyleSheet("QTextEdit { color: white; background-color: #252525; }")
        self.decrypt_button.setStyleSheet("QPushButton { color: white; background-color: #353535; }")
        self.themeToggleBtn.setStyleSheet("QPushButton { color: white; background-color: #7f8cc4; }")
        self.generate_rsa_keys_button.setStyleSheet("QPushButton { color: white; background-color: #353535; }")
        self.public_key_display.setStyleSheet("QTextEdit { color: white; background-color: #252525; }")
        self.private_key_display.setStyleSheet("QTextEdit { color: white; background-color: #252525; }")

    # 初始化外观模式
    def set_light_mode(self):
        self.setPalette(self.style().standardPalette())

        # 重置各个控件的样式
        self.key_label.setStyleSheet("")
        self.key_input.setStyleSheet("")
        self.encryption_type_label.setStyleSheet("")
        self.encryption_type_combo.setStyleSheet("")
        self.plaintext_label.setStyleSheet("")
        self.plaintext_input.setStyleSheet("")
        self.encrypt_button.setStyleSheet("")
        self.ciphertext_label.setStyleSheet("")
        self.ciphertext_display.setStyleSheet("")
        self.decrypt_button.setStyleSheet("")
        self.themeToggleBtn.setStyleSheet("")
        self.generate_rsa_keys_button.setStyleSheet("")
        self.public_key_display.setStyleSheet("")
        self.private_key_display.setStyleSheet("")

    # 切换白天夜间模式
    def toggle_theme(self, checked):
        if checked:
            self.set_dark_mode()
            self.themeToggleBtn.setText('切换白天模式')
        else:
            self.set_light_mode()
            self.themeToggleBtn.setText('切换夜间模式')


# 子系统测试

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EncryptDecryptApp()
    ex.show()
    sys.exit(app.exec_())
