import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    '''主窗口'''

    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.resize(500, 300)
        self.btn = QPushButton('close')                 # 初始化按钮
        self.btn.clicked.connect(self.close)            # 设置按钮的点击动作

        self.lb1 = QLabel()                             # 初始化标签
        self.lb1.setText("<h1>this is a lable</h1>")    # 设置标签文字,可以使用html格式
        self.lb1.setAutoFillBackground(True)            # 自动填充背景
        palette = QPalette()                            # 初始化调色板
        palette.setColor(palette.Background, Qt.GlobalColor.yellow)  # 设置背景色
        self.lb1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置对齐方式
        self.lb1.setPalette(palette)                    # 应用调色板到标签

        self.lb2 = QLabel()                             # 初始化标签
        pic = QPixmap("src/resource/1.jpg")

        self.lb2.setPixmap(pic)                         # 设置标签图片
        layout = QVBoxLayout()                          # 初始化水平布局
        layout.addWidget(self.btn)                      # 向布局中添加按钮
        layout.addWidget(self.lb1)
        layout.addWidget(self.lb2)
        mainFrame = QWidget()                           # 初始化组件
        mainFrame.setLayout(layout)                     # 向组件中添加布局
        # 设置主要组件,setCentralWidget只能由QMainWindow调用
        self.setCentralWidget(mainFrame)

    def setStatusText(self):
        self.setStatusBar("123")


if __name__ == '__main__':
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = MainWindow()                                   # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
