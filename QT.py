import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# QtDesigner生成`的.ui文件转.py文件
# 方法1: python -m PyQt5.uic.pyuic <filename>.ui -o <filename>.py
# 方法2: <venv>/Lib/site-packages/PyQt5/uic/pyuic.py <filename>.ui -o <filename>.py
# ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@192.168.100.103



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = QWidget()
    mw = QMainWindow()
    mw.show()
    sys.exit(app.exec_())
