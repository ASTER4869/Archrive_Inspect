# coding: utf-8
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition)
from qfluentwidgets import FluentIcon as FIF
from .home_interface import HomeInterface
from .ocr_interface import OCRInterface
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.homeInterface = HomeInterface(self)
        self.ocrInterface = OCRInterface(self)


        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.DOCUMENT, '目录检测')
        self.addSubInterface(self.ocrInterface, FIF.FOLDER, 'OCR检测')
        self.addSubInterface(self.ocrInterface, FIF.LIBRARY_FILL, 'OCR检测')
        self.navigationInterface.addSeparator()

        


    def initWindow(self):
        self.resize(900, 700)
        self.setWindowTitle('检测程序')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)