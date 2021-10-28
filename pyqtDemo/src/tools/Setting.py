
import os

from PyQt5.QtCore import QSettings

from Main import App

class Setting():
    def __init__(self) -> None:
        self.config = QSettings('','APP')