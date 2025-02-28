import ctypes
import sys
import warnings
import qrcode
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, \
    QLineEdit, QMessageBox, QComboBox, QSpinBox, QGridLayout, QDesktopWidget
from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
from io import BytesIO
from QrCodeFactory import QRCodeFactory  # 导入二维码工厂类

'''
GUI类 调用二维码工厂类 实现接口
'''
# 设置应用程序 ID
appId = "ID"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class QrGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('二维码生成器')
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央
        self.setWindowIcon(QIcon('qr_icon/QR.png'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.defaultPixmap = QPixmap('qr_icon/defaultQR.png')  # 使用一个默认图片名为default_image.png占住生成QRCode的位置
        self.label.setPixmap(
            self.defaultPixmap.scaled(self.label.size() * 5, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.label)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("输入文本或URL")
        self.layout.addWidget(self.text_input)
        # -----------------*------------------------
        button_grid_layout = QGridLayout()  # 创建网格布局

        self.version_input = QSpinBox(self)
        self.version_input.setRange(1, 40)
        self.version_input.setValue(1)
        self.version_input.setPrefix("版本: ")
        self.layout.addWidget(self.version_input)
        button_grid_layout.addWidget(self.version_input, 0, 0)  # 将按钮添加到网格布局的第一行第一列

        self.error_correction_input = QComboBox(self)
        self.error_correction_input.addItems([
            "低 (7%)", "中等 (15%)", "高 (25%)", "最高 (30%)"
        ])
        self.layout.addWidget(self.error_correction_input)
        button_grid_layout.addWidget(self.error_correction_input, 0, 1)  # 将按钮添加到网格布局的第一行第一列

        self.box_size_input = QSpinBox(self)
        self.box_size_input.setRange(1, 20)
        self.box_size_input.setValue(17)
        self.box_size_input.setPrefix("方块大小: ")
        self.layout.addWidget(self.box_size_input)
        button_grid_layout.addWidget(self.box_size_input, 1, 0)  # 将按钮添加到网格布局的第二行第一列

        self.border_input = QSpinBox(self)
        self.border_input.setRange(1, 10)
        self.border_input.setValue(3)
        self.border_input.setPrefix("边框: ")
        self.layout.addWidget(self.border_input)
        button_grid_layout.addWidget(self.border_input, 1, 1)  # 将按钮添加到网格布局的第二行第二列

        # -------------------------------*----------------------
        self.btnGenerate = QPushButton(QIcon('qr_icon/CreateQR.png'), '生成二维码', self)
        self.btnGenerate.clicked.connect(self.generate_qr_code)
        self.layout.addWidget(self.btnGenerate)
        button_grid_layout.addWidget(self.btnGenerate, 2, 0)  # 将按钮添加到网格布局的第三行第一列

        self.btnSave = QPushButton(QIcon('qr_icon/SaveQR.png'), '保存二维码', self)
        self.btnSave.clicked.connect(self.save_qr_code)
        self.layout.addWidget(self.btnSave)
        button_grid_layout.addWidget(self.btnSave, 2, 1)  # 将按钮添加到网格布局的第三行第二列
        self.layout.addLayout(button_grid_layout)  # 将网格布局添加到主布局

        self.themeToggleBtn = QPushButton(QIcon('qr_icon/changeAppearance.png'), '切换夜间模式', self)
        self.themeToggleBtn.setCheckable(True)
        self.themeToggleBtn.toggled.connect(self.toggle_theme)
        self.layout.addWidget(self.themeToggleBtn)
        # 设置样式表
        self.setStyleSheet("""
           /* 设置主窗口的背景色和组件之间的间距 */
           QWidget {
               background-color: #f5f5f5; /* 设置背景色为浅灰色 */
               padding: 20px; /* 设置内边距 */
               margin: 10px; /* 设置外边距 */
           }

           /* 设置 QLabel 的字体大小和颜色 */
           QLabel {
               font-size: 25px;
               color: #fff; /* 设置字体颜色为深灰色 */
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */
               border: 1px solid #808B96;   /* 深紫色边框 */
               border-radius: 18px; /* 设置圆角 */
               padding: 5px; /* 增加内边距 */
               margin: 5px 0; /* 增加外边距，上下间距 */
           }

           /* 设置 QLineEdit、QPushButton 和 QComboBox 的字体大小 */
           QLineEdit, QPushButton, QComboBox, QSpinBox {
               font-size: 26px;
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */
               border: 1px solid #808B96;   /* 浅紫色边框 */
               padding: 5px; /* 增加内边距 */
               margin: 5px 0; /* 增加外边距，上下间距 */
           }

           /* 设置 QLineEdit 的样式 */
           QLineEdit {
               background-color: #fff; /* 设置背景色为白色 */
               border-radius: 8px; /* 设置圆角 */
           }

           /* 设置 QPushButton 的样式 */
           QPushButton {
               background-color: #808B96; /* 按钮背景色为浅灰色 */
               color: white; /* 按钮文字颜色为白色 */
               border: 1px solid #E49BFF;   /*浅灰色边框 */
               padding: 15px 15px; /* 设置内边距 */
               border-radius: 8px; /* 设置圆角 */
               font-family: "Arial", sans-serif;
               margin: 5px 0; /* 增加外边距，上下间距 */
           }

           /* 鼠标悬停时的样式 */
           QPushButton:hover {
               color: black;
               background-color: #E0E0E0; /* 按钮背景色变暗 */
           }

           /* 按钮被按下时的样式 */
           QPushButton:pressed {
               background-color: #E0E0E0; /* 按钮背景色变更深 */
           }

           /* 设置 QComboBox 的样式 */
           QComboBox {
               background-color: #fff; /* 设置背景色为白色 */
               border-radius: 8px; /* 设置圆角 */
           }

           /* 设置 QSpinBox 的样式 */
           QSpinBox {
               background-color: #fff; /* 设置背景色为白色 */
               border-radius: 8px; /* 设置圆角 */
           }
        """)

    # 将界面放到屏幕的中心
    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角

    # 二维码容错率函数
    def get_error_correction(self, selection):
        error_correction_map = {
            "低 (7%)": qrcode.constants.ERROR_CORRECT_L,
            "中等 (15%)": qrcode.constants.ERROR_CORRECT_M,
            "高 (25%)": qrcode.constants.ERROR_CORRECT_Q,
            "最高 (30%)": qrcode.constants.ERROR_CORRECT_H
        }
        return error_correction_map.get(selection, qrcode.constants.ERROR_CORRECT_L)

    # 生成二维码函数，调用工厂类生成二维码函数
    def generate_qr_code(self):
        data = self.text_input.text()
        version = self.version_input.value()
        error_correction = self.get_error_correction(self.error_correction_input.currentText())
        box_size = self.box_size_input.value()
        border = self.border_input.value()

        if data:
            qr_generator = QRCodeFactory.create_qr_generator(
                data_text=data,
                version=version,
                error_correction=error_correction,
                box_size=box_size,
                border=border
            )
            img = qr_generator.generate_qr()

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qimage = QPixmap()
            qimage.loadFromData(buffer.getvalue())
            self.label.setPixmap(qimage)
        else:
            QMessageBox.warning(self, "警告", "请输入文本或URL以生成二维码")

    # 保存二维码函数，使用pyqt5默认的文件保存函数
    def save_qr_code(self):
        if not self.label.pixmap():
            QMessageBox.warning(self, "警告", "请先生成二维码")
            return
        options = QFileDialog.Options()
        default_filename = "my_qr_code.png"
        file_path, _ = QFileDialog.getSaveFileName(self, "保存二维码", default_filename,
                                                   "PNG Files (*.png);;All Files (*)",
                                                   options=options)
        if file_path:
            self.label.pixmap().save(file_path)
            QMessageBox.information(self, "成功", f"二维码已保存到: {file_path}")

    # 切换主题
    def toggle_theme(self, checked):
        if checked:
            self.set_dark_mode()
            self.themeToggleBtn.setText('切换白天模式')
        else:
            self.set_light_mode()
            self.themeToggleBtn.setText('切换夜间模式')

    # 设置暗夜模式
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
        self.central_widget.setStyleSheet("QWidget { background-color: #353535; }")
        self.label.setStyleSheet("QLabel { color: white; border: 1px solid white;}")
        self.text_input.setStyleSheet("QLineEdit { color: white; background-color: #252525; border: 1px solid white;}")
        self.error_correction_input.setStyleSheet(
            "QComboBox {color: white; background-color: #353535; border: 1px solid white; }")
        self.version_input.setStyleSheet(
            "QSpinBox {color: white; background-color: #353535; border: 1px solid white;}")
        self.box_size_input.setStyleSheet(
            "QSpinBox {color: white; background-color: #353535; border: 1px solid white;}")
        self.border_input.setStyleSheet("QSpinBox { color: white; background-color: #353535; border: 1px solid white;}")
        self.btnGenerate.setStyleSheet("QPushButton { color: white; background-color: #353535; }")
        self.btnSave.setStyleSheet("QPushButton { color: white; background-color: #353535; border: 1px solid #FFFFFF;}")
        # **
        self.btnGenerate.setStyleSheet(
            "QPushButton { color: white; background-color: #353535; border: 1px solid #FFFFFF;}")
        self.themeToggleBtn.setStyleSheet(
            "QPushButton { color: white; background-color: #353535; border: 1px solid #FFFFFF;}")
        # **
        # self.themeToggleBtn.setStyleSheet("QPushButton { color: white; background-color: #353535; }")

    # 设置白日模式
    def set_light_mode(self):
        self.setPalette(self.style().standardPalette())

        # 重置各个控件的样式
        self.central_widget.setStyleSheet("")
        self.label.setStyleSheet("")
        self.text_input.setStyleSheet("")
        self.error_correction_input.setStyleSheet("")
        self.version_input.setStyleSheet("")
        self.box_size_input.setStyleSheet("")
        self.border_input.setStyleSheet("")
        self.btnGenerate.setStyleSheet("")
        self.btnSave.setStyleSheet("")
        self.themeToggleBtn.setStyleSheet("")


# 子系统测试
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QrGUI()
    mainWindow.show()
    sys.exit(app.exec_())
