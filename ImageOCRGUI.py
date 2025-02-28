import os
import sys
import warnings

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QHBoxLayout, \
    QFileDialog, QMessageBox, QApplication, QGridLayout, QDesktopWidget

from ImageFactory import imageFactory

# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class ImageOCRGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图片OCR识别工具')
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央
        self.setWindowIcon(QIcon('image_icon/icon.png'))

        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.input_label = QLabel('输入文件/文件夹:')
        self.input_path = QLineEdit()
        self.input_button = QPushButton(QIcon('image_icon/find_file.png'), '选择')
        self.input_button.clicked.connect(self.select_input)
        # ------------------------------拖拽--------------------------
        # 输入拖拽按钮
        self.input_drag_button = QPushButton(QIcon('image_icon/drag.png'), '拖拽输入图片或图片文件夹到此')
        self.input_drag_button.setStyleSheet("""
                    QPushButton {
                        font-size: 25px;
                        border: 2px dashed #6a1b9a;
                        padding: 20px;
                    }
                    QPushButton:hover {
                        background-color: #e6e6fa;
                        color: #ea580c;
                    }
                """)

        self.input_drag_button.setAcceptDrops(True)
        # 输出拖拽按钮
        self.output_drag_button = QPushButton(QIcon('image_icon/folder.png'), '拖拽输出压缩图片文件夹到此处')
        self.output_drag_button.setStyleSheet("""
                           QPushButton {
                               font-size: 25px;
                               border: 2px dashed #6a1b9a;
                               padding: 20px;
                           }
                           QPushButton:hover {
                               background-color: #e6e6fa;
                               color: #ea580c;
                           }
                       """)
        self.output_drag_button.setAcceptDrops(True)
        # ------------------------拖拽-----------------------

        self.output_label = QLabel('输出文件夹:')
        self.output_path = QLineEdit()
        self.output_button = QPushButton(QIcon('image_icon/output_file.png'), '选择')
        self.output_button.clicked.connect(self.select_output_folder)

        self.language_label = QLabel('识别语言:')
        self.language_combobox = QComboBox()
        self.language_combobox.addItems(['chi_sim', 'eng'])

        self.ocr_button = QPushButton(QIcon('image_icon/convert.png'), '开始识别')
        self.ocr_button.clicked.connect(self.start_ocr)

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
        # ---------------------------------------
        button_grid_layout = QGridLayout()  # 创建网格布局,把这两个拖拽按钮保持水平

        input_drag_layout = QHBoxLayout()
        input_drag_layout.addWidget(self.input_drag_button)
        button_grid_layout.addLayout(input_drag_layout, 0, 0)

        output_drag_layout = QHBoxLayout()
        output_drag_layout.addWidget(self.output_drag_button)
        button_grid_layout.addLayout(output_drag_layout, 0, 1)

        layout.addLayout(button_grid_layout)  # 直接添加布局对象而不是使用addWidget()函数
        # ----------------------------------------
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combobox)

        layout.addWidget(self.ocr_button)

        layout.addWidget(self.result_label)
        layout.addWidget(self.result_textedit)

        self.setLayout(layout)
        # 使窗口接受拖拽
        self.setAcceptDrops(True)

    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角

    def dragEnterEvent(self, event):
        # 检查拖拽内容是否包含URL格式（文件路径）
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 处理拖拽事件，提取文件路径并显示在输入框中
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            url = mime_data.urls()[0]
            file_path = url.toLocalFile()

            cursor_pos = event.pos()
            if self.input_drag_button.geometry().contains(cursor_pos):
                if os.path.isdir(file_path):
                    self.input_path.setText(file_path)
                else:
                    if file_path.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.ppm', '.ico', '.webp')):
                        self.input_path.setText(file_path)
                    else:
                        self.input_path.setText('请拖拽图片')
            elif self.output_drag_button.geometry().contains(cursor_pos):
                if os.path.isdir(file_path):
                    self.output_path.setText(file_path)
                else:
                    self.output_path.setText('请拖拽文件夹')
        else:
            event.ignore()

    def select_input(self):
        path, _ = (QFileDialog.getOpenFileName(self, '选择输入文件/文件夹')
                   or QFileDialog.getExistingDirectory(self, '选择输入文件/文件夹'))
        if path:
            self.input_path.setText(path)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if folder:
            self.output_path.setText(folder)

    def start_ocr(self):
        input_path = self.input_path.text()
        output_path = self.output_path.text()
        language = self.language_combobox.currentText()

        if not input_path or not output_path:
            QMessageBox.critical(self, '错误', '输入和输出路径都是必填的')
            return

        ocr = imageFactory.create_image_factory('OCR提取')
        try:
            word_list, path_list = ocr.imageProcess(input_path, output_path, language)
            self.display_result(word_list, path_list)
            QMessageBox.information(self, '成功', '图片OCR识别完成')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'识别过程中发生错误: {e}')

    def display_result(self, word_list, path_list):
        if len(path_list):  # 判断输入为一个文件的话
            result_text = "\n".join([f"识别结果:{word}" for word in word_list])  # 将识别结果列表连接成一个文本
            path_text = "\n".join([f"保存路径: {path}" for path in path_list])
            self.result_textedit.setText(result_text + "\n" + path_text)
        else:
            for file_list, address_list in zip(word_list, path_list):
                result_text = "\n".join([f"识别结果:{word}" for word in file_list])  # 将识别结果列表连接成一个文本
                path_text = "\n".join([f"保存路径: {path}" for path in address_list])
                self.result_textedit.setText(result_text + "\n" + path_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageOCRGUI()
    ex.show()
    sys.exit(app.exec_())
