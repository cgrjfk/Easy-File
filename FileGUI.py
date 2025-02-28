import ctypes
import sys
import warnings

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QDesktopWidget
)
# 导入两个GUI类 组合实现一个子系统类
from PdfToWordGUI import PDFToWordGUI
from WordToPdfGUI import WordToPDFGUI
from ControlThreaded import ControlThreaded  # 导入控制是否开启多线程的控制类

# 设置应用程序 ID
appId = "ID"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


# 子系统GUI类 图片处理类
class FileGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件处理工具')
        self.resize(1300, 950)  # 设置窗口的宽度和高度
        self.center()  # 将窗口放置在屏幕中央

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(PDFToWordGUI(), QIcon("process_icon/word.png"), 'pdf转docx文档')
        self.tabs.addTab(WordToPDFGUI(), QIcon("process_icon/pdf.png"), 'docx转pdf文档')

        self.setWindowIcon(QIcon('process_icon/conversion.png'))
        # 设置样式表
        self.tabs.setStyleSheet("""
            QTabWidget {
                font-size: 25px;
                color: #555; /* 设置字体颜色为深灰色 */
                font-family: "Arial", sans-serif; /* 设置字体为Arial或者sans-serif字体 */

            }
            QTabBar::tab {
                background: #F5F5F5; /* 设置标签的背景色 */
                border: 1px solid #CCC; /* 设置标签的边框 */
                padding: 10px; /* 设置标签的内边距 */
                margin: 2px; /* 设置标签的外边距 */
                border-radius: 4px; /* 设置标签的圆角 */

            }
            QTabBar::tab:selected {
                background: #DDD; /* 设置选中标签的背景色 */
                border-color: #AAA; /* 设置选中标签的边框颜色 */
            }
            QTabBar::tab:hover {
                background: #EAEAEA; /* 设置鼠标悬停标签的背景色 */
            }
            QTabBar::tab {
                /* 添加阴影效果 */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); 
            }
        """)

    def center(self):
        qr = self.frameGeometry()  # 获取窗口的框架几何图形
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 将窗口的框架几何图形移动到屏幕中心
        self.move(qr.topLeft())  # 将窗口移动到框架几何图形的左上角


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # print(multiThreaded.get_is_multi())
    mainGUI = FileGUI()
    mainGUI.show()
    sys.exit(app.exec_())
