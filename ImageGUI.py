import ctypes
import sys
import warnings

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QDesktopWidget
)

# 导入三个GUI类 组合实现一个子系统类
from ImageCompressorGUI import ImageCompressorGUI
from ImageConverterGUI import ImageConverterGUI
from ImageOCRGUI import ImageOCRGUI

# 设置应用程序 ID
appId = "ID"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


# 子系统GUI类 图片处理类
class imageGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图片处理工具')
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央

        # 设置窗口图标
        self.setWindowIcon(QIcon('image_icon/icon.png'))  # 请确保icon.png存在于程序目录下

        # 创建一个中央Widget，并设置一个垂直布局
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        # 创建一个QTabWidget并添加到布局中
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.setCentralWidget(centralWidget)

        # 添加标签页
        self.tabs.addTab(ImageConverterGUI(), QIcon("image_icon/transFile.png"), '图片格式转换')
        self.tabs.addTab(ImageCompressorGUI(), QIcon("image_icon/compressor_image.png"), '图片压缩')
        self.tabs.addTab(ImageOCRGUI(), QIcon("image_icon/ocr.png"), '图片OCR提取')

        # 设置样式表
        self.tabs.setStyleSheet("""
            QTabWidget {
                font-size: 25px;
                color: #555; /* 设置字体颜色为深灰色 */
                font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */

            }
            QTabBar::tab {
                background: #F5F5F5; /* 设置标签的背景色 */
                border: 1px solid #DDDDDD; /* 设置标签的边框 */
                padding: 10px; /* 设置标签的内边距 */
                margin: 2;  /*设置标签的左右外边距
                border-radius: 4px; /* 设置标签的圆角 */
            }
            QTabBar::tab:selected {
                background: #DDDDDD; /* 设置选中标签的背景色 */
                border-color: #AAA; /* 设置选中标签的边框颜色 */
            }
            QTabBar::tab:hover {
                background: #DDDDDD; /* 设置鼠标悬停标签的背景色 */
            }
            QTabBar::tab {
                /* 添加阴影效果 */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); 
            }
        """)

    # 将界面放到屏幕的中心
    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # print(multiThreaded.get_is_multi())
    mainGUI = imageGUI()
    mainGUI.show()
    sys.exit(app.exec_())
