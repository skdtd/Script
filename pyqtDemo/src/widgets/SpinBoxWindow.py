from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QRadioButton, QSpinBox


class SpinBoxWindow(QDialog):
    def __init__(self, parent=None):
        super(SpinBoxWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)
        self.lable = QLabel('&Hello')
        self.spin = QSpinBox()
        self.spin.setMaximum(20)
        self.spin.setMinimum(1)
        self.spin.setValue(10)
        self.spin.setSingleStep(1)
        self.spin.valueChanged.connect(self.getStatus)
        self.lable.setBuddy(self.spin)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lable)
        hbox.addWidget(self.spin)
        self.setLayout(hbox)

    def getStatus(self):
        self.lable.setFont(QFont('Arial',self.spin.value()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = SpinBoxWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
