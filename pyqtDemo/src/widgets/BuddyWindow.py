from PyQt5.QtGui import QDoubleValidator, QIcon, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
                             QLineEdit, QPushButton)

from PyQt5.QtCore import QRegExp

'''掩码
A	ASCII字母字符是必须输入的（A-Z，a-z）
a	ASCII字母字符是允许输入的，但不是必须输入的
N	ASCII字母字符是必须输入的（A-Z，a-z，0-9）
n	ASCII字母字符是允许输入的，但不是必须输入的
X	任何字符都是必须输入
x	任何字符都是允许输入的，但不是必须输入的
9	ASCII数字字符是必须输入的（0-9）
0	ASCII数字字符是允许输入的，但不是必须输入的
D	ASCII数字字符是必须输入的（1-9）
d	ASCII数字字符是允许输入的，但不是必须的（1-9）
#	ASCII数字字符与加减字符是允许输入的，但不是必须的
H	十六进制格式字符是必须输入的（A-F，a-f，0-9）
h	十六进制格式字符允许输入，但不是必须的
B	二进制格式字符是必须输入的（0,1）
b	二进制格式字符是允许输入的，但不是必须的
>	所有字母字符都大写
<	所有字母字符都小写
！	关闭大小写转换
\	使用‘\’转义上面列出的字符
'''


class BuddyWindow(QDialog):
    '''主窗口'''

    def __init__(self, parent=None) -> None:
        super(BuddyWindow, self).__init__(parent)

        self.initUI()

    def initUI(self) -> None:
        '''初始化界面'''
        self.setWindowTitle('Qlable与伙伴关系')
        self.resize(300, 200)
        username = QLabel('user&Name', self) # &:后面字母为热键
        password = QLabel('&Password', self)
        phone    = QLabel('&Phone',    self)
        email    = QLabel('&E-Mail',   self)
        gender   = QLabel('&Gender',   self)

        self.usernameLineEdit = QLineEdit(self)
        self.passwordLineEdit = QLineEdit(self)
        self.phoneLineEdit    = QLineEdit(self)
        self.emailLineEdit    = QLineEdit(self)
        self.genderLineEdit   = QLineEdit(self)

        # 隐藏输入
        # EchoMode(4种):
        # 1. Normal: 正常显示
        # 2. NoEcho: 不回显
        # 3. Password: 隐藏显示
        # 4. PasswordEchoOnEdit: 失去焦点后隐藏,再输入时删除之前输入内容
        self.usernameLineEdit.setPlaceholderText('用户名')
        self.passwordLineEdit.setPlaceholderText('密码')
        self.phoneLineEdit.setPlaceholderText('手机号码')
        self.emailLineEdit.setPlaceholderText('E-Mail')
        self.genderLineEdit.setPlaceholderText('性别')

        # 设置只读
        self.genderLineEdit.setText('男')
        self.genderLineEdit.setReadOnly(True)

        # 设置回显
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        # 输入验证
        intVal = QIntValidator()                                    # 整型校验
        intVal.setRange(1,2147483647)                               # 允许范围
        doubleVal = QDoubleValidator()                              # 浮点数校验
        doubleVal.setRange(-9999999,9999999)                        # 允许范围
        doubleVal.setNotation(QDoubleValidator.StandardNotation)    # 标准显示
        doubleVal.setDecimals(2)                                    # 小数位数
        regVal = QRegExpValidator()                                 # 正则校验
        regVal.setRegExp(QRegExp('^[\d|A-z]+$'))                    # 设置正则

        # 限定输入长度
        self.usernameLineEdit.setMaxLength(16)
        self.phoneLineEdit.setMaxLength(11)

        # 设置输入验证
        self.usernameLineEdit.setValidator(regVal)
        self.passwordLineEdit.setValidator(doubleVal)
        self.phoneLineEdit.setValidator(intVal)
        
        # 设置伙伴关系
        username.setBuddy(self.usernameLineEdit)
        password.setBuddy(self.passwordLineEdit)
        phone.setBuddy(self.phoneLineEdit)
        email.setBuddy(self.emailLineEdit)
        gender.setBuddy(self.genderLineEdit)

        # 掩码
        self.emailLineEdit.setInputMask('Nnnnnn@Nnn.Nnn;x')

        btn_OK = QPushButton('&OK')
        btn_Cancel = QPushButton('&Cancel')

        # 设置信号
        btn_OK.clicked.connect(self.printInput)
        btn_Cancel.clicked.connect(self.close)
        
        mlayout = QGridLayout()
        # addWidget(组件, 行, 列, 占几行, 占几列, 对齐方式)
        mlayout.addWidget(username, 1, 1, 1, 2)
        mlayout.addWidget(password, 2, 1, 1, 2)
        mlayout.addWidget(phone, 3, 1, 1, 2)
        mlayout.addWidget(email, 4, 1, 1, 2)
        mlayout.addWidget(gender, 5, 1, 1, 2)
        mlayout.addWidget(self.usernameLineEdit, 1, 2, 1, 2)
        mlayout.addWidget(self.passwordLineEdit, 2, 2, 1, 2)
        mlayout.addWidget(self.phoneLineEdit, 3, 2, 1, 2)
        mlayout.addWidget(self.emailLineEdit, 4, 2, 1, 2)
        mlayout.addWidget(self.genderLineEdit, 5, 2, 1, 2)
        mlayout.addWidget(btn_OK, 6, 2)
        mlayout.addWidget(btn_Cancel, 6, 3)
        self.setLayout(mlayout)

    def printInput(self):
        print('username:',self.usernameLineEdit.text())
        print('password:',self.passwordLineEdit.text())
        print('phone:',self.phoneLineEdit.text())
        print('email:',self.emailLineEdit.text())
        print('gender:',self.genderLineEdit.text())
        self.close()

    def display(self):
        self.usernameLineEdit.clear()
        self.passwordLineEdit.clear()
        self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)                        # 创建主应用程序
    app.setApplicationName('APP')                       # 设置应用名称
    app.setWindowIcon(QIcon(''))                        # 设置应用图标
    mw = BuddyWindow()                                  # 创建主窗口
    mw.show()                                           # 显示窗口
    sys.exit(app.exec_())
