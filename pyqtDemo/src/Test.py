

# 注册表位置: HKEY_CURRENT_USER\Software\
from PyQt5.QtCore import QSettings

name = "AAAPPP"
GUI = QSettings(name, 'GUI')
CONFIG = QSettings(name, 'CONFIG')
GUI.setValue("a/b/c","1")
CONFIG.setValue("b","2")