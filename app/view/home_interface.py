# coding:utf-8
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,BodyLabel,
                            OptionsSettingCard, PushSettingCard,PushButton,IconWidget,InfoBarIcon,
                            PrimaryPushButton,FluentIcon, PrimaryPushSettingCard, ScrollArea,ComboBox,SearchLineEdit,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, GroupHeaderCardWidget, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths,QThread
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog,QHBoxLayout,QVBoxLayout
from ..tool.xls_view import dataCheck,pdfFileCheck
from ..tool.config import cfg
from ..tool.work import WorkerThread
class IndexOperateCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("条目数据检测")
        self.setBorderRadius(8)

        self.chooseButton = PushButton("选择目录文件")


        self.hintLabel = BodyLabel("点击运行按钮以开始检测")
        self.operateButton = PushButton( "运行")
        self.bottomLayout = QHBoxLayout()

        self.chooseButton.setFixedWidth(120)
        self.content = "选择需要检测的目录文件"



        # 设置底部工具栏布局

        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.operateButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)

        # 添加组件到分组中
        group = self.addGroup(None,"选择文件", self.content, self.chooseButton)

        group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)
class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)



        self.indexOperateCard=IndexOperateCard()
        self.__initWidget()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(10, 20, 0, 20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('homeInterface')

        # initialize style sheet
        # self.scrollWidget.setObjectName('scrollWidget')
        # self.settingLabel.setObjectName('settingLabel')

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)

        # initialize layout
        self.__initLayout()
        # self.__connectSignalToSlot()

    def __initLayout(self):
        self.vBoxLayout.addWidget(self.indexOperateCard, 0, Qt.AlignTop)
        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')

    def __onChooseButtonClicked(self):
        fileUrl, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "./", "Excel文件(*xls *xlsx)")
        if not fileUrl:
            return
        cfg.itemFileUrl = fileUrl
        self.indexOperateCard.groupWidgets[0].setContent(fileUrl)
    def __onOperateButtonClicked(self):

        self.thread = WorkerThread(dataCheck,cfg.itemFileUrl)  # 逻辑函数
        self.thread.start()

    def __connectSignalToSlot(self):
        self.indexOperateCard.chooseButton.clicked.connect(
            self.__onChooseButtonClicked)
        self.indexOperateCard.operateButton.clicked.connect(
            self.__onOperateButtonClicked)