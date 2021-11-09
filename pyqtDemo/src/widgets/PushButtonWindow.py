from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout


class PushButtonWindow(QDialog):
    def __init__(self, parent=None):
        super(PushButtonWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('按钮窗口')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)
        self.btn1 = QPushButton('按钮1')
        self.btn2 = QPushButton('按钮2')
        self.btn3 = QPushButton('按钮3(&X)')

        self.btn1.setIcon(wicon)

        self.btn2.setCheckable(True)
        self.btn2.toggle()

        self.btn3.setEnabled(False)

        self.btn1.clicked.connect(lambda: self.switchBtn(self.btn3))
        self.btn1.clicked.connect(lambda: self.btnsStatus(self.btn2))

        self.btn3.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        self.setLayout(layout)

    def switchBtn(self, btn):
        btn.setEnabled(not btn.isEnabled())

    def btnsStatus(self, btn):
        print('btn clicked: ', btn.isChecked())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = PushButtonWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
