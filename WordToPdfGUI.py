import os
import sys
import warnings

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, \
    QMessageBox, QLabel, QTextEdit, QProgressBar, QGridLayout, QDesktopWidget, QHBoxLayout

from fileFactory import FileConverterFactory  # 确保这个文件与工厂类代码在同一目录

# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


class WordToPDFGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央
        self.setWindowIcon(QIcon('process_icon/conversion.png'))  # 设置窗口图标

        self.input_path_edit = QLineEdit(self)
        self.input_path_edit.setPlaceholderText('输入文件或文件夹路径')
        layout.addWidget(self.input_path_edit)

        self.output_path_edit = QLineEdit(self)
        self.output_path_edit.setPlaceholderText('输出文件夹路径')
        layout.addWidget(self.output_path_edit)
        # ------------------------------拖拽--------------------------
        # 输入拖拽按钮
        self.input_drag_button = QPushButton(QIcon('process_icon/drag.png'), '拖拽输入图片或图片文件夹到此')
        self.input_drag_button.setStyleSheet("""
                  QPushButton {
                      font-size: 25px;
                      border: 2px dashed #808B96;
                      padding: 20px;
                  }
                  QPushButton:hover {
                      background-color: #e6e6fa;
                      color: #ea580c;
                  }
              """)

        self.input_drag_button.setAcceptDrops(True)
        # 输出拖拽按钮
        self.output_drag_button = QPushButton(QIcon('process_icon/folder.png'), '拖拽输出压缩图片文件夹到此处')
        self.output_drag_button.setStyleSheet("""
                         QPushButton {
                             font-size: 25px;
                             border: 2px dashed #808B96;
                             padding: 20px;
                         }
                         QPushButton:hover {
                             background-color: #e6e6fa;
                             color: #ea580c;
                         }
                     """)
        self.output_drag_button.setAcceptDrops(True)
        # ------------------------拖拽-----------------------
        # ---------------------------------------------------------
        drag_grid_layout = QGridLayout()  # 创建网格布局,把这两个拖拽按钮保持水平

        input_drag_layout = QHBoxLayout()
        input_drag_layout.addWidget(self.input_drag_button)
        drag_grid_layout.addLayout(input_drag_layout, 0, 0)

        output_drag_layout = QHBoxLayout()
        output_drag_layout.addWidget(self.output_drag_button)
        drag_grid_layout.addLayout(output_drag_layout, 0, 1)

        layout.addLayout(drag_grid_layout)  # 直接添加布局对象而不
        # --------------------------------------------------
        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)  # 设置进度条文本居中显示
        layout.addWidget(self.progress_bar)

        # 识别结果
        self.result_label = QLabel('识别结果:')
        self.result_textedit = QTextEdit()
        self.result_textedit.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_textedit)

        # 按钮连接槽函数
        button_grid_layout = QGridLayout()  # 创建网格布局

        browse_input_file_button = QPushButton(QIcon("process_icon/input_file.png"), '浏览输入文件', self)
        browse_input_file_button.clicked.connect(self.browse_input_file)
        button_grid_layout.addWidget(browse_input_file_button, 0, 0)  # 将按钮添加到网格布局的第一行第一列

        browse_input_folder_button = QPushButton(QIcon("process_icon/find_file.png"), '浏览输入文件夹', self)
        browse_input_folder_button.clicked.connect(self.browse_input_folder)
        button_grid_layout.addWidget(browse_input_folder_button, 0, 1)  # 将按钮添加到网格布局的第一行第二列

        browse_output_button = QPushButton(QIcon("process_icon/output_file.png"), '浏览输出路径', self)
        browse_output_button.clicked.connect(self.browse_output)
        button_grid_layout.addWidget(browse_output_button, 1, 0)  # 将按钮添加到网格布局的第二行第一列

        convert_button = QPushButton(QIcon("process_icon/convert.png"), 'docx->pdf文件', self)
        convert_button.clicked.connect(self.convert)
        button_grid_layout.addWidget(convert_button, 1, 1)  # 将按钮添加到网格布局的第二行第二列

        layout.addLayout(button_grid_layout)  # 将网格布局添加到主布局

        self.setLayout(layout)
        self.setWindowTitle('Word 转 PDF 转换器')
        # 设置样式表
        self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f5;   /* 更深的整体背景色 */
                }
                QLabel {
                    font-size: 25px;
                    color: #444;  /* 深一些的文字颜色 */
                    font-family: "Arial", sans-serif;
                }
                QLineEdit, QPushButton, QComboBox {
                    font-size: 25px;
                    font-family: "Arial", sans-serif;
                    padding: 10px;  /* 增大组件的内边距 */
                    margin: 10px;  /* 增大组件之间的间隙 */
                }
                QPushButton {
                    background-color: #e6e6fa; /* 深紫色背景 */
                    border: 1px solid #808B96;   /* 深紫色边框 */
                    padding: 15px 25px;  /* 增大按钮的内边距 */
                    border-radius: 8px;
                    font-family: "Arial", sans-serif;
                }
                QPushButton:hover {
                    background-color: #4527a0;  /* 更深的深紫色背景 */
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #4527a0;  /* 最深的深紫色背景 */
                    color: white;
                }
                QProgressBar {
                    text-align: center;
                    font-size: 18px;
                    border: 1px solid #808B96;  /* 深紫色边框 */
                    border-radius: 5px;
                    background-color: #EEEEEE;  /* 深紫色背景 */
                    padding: 10px;  /* 增大进度条的内边距 */
                    margin: 10px;  /* 增大组件之间的间隙 */
                }
                QProgressBar::chunk {
                    background-color: #28a745;  /* 绿色进度 */
                    width: 20px;
                }
                QTextEdit {
                 border: 1px solid #808B96;  /* 深紫色边框 */
                 padding: 10px;  /* 增大 QTextEdit 的内边距 */
                 margin: 10px;  /* 增大组件之间的间隙 */
                 min-height: 50px;  /* 减小 QTextEdit 的高度 */
                }
                QLineEdit {
                 border: 1px solid #808B96;  /* 深紫色边框 */
                 padding: 10px;  /* 增大 QLineEdit 的内边距 */
                 margin: 10px;  /* 增大组件之间的间隙 */
                }
        """)

        # 使窗口接受拖拽
        self.setAcceptDrops(True)

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
                    self.input_path_edit.setText(file_path)
                else:
                    if file_path.endswith(('.docx', '.doc')):
                        self.input_path_edit.setText(file_path)
                    else:
                        self.input_path_edit.setText('请拖拽文件')
            elif self.output_drag_button.geometry().contains(cursor_pos):
                if os.path.isdir(file_path):
                    self.output_path_edit.setText(file_path)
                else:
                    self.output_path_edit.setText('请拖拽文件夹')
        else:
            event.ignore()

    # 确保界面保存到屏幕中间
    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角

    # 浏览输入文件
    def browse_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 Word 文件", "", "Word 文件 (*.docx);;所有文件 (*)",
                                                   options=options)
        if file_path:
            self.input_path_edit.setText(file_path)
            self.progress_bar.setValue(0)  # 清零进度条
            self.update_progress(0)

    # 浏览输入文件夹
    def browse_input_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "选择输入文件夹", options=options)
        if directory:
            self.input_path_edit.setText(directory)
            self.progress_bar.setValue(0)  # 清零进度条
            self.update_progress(0)  # 清空进度条的数字

    # 浏览输出文件夹
    def browse_output(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "选择输出文件夹", options=options)
        if directory:
            self.output_path_edit.setText(directory)

    # 转化方法
    def convert(self):
        input_path = self.input_path_edit.text()
        output_path = self.output_path_edit.text()
        # 将文件输入输出地址正常化，防止出错
        input_file_path = os.path.abspath(input_path)
        input_file_path = os.path.normpath(input_file_path)
        output_file_path = os.path.abspath(output_path)  # 获取绝对路径
        output_file_path = os.path.normpath(output_file_path)  # 标准化路径格式
        if not input_path or not output_path:
            QMessageBox.warning(self, "警告", "请输入有效的输入路径和输出路径")
            return

        converter = FileConverterFactory.create_converter('word_to_pdf', os.cpu_count(),
                                                          progress_callback=self.update_progress)
        try:
            output_paths = converter.judge_single_folder(input_file_path, output_file_path)
            self.display_result(output_paths)
            QMessageBox.information(self, "成功", "文件已成功转换")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"转换失败: {str(e)}")

    # 更新进度条
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"{value}%")  # 在进度条中间显示进度

    # 显示结果
    def display_result(self, path_list):  # 将识别结果列表连接成一个文本
        path_text = "\n".join([f"保存路径: {path}" for path in path_list])
        self.result_textedit.setText(path_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordToPDFGUI()
    ex.show()
    sys.exit(app.exec_())
