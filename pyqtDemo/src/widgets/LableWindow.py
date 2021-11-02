from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)


class LableWindow(QMainWindow):
    STATUS_FLAG = False
    '''主窗口'''

    def __init__(self, parent=None) -> None:
        super(LableWindow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.setWindowTitle('标签')
        self.resize(500, 300)
        self.btn = QPushButton('close')                 # 初始化按钮
        self.btn.clicked.connect(self.close)            # 设置按钮的点击动作
        self.status = self.statusBar()                  # 初始化状态栏

        lb1 = QLabel(self)                              # 初始化标签
        # 设置标签文字,可以使用html格式
        lb1.setText("<a href='www.baidu.com'>欢迎使用Python GUI程序</a>")
        lb1.setAutoFillBackground(True)                 # 自动填充背景
        palette = QPalette()                            # 初始化调色板
        palette.setColor(palette.Background, Qt.GlobalColor.yellow)  # 设置背景色
        lb1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置对齐方式
        lb1.setPalette(palette)                         # 应用调色板到标签
        # 设置鼠标移过事件
        # 在可点击的状态下有效
        # 在移动到文字上和标签内文字外为两种事件
        lb1.linkHovered.connect(self.setStatusText)
        lb1.setOpenExternalLinks(False)                 # 与单击事件相斥,设置不打开富文本连接

        lb2 = QLabel()                                  # 初始化标签
        pic = QPixmap("src/resource/1.jpg")
        lb2.setMaximumSize(300, 200)
        lb2.setPixmap(pic)                              # 设置标签图片
        layout = QVBoxLayout()                          # 初始化水平布局
        layout.addWidget(self.btn)                      # 向布局中添加按钮
        layout.addWidget(lb1)
        layout.addWidget(lb2)
        mainFrame = QWidget()                           # 初始化组件
        mainFrame.setLayout(layout)                     # 向组件中添加布局
        # 设置主要组件,setCentralWidget只能由QMainWindow调用
        self.setCentralWidget(mainFrame)

    def setStatusText(self):
        if LableWindow.STATUS_FLAG:
            self.status.clearMessage()
            LableWindow.STATUS_FLAG = False
        else:
            self.status.showMessage("this is a lable")
            LableWindow.STATUS_FLAG = True

    def showOrHide(self) -> None:
        if self.isHidden():
            self.show()
        else:
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = LableWindow()                                   # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
