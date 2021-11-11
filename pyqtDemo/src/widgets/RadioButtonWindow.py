from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QRadioButton


class RadioButtonWindow(QDialog):
    def __init__(self, parent=None):
        super(RadioButtonWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('单选按钮窗口')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)

        rbtn1 = QRadioButton('man')
        rbtn2 = QRadioButton('woman')
        rbtn1.setChecked(True)
        rbtn1.toggled.connect(self.buttonStatus)
        rbtn2.toggled.connect(self.buttonStatus)

        layout = QHBoxLayout()
        layout.addWidget(rbtn1)
        layout.addWidget(rbtn2)
        self.setLayout(layout)
    def buttonStatus(self):
        sender = self.sender()
        print(sender.text(),sender.isChecked())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = RadioButtonWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
