import sys
import threading

from exception.ConstCaseError import ConstCaseError
from exception.NotFoundSettingsError import NotFoundSettingsError
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication


class _Setting():
    _instance_lock = threading.Lock()
    _keys = [
        "WIDTH", "HEGITH", "x", "y"
    ]

    def __init__(self, app: QApplication) -> None:
        # 注册表位置: HKEY_CURRENT_USER\Software\
        self.organizationName = app.applicationName()
        self.GUI = QSettings(self.OrganizationName, 'GUI')
        self.CONFIG = QSettings(self.OrganizationName, 'CONFIG')

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(_Setting, "_instance"):
            with _Setting._instance_lock:
                if not hasattr(_Setting, "_instance"):
                    _Setting._instance = object.__new__(cls)
        return _Setting._instance

    def __setattr__(self, name, value):
        if not name.isupper():  # 属性名全大写
            raise ConstCaseError(
                "const name {0} is not all uppercase".format(name))
        if name not in _Setting:  # 设置项检查
            raise NotFoundSettingsError(
                "The related setting named {0} could not be found".format(name))

        self.__dict__[name] = value


sys.modules[__name__] = _Setting()
