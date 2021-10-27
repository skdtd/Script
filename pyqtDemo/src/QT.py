# Python API: https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qtcore-module.html
import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPalette  # 调色板
from PyQt5.QtGui import QPixmap  # 图片
from PyQt5.QtGui import QFont, QIcon  # 字体和图标
from PyQt5.QtWidgets import QApplication  # 主应用程序
from PyQt5.QtWidgets import QDesktopWidget  # windows桌面属性类
from PyQt5.QtWidgets import QDialog  # 对话框的基类,没有菜单栏,工具栏和标题栏
from PyQt5.QtWidgets import QHBoxLayout  # 水平布局
from PyQt5.QtWidgets import QMainWindow  # 主窗口,可以包含菜单栏,工具栏和标题栏
from PyQt5.QtWidgets import QPushButton  # 按钮
from PyQt5.QtWidgets import QToolTip  # 提示星系
from PyQt5.QtWidgets import QWidget  # 组件窗口,三种窗口的基类

# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@192.168.100.103

# QtDesigner生成的.ui文件转.py文件
# 方法1: python -m PyQt5.uic.pyuic <filename>.ui -o <filename>.py
# 方法2: <venv>/Lib/site-packages/PyQt5/uic/pyuic.py <filename>.ui -o <filename>.py


# QT的三种窗口类型
# QMainWindow, QDialog, QWidget
# QMainWindow:  主窗口,可以包含菜单栏,工具栏和标题栏
# QDialog:      对话框的基类,没有菜单栏,工具栏和标题栏
# QWidget:
class aWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(aWidget, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('TEST')


class MainWin(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWin, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(100, 100, 300, 200)            # 设置窗口属性(x,y,w,h)
        self.setWindowTitle('APP')                      # 设置标题
        self.setWindowIcon(QIcon(''))                   # 设置图标(mac下无法显示图标)

        self.status = self.statusBar()                  # 初始化状态栏
        self.status.showMessage('I am Message!', 3000)  # 设置状态栏
        QToolTip.setFont(QFont('SansSerif', 12))        # 设置字体
        self.setToolTip('hello world')                  # 设置提示信息

        self.btn = QPushButton('Click hear')            # 初始化按钮
        self.btn.setToolTip('heiheihei')                # 设置按钮文字
        self.btn.clicked.connect(self.center)           # 设置按钮的点击动作

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


if __name__ == '__main__':
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = MainWin()                                      # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
