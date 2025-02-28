import os
import sys
import warnings

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QHBoxLayout, QMessageBox, QApplication, QFileDialog, QTextEdit, QDesktopWidget
)
from PyQt5.QtGui import QIcon, QDropEvent
from ImageFactory import imageFactory

# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class ImageConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # 初始化UI类
    def initUI(self):
        self.setWindowTitle('图片格式转换工具')
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央

        self.setWindowIcon(QIcon('image_icon/icon.png'))  # 设置窗口图标

        layout = QVBoxLayout()
        layout.setSpacing(20)  # 设置部件之间的间距

        # 输入文件部分
        self.input_file_label = QLabel('输入图片:')
        self.input_file_path = QLineEdit()
        self.input_file_path.setPlaceholderText('请拖拽图片或者点击选择图片')
        self.input_file_button = QPushButton(QIcon('image_icon/input_file.png'), '选择')
        self.input_file_button.clicked.connect(self.select_input_file)

        # 输入文件夹部分
        self.input_label = QLabel('输入文件夹:')
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText('请拖拽文件夹或者点击选择文件夹')
        self.input_button = QPushButton(QIcon('image_icon/find_file.png'), '选择')
        self.input_button.clicked.connect(self.select_input_folder)

        # 输出文件夹部分
        self.output_label = QLabel('输出文件夹:')
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText('请拖拽文件夹或者点击选择文件夹')
        self.output_button = QPushButton(QIcon('image_icon/output_file.png'), '选择')
        self.output_button.clicked.connect(self.select_output_folder)

        # 图片格式部分
        self.format_label = QLabel('图片格式:')
        self.image_format = QComboBox()
        self.image_format.addItems(['jpeg', 'png', 'gif', 'bmp', 'jpg', 'tiff', 'ppm', 'ico', 'webp'])

        # 开始转换按钮
        self.convert_button = QPushButton(QIcon('image_icon/convert.png'), '开始转换')
        self.convert_button.clicked.connect(self.start_conversion)

        # 识别结果
        self.result_label = QLabel('识别结果:')
        self.result_textedit = QTextEdit()
        self.result_textedit.setReadOnly(True)

        # 设置样式表
        self.setStyleSheet("""
           /* 设置 QLabel 的字体大小和颜色 */
           QLabel {
               font-size: 25px;
               color: #555; /* 设置字体颜色为深灰色 */
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */
           }

           /* 设置 QLineEdit、QPushButton 和 QComboBox 的字体大小 */
           QLineEdit, QPushButton, QComboBox {
               font-size: 25px;
               font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */
               border: 1px solid #808B96;   /*深紫色边框 */
           }

           /* 设置 QPushButton 的样式 */
           QPushButton {
               background-color: #e6e6fa; /* 按钮背景色为紫色 */
               color: black; /* 按钮文字颜色为白色 */
               border: 1px solid #808B96;   /*深紫色边框 */
               padding: 8px 12px;  /*设置内边距 */
               border-radius: 8px; /* 设置圆角 */
               font-family: "Arial", sans-serif
           }

           /* 鼠标悬停时的样式 */
           QPushButton:hover {
               background-color: #6a1b9a; /* 按钮背景色变暗 */
               color: white; /* 按钮文字颜色为白色 */
           }

           /* 按钮被按下时的样式 */
           QPushButton:pressed {
               background-color: #4a148c; /* 按钮背景色变更深 */
           }
        """)

        # 将部件添加到布局中
        layout.addWidget(self.input_file_label)
        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(self.input_file_path)
        input_file_layout.addWidget(self.input_file_button)
        layout.addLayout(input_file_layout)

        layout.addWidget(self.input_label)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(self.input_button)
        layout.addLayout(input_layout)

        layout.addWidget(self.output_label)
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.output_button)
        layout.addLayout(output_layout)

        layout.addWidget(self.format_label)
        layout.addWidget(self.image_format)
        layout.addWidget(self.convert_button)

        layout.addWidget(self.result_label)
        layout.addWidget(self.result_textedit)

        self.setLayout(layout)

        # 使窗口接受拖拽
        self.setAcceptDrops(True)

    # 确保文件界面为中间
    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角

    # 检查拖拽内容是否包含URL格式（文件路径）
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    # 处理拖拽事件，提取文件路径并显示在输入框中
    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            url = mime_data.urls()[0]
            file_path = url.toLocalFile()

            cursor_pos = event.pos()
            if self.input_path.geometry().contains(cursor_pos):
                if os.path.isdir(file_path):
                    self.input_path.setText(file_path)
                    self.input_file_path.clear()
                    self.input_file_path.setReadOnly(True)
                else:
                    self.input_path.setPlaceholderText('请拖拽文件夹')
            elif self.output_path.geometry().contains(cursor_pos):
                if os.path.isdir(file_path):
                    self.output_path.setText(file_path)
                else:
                    self.output_path.setPlaceholderText('请拖拽文件夹')
            else:
                if file_path.endswith(
                        ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.ppm', '.ico', '.webp')):
                    self.input_file_path.setText(file_path)
                    self.input_path.clear()
                    self.input_path.setReadOnly(True)
                else:
                    self.input_file_path.setPlaceholderText('请拖拽图片文件')
        else:
            event.ignore()

    # 选择输入文件
    def select_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, '选择输入文件')
        if file:
            self.input_file_path.setText(file)
            # 禁用选择文件夹按钮,同时清空选择文件夹的文件地址,同时确保文件夹输入地址无法输入
            self.input_button.setEnabled(False)
            self.input_path.clear()
            self.input_path.setReadOnly(True)

        # 选择输入文件夹

    # 选择输入文件夹
    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输入文件夹')
        if folder:
            self.input_path.setText(folder)
            # 禁用选择文件按钮,同时清空选择文件的文件地址,同时确保文件输入地址无法输入
            self.input_file_button.setEnabled(False)
            self.input_file_path.clear()
            self.input_file_path.setReadOnly(True)

    # 选择输出文件夹
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if folder:
            self.output_path.setText(folder)

    # 开始图片格式转换
    def start_conversion(self):
        inp_file_path = self.input_file_path.text()
        inp_folder_path = self.input_path.text()
        out_path = self.output_path.text()
        image_format = self.image_format.currentText()

        if not out_path or not image_format:
            QMessageBox.critical(self, '错误', '所有字段都是必填的')
            return
        # 当开始转化的时候禁用按钮和输入框

        self.input_file_path.setReadOnly(True)
        self.input_path.setReadOnly(True)
        self.output_path.setReadOnly(True)
        self.convert_button.setEnabled(False)
        self.input_file_button.setEnabled(False)
        self.input_button.setEnabled(False)
        self.output_button.setEnabled(False)
        converter = imageFactory.create_image_factory('格式转化')
        try:
            if inp_file_path:
                output_paths = converter.imageProcess(inp_file_path, out_path, image_format)
            elif inp_folder_path:
                output_paths = converter.imageProcess(inp_folder_path, out_path, image_format)
            else:
                QMessageBox.critical(self, '错误', '必须选择输入文件或输入文件夹')
                return
            self.display_result(output_paths)  # 调用 display_result 方法，显示转换结果
            QMessageBox.information(self, '成功', '图片格式转换完成')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'转换过程中发生错误: {e}')
        finally:
            # 恢复按钮和输入框状态
            self.input_file_path.setReadOnly(False)
            self.input_path.setReadOnly(False)
            self.output_path.setReadOnly(False)
            self.convert_button.setEnabled(True)
            self.input_file_button.setEnabled(True)
            self.input_button.setEnabled(True)
            self.output_button.setEnabled(True)

    # 显示结果
    def display_result(self, path_list):  # 将识别结果列表连接成一个文本
        path_text = "\n".join([f"保存路径: {path}" for path in path_list])
        self.result_textedit.setText(path_text + "\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverterGUI()
    ex.show()
    sys.exit(app.exec_())
