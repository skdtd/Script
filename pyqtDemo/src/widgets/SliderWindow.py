from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QDialog, QHBoxLayout, QSlider, QVBoxLayout


class CheckBoxWindow(QDialog):
    def __init__(self, parent=None):
        super(CheckBoxWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('复选框窗口')
        self.resize(300, 200)
        wicon = QIcon(QPixmap('src/resource/1.jpg'))
        self.setWindowIcon(wicon)
        
        self.hslider = QSlider(Qt.Orientation.Horizontal)
        self.vslider = QSlider(Qt.Orientation.Vertical)
        self.hslider.setObjectName('hslider')
        self.vslider.setObjectName('vslider')
        self.hslider.setMinimum(0)          # 设置最小值
        self.hslider.setMaximum(100)        # 设置最大值
        self.hslider.setSingleStep(100)     # 设置步长
        self.hslider.setValue(50)           # 设置初始显示值
        self.hslider.setTickPosition(QSlider.TickPosition.TicksBelow)   # 显示刻度位置
        self.hslider.setTickInterval(20)    # 显示刻度间隔
        self.hslider.valueChanged.connect(lambda:self.getValue(self.hslider))
        self.vslider.valueChanged.connect(lambda:self.getValue(self.vslider))

        layout = QHBoxLayout()
        layout.addWidget(self.hslider)
        layout.addWidget(self.vslider)
        self.setLayout(layout)

    def getValue(self,slider):
        print(slider.objectName(),slider.value())
        # print('vslider',slider.value())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = CheckBoxWindow()                             # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
