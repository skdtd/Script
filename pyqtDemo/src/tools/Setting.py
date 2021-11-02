import sys

from exception import ConstCaseError, NotFoundSettingsError


class _Setting():
    _keys = ['A', 'B']

    def __init__(self) -> None:
        # 注册表位置: HKEY_CURRENT_USER\Software\
        pass

    def __setattr__(self, name, value):
        if not name.isupper():
            # 属性名全大写
            raise ConstCaseError(
                'const name "{0}" is not all uppercase'.format(name))
        if name not in _Setting._keys:
            # 设置项检查
            raise NotFoundSettingsError(
                'The related setting named "{0}" could not be found'.format(name))
        self.__dict__[name] = value

    def __getattr__(self, name):
        print('"{0}" is not initialized or does not have this setting'.format(name))
        return None

    def push():
        pass


sys.modules[__name__] = _Setting()
