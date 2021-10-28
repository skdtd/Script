
from PyQt5.QtCore import QSettings

print(123)
settings = QSettings('AAAAPPPPPPPP','APP')
settings.setValue('asb','aaaa')
print(settings.value('asb'))
print(settings)
print(settings.fileName())
print(settings.allKeys())
print(settings.applicationName())
print(settings.clear())