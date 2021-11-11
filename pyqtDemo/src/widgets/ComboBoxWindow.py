from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDialog, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class ComboBoxWindow(QWidget):
    def __init__(self, parent=None):
        super(ComboBoxWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('下拉列表窗口')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)
        list = ['java', 'python', 'c', 'c++', 'scale', 'go', 'shell']
        self.combo = QComboBox()
        self.combo.addItems(list)
        self.combo.currentIndexChanged.connect(self.getStatus)
        vbox = QVBoxLayout()
        vbox.addWidget(self.combo)
        self.setLayout(vbox)

    def getStatus(self):
        print(self.combo.currentText())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = ComboBoxWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
