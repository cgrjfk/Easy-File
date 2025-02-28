import ctypes
import sys
import warnings
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QTabWidget, QPushButton, QHBoxLayout, \
    QMainWindow, QDesktopWidget, QTextEdit, QSystemTrayIcon, QMenu, QAction

from ImageGUI import imageGUI
from FileGUI import FileGUI
from EncryptionGUI import EncryptDecryptApp
from QRGUI import QrGUI

# 设置应用程序 ID
appId = "ID"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
# 忽略DeprecationWarning警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


# 主GUI类 调用子系统的GUI合并到主GUI类中
class MainFacade(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_button = self.create_button('icon/home.png', '主界面')
        self.image_button = self.create_button('icon/image.png', '图片处理')
        self.file_button = self.create_button('icon/file.png', '文件转换')
        self.encryption_button = self.create_button('icon/encryption.png', '文本加密')
        self.qr_button = self.create_button('icon/QR.png', '二维码生成')

        self.main_tab = self.create_main_tab()  # 创建主界面标签页
        self.image_tab = imageGUI()
        self.file_tab = FileGUI()
        self.encryption_tab = EncryptDecryptApp()
        self.qr_tab = QrGUI()
        self.right_widget = QTabWidget()

        self.initUI()  # 初始化UI

    def create_button(self, icon_path, text):
        button = QPushButton(QIcon(icon_path), text, self)
        button.setStyleSheet("""
            QPushButton {
                background-color: ; 
                color: black;
                border: 1px solid white; 
                padding: 10px 20px;
                text-align: left;
                font-size: 25px;
                margin: 4px 2px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D3D3D3; /* 悬停时的背景颜色 */
                color: #b91c1c; /* 悬停时的文字颜色 */
            }
            QPushButton:pressed {
                background-color: #D3D3D3; 
                color: #b91c1c; 
            }
        """)

        return button

    def create_main_tab(self):
        layout = QVBoxLayout()

        # 添加图片
        image_label = QLabel()
        pixmap = QPixmap("icon/icon_one.png")
        scaled_pixmap = pixmap.scaledToWidth(230, Qt.SmoothTransformation)  # 设置最大宽度为 230，等比例缩放
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)  # 图片居中显示

        # 设置图片与文字之间的距离
        image_layout = QVBoxLayout()
        image_layout.addWidget(image_label)
        image_layout.addSpacing(30)  # 增加一些距离

        title_label = QLabel("Easy File - 多功能文件处理工具")
        title_label.setFont(QFont('Arial', 25, QFont.Bold))
        title_label.setStyleSheet("color: black; padding: 15px;")

        description = QTextEdit()
        description.setText("Easy File 是一款功能强大的文件处理工具，具有图片处理、文件格式转换、OCR识别、二维码生成等功能。"
                            "此外，Easy File 还提供了文本加密与解密功能，确保你的文件安全可靠。"
                            "让 Easy File 成为你文件处理的得力助手！")

        description.setFont(QFont('Arial', 14))
        description.setStyleSheet("background-color: #606B7A; color: white; padding: 20px;")
        description.setReadOnly(True)

        author_label = QLabel("作者: RUI ")
        author_label.setFont(QFont('Arial', 14))
        author_label.setStyleSheet(" padding: 15px;")

        layout.addLayout(image_layout)
        layout.addWidget(title_label)
        layout.addWidget(description)
        layout.addWidget(author_label)
        layout.addStretch(5)  # 添加拉伸空间

        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def initUI(self):
        self.setWindowTitle('Easy File')  # 设置窗口标题
        self.resize(1600, 1000)  # 调整窗口大小
        self.center_window()  # 居中窗口
        self.setWindowIcon(QIcon(r'icon/icon_one.png'))  # 确保icon.png存在于程序目录下

        # 设置主窗口背景颜色
        self.setStyleSheet("""
            QMainWindow {
                background-color: #808B96;  /* 深灰色背景 */
            }
        """)

        # 连接按钮点击事件与切换标签页的函数
        self.main_button.clicked.connect(lambda: self.switch_tab(0))
        self.image_button.clicked.connect(lambda: self.switch_tab(1))
        self.file_button.clicked.connect(lambda: self.switch_tab(2))
        self.encryption_button.clicked.connect(lambda: self.switch_tab(3))
        self.qr_button.clicked.connect(lambda: self.switch_tab(4))

        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.main_button)
        left_layout.addWidget(self.image_button)
        left_layout.addWidget(self.file_button)
        left_layout.addWidget(self.encryption_button)
        left_layout.addWidget(self.qr_button)
        left_layout.addStretch(5)
        left_layout.setSpacing(35)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(225)

        left_widget.setStyleSheet("""
            QWidget {
                background-color: #808B96;  /* 深灰色背景 */
                border-right: 2px solid #fff;  /* 白色右边框 */
            }
        """)

        # 设置右侧标签页
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.addTab(self.main_tab, QIcon('icon/home.png'), '')
        self.right_widget.addTab(self.image_tab, QIcon('icon/image.png'), '')
        self.right_widget.addTab(self.file_tab, QIcon('icon/file.png'), '')
        self.right_widget.addTab(self.encryption_tab, QIcon('icon/icon.png'), '')
        self.right_widget.addTab(self.qr_tab, QIcon('icon/QR.png'), '')

        self.right_widget.setCurrentIndex(0)  # 设置默认显示的标签页
        self.right_widget.tabBar().hide()  # 隐藏标签栏

        self.right_widget.setStyleSheet('''
            QTabBar::tab {
                background: #808B96;
                border: 1px solid #ccc;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-left: 2px;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #5e5e5e;
            }
            QTabBar::tab:hover {
                background: #5e5e5e;    
            }
        ''')

        # 主布局
        content_layout = QHBoxLayout()
        content_layout.addWidget(left_widget)
        content_layout.addWidget(self.right_widget)
        content_layout.setStretch(0, 1)
        content_layout.setStretch(1, 4)

        main_widget = QWidget()
        main_widget.setLayout(content_layout)
        self.setCentralWidget(main_widget)

    def center_window(self):
        qr = self.frameGeometry()  # 获取窗口的矩形框架
        cp = QDesktopWidget().availableGeometry().center()  # 获取屏幕中心点
        qr.moveCenter(cp)  # 窗口中心移动到屏幕中心
        self.move(qr.topLeft())  # 移动窗口的左上角到新的位置

    def switch_tab(self, index):
        current_widget = self.right_widget.currentWidget()
        new_widget = self.right_widget.widget(index)
        if current_widget != new_widget:
            self.animate_widget(current_widget, 1, 0, 300)  # 当前标签页淡出
            self.right_widget.setCurrentIndex(index)  # 切换到新的标签页
            self.animate_widget(new_widget, 0, 1, 300)  # 新标签页淡入

    def animate_widget(self, widget, start_value, end_value, duration):
        if widget:
            widget.setWindowOpacity(start_value)
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(duration)
            animation.setStartValue(start_value)
            animation.setEndValue(end_value)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序
    main_window = MainFacade()  # 创建主窗口
    main_window.show()  # 显示主窗口

    # 创建系统托盘图标
    tray_icon = QSystemTrayIcon(QIcon("icon/icon_one.png"), app)

    # 创建托盘菜单
    menu = QMenu()

    # 添加打开按钮
    open_action = QAction("打开", app)
    open_action.triggered.connect(main_window.showNormal)  # 恢复窗口显示
    menu.addAction(open_action)

    # 添加退出按钮
    exit_action = QAction("退出", app)
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)

    # 显示任务栏图标
    tray_icon.show()

    sys.exit(app.exec_())  # 运行应用程序事件循环
