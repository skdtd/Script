from PyQt5.QtWidgets import QWidget


class NewWidget(QWidget):
    '''主窗口'''
    def __init__(self, parent = None) -> None:
        super(NewWidget, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.setGeometry(100, 100, 300, 200)            # 设置窗口属性(x,y,w,h)
        self.setWindowTitle('new window')               # 设置标题
    def showOrHide(self) -> None:
        sender = self.sender()                          # 获取信号发送源
        print(sender)
        if self.isHidden():
            self.show()
        else:
            self.close()
