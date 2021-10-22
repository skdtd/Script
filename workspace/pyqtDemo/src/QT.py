from _typeshed import Self
import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QWidget, QDialog


# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@192.168.100.103

# QtDesigner生成的.ui文件转.py文件
# 方法1: python -m PyQt5.uic.pyuic <filename>.ui -o <filename>.py
# 方法2: <venv>/Lib/site-packages/PyQt5/uic/pyuic.py <filename>.ui -o <filename>.py


# QT的三种窗口类型
# QMainWindow, QDialog, QWidget
# QMainWindow:  主窗口,可以包含菜单栏,工具栏和标题栏
# QDialog:      对话框的基类,没有菜单栏,工具栏和标题栏
# QWidget:      组件窗口


class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setWindowTitle('APP')
        self.resize(400, 300)
        self.status = self.statusBar()
        self.status.showMessage('I am Message!', 3000)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        w = (screen.width() - size.width()) / 2
        h = (screen.height() - size.height()) / 2
        self.move(int(w), int(h))


if __name__ == '__main__':
    # 创建主应用程序
    app = QApplication(sys.argv)
    # 设置应用图标
    app.setWindowIcon(QIcon(''))

    # 创建主窗口
    mw = MainWin()
    # 显示窗口
    mw.show()

    sys.exit(app.exec_())
