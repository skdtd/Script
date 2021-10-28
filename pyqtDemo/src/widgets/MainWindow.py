

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QDesktopWidget, QHBoxLayout, QMainWindow,
                             QPushButton, QToolTip, QWidget)

from widgets.NewWidget import NewWidget


class MainWindow(QMainWindow):
    
    '''主窗口'''
    def __init__(self, parent = None) -> None:
        super(MainWindow, self).__init__(parent)
        self.nw = NewWidget()
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.resize(500,300)
        # self.setGeometry(100,100,500, 300)            # 设置窗口属性(x,y,w,h)
        self.setWindowTitle('APP')                      # 设置标题
        self.setWindowIcon(QIcon(''))                   # 设置图标(mac下无法显示图标)

        self.status = self.statusBar()                  # 初始化状态栏
        self.status.showMessage('I am Message!', 3000)  # 设置状态栏
        QToolTip.setFont(QFont('SansSerif', 12))        # 设置字体
        self.setToolTip('hello world')                  # 设置提示信息

        self.btn = QPushButton('Click hear')            # 初始化按钮
        self.btn.setToolTip('heiheihei')                # 设置按钮文字
        self.btn.clicked.connect(self.nw.showOrHide)    # 设置按钮的点击动作
        layout = QHBoxLayout()                          # 初始化水平布局
        layout.addWidget(self.btn)                      # 向布局中添加按钮

        mainFrame = QWidget()                           # 初始化组件
        mainFrame.setLayout(layout)                     # 向组件中添加布局
        self.setCentralWidget(mainFrame)                # 设置主要组件,setCentralWidget只能由QMainWindow调用

    def center(self) -> None:
        '''移动到屏幕中心'''
        screen = QDesktopWidget().screenGeometry()      # 获取桌面属性
        size = self.geometry()                          # 获取窗口属性
        w = (screen.width() - size.width()) / 2         # 中心位置的x坐标
        h = (screen.height() - size.height()) / 2       # 中心位置的y坐标
        self.move(int(w), int(h))                       # 移动
