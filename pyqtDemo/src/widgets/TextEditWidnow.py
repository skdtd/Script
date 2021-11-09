from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget)


class TextEditWidnow(QWidget):
    def __init__(self, parent=None):
        super(TextEditWidnow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.setWindowTitle('Qlable与伙伴关系')
        self.resize(500, 300)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.btn_getText = QPushButton('Get&Text')
        self.btn_setText = QPushButton('SetT&ext')
        self.btn_getHtml = QPushButton('Get&Html')
        self.btn_setHtml = QPushButton('SetHt&ml')
        self.btn_getText.clicked.connect(self.getText)
        self.btn_setText.clicked.connect(self.setText)
        self.btn_getHtml.clicked.connect(self.getHtml)
        self.btn_setHtml.clicked.connect(self.setHtml)
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btn_getText)
        layout.addWidget(self.btn_setText)
        layout.addWidget(self.btn_getHtml)
        layout.addWidget(self.btn_setHtml)
        self.setLayout(layout)

    def getText(self):
        print(self.textEdit.toPlainText())

    def setText(self):
        self.textEdit.setText('Hello World')

    def getHtml(self):
        print(self.textEdit.toHtml())

    def setHtml(self):
        self.textEdit.setHtml('<font color="blue" size=10>Hello Pyhton</font>')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = TextEditWidnow()                                  # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
