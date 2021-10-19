import sys
from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# QtDesigner生成`的.ui文件转.py文件
# 方法1: python -m PyQt5.uic.pyuic <filename>.ui -o <filename>.py
# 方法2: <venv>/Lib/site-packages/PyQt5/uic/pyuic.py <filename>.ui -o <filename>.py
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@192.168.100.103


if __name__ == '__main__':
    # 创建主应用程序
    app = QApplication(sys.argv)
    # 创建主窗口
    mw = QMainWindow()
    # 初始化窗口示例
    ui = Ui_MainWindow()
    # 创建窗口
    ui.setupUi(mw)

    # 显示窗口
    mw.show()
    sys.exit(app.exec_())
