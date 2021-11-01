from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
                             QLineEdit, QPushButton)


class BuddyWindow(QDialog):
    '''主窗口'''

    def __init__(self, parent=None) -> None:
        super(BuddyWindow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.setWindowTitle('Qlable与伙伴关系')
        self.resize(300, 200)
        username = QLabel('user&Name', self)
        password = QLabel('&Password', self)
        self.usernameLineEdit = QLineEdit(self)
        self.passwordLineEdit = QLineEdit(self)
        # 隐藏输入
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        username.setBuddy(self.usernameLineEdit)
        password.setBuddy(self.passwordLineEdit)
        btn_OK = QPushButton('&OK')
        btn_Cancel = QPushButton('&Cancel')
        btn_OK.clicked.connect(self.printInput)
        btn_Cancel.clicked.connect(self.close)

        mlayout = QGridLayout()
        # addWidget(组件, 行, 列, 占几行, 占几列, 对齐方式)
        mlayout.addWidget(username, 1, 1, 1, 2)
        mlayout.addWidget(password, 2, 1, 1, 2)
        mlayout.addWidget(self.usernameLineEdit, 1, 2, 1, 2)
        mlayout.addWidget(self.passwordLineEdit, 2, 2, 1, 2)
        mlayout.addWidget(btn_OK, 3, 2)
        mlayout.addWidget(btn_Cancel, 3, 3)
        self.setLayout(mlayout)

    def printInput(self):
        print(self.usernameLineEdit.text())
        print(self.passwordLineEdit.text())
        self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = BuddyWindow()                                   # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
