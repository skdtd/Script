from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QMainWindow, QPushButton,
                             QToolTip, QVBoxLayout, QWidget)

if __name__ == '__main__':
    from BuddyWindow import BuddyWindow
    from LableWindow import LableWindow
else:
    from widgets.BuddyWindow import BuddyWindow
    from widgets.LableWindow import LableWindow



class MainWindow(QMainWindow):
    '''主窗口'''
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.lw = LableWindow()
        self.bw = BuddyWindow()
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.resize(500, 300)
        self.setWindowTitle('这是主窗口')
        self.setWindowIcon(QIcon(''))                   # 设置图标(mac下无法显示图标)

        self.status = self.statusBar()                  # 初始化状态栏
        self.status.showMessage('I am Message!', 3000)  # 设置状态栏
        QToolTip.setFont(QFont('SansSerif', 12))        # 设置字体
        self.setToolTip('hello world')                  # 设置提示信息

        btn_LW = QPushButton('LableWindow')
        btn_LW.setToolTip('LableWindow')
        btn_LW.clicked.connect(self.lw.showOrHide)
        
        btn_BW = QPushButton('BuddyWindow')
        btn_BW.setToolTip('BuddyWindow')
        btn_BW.clicked.connect(self.bw.display)

        layout = QVBoxLayout()                          # 初始化垂直布局
        layout.addWidget(btn_LW)                        # 向布局中添加按钮
        layout.addWidget(btn_BW)                        # 向布局中添加按钮

        mainFrame = QWidget()                           # 初始化组件
        mainFrame.setLayout(layout)                     # 向组件中添加布局
        # 设置主要组件,setCentralWidget只能由QMainWindow调用
        self.setCentralWidget(mainFrame)

    def center(self) -> None:
        '''移动到屏幕中心'''
        screen = QDesktopWidget().screenGeometry()      # 获取桌面属性
        size = self.geometry()                          # 获取窗口属性
        w = (screen.width() - size.width()) / 2         # 中心位置的x坐标
        h = (screen.height() - size.height()) / 2       # 中心位置的y坐标
        self.move(int(w), int(h))                       # 移动


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = MainWindow()                                   # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
