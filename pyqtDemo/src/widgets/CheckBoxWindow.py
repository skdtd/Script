from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QDialog, QVBoxLayout


class CheckBoxWindow(QDialog):
    def __init__(self, parent=None):
        super(CheckBoxWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('复选框窗口')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)
        
        self.cb1 = QCheckBox('apple')
        self.cb2 = QCheckBox('orange')
        self.cb3 = QCheckBox('banana')
        self.cb1.setChecked(True)
        self.cb2.setTristate(True)   # 设置允许半选中
        self.cb1.stateChanged.connect(self.BoxStatus)
        self.cb2.stateChanged.connect(self.BoxStatus)
        self.cb3.stateChanged.connect(self.BoxStatus)
        vbox = QVBoxLayout()
        vbox.addWidget(self.cb1)
        vbox.addWidget(self.cb2)
        vbox.addWidget(self.cb3)
        self.setLayout(vbox)

    def BoxStatus(self):
        cb1 = '{0}: {1}, {2}'.format(self.cb1.text(), self.cb1.isChecked(), self.cb1.checkState())
        cb2 = '{0}: {1}, {2}'.format(self.cb2.text(), self.cb2.isChecked(), self.cb2.checkState())
        cb3 = '{0}: {1}, {2}'.format(self.cb3.text(), self.cb3.isChecked(), self.cb3.checkState())
        print(cb1,cb2,cb3)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = CheckBoxWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
