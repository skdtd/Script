# Python API: https://www.riverbankcomputing.com/static/Docs/PyQt5/module_index.html
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from widgets.MainWindow import MainWindow

# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@192.168.100.103

# QtDesigner生成的.ui文件转.py文件
# 方法1: python -m PyQt5.uic.pyuic <filename>.ui -o <filename>.py
# 方法2: <venv>/Lib/site-packages/PyQt5/uic/pyuic.py <filename>.ui -o <filename>.py


# QT的三种窗口类型
# QMainWindow, QDialog, QWidget
# QMainWindow:  主窗口,可以包含菜单栏,工具栏和标题栏
# QDialog:      对话框的基类,没有菜单栏,工具栏和标题栏
# QWidget:
if __name__ == '__main__':
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = MainWindow()                                   # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
