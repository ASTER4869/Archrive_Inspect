# coding:utf-8
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,BodyLabel,
                            OptionsSettingCard, PushSettingCard,PushButton,IconWidget,InfoBarIcon,
                            PrimaryPushButton,FluentIcon, PrimaryPushSettingCard, ScrollArea,ComboBox,SearchLineEdit,
                            ComboBoxSettingCard, ExpandLayout, ProgressBar, CustomColorSettingCard,
                            setTheme, setThemeColor, GroupHeaderCardWidget, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths,QThread
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel,QProgressBar, QFileDialog,QHBoxLayout,QVBoxLayout,QTextBrowser,QApplication
from ..tool.classify import classify_ocr_pdf
from ..tool.config import cfg
from ..tool.work import WorkerThread

class OCROperateCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("OCR检测")
        self.setBorderRadius(8)

        self.chooseButton = PushButton("选择目录")
        self.hintLabel = BodyLabel("点击运行按钮以开始检测")
        self.operateButton = PushButton( "运行")
        self.bottomLayout = QHBoxLayout()

        self.chooseButton.setFixedWidth(120)
        self.content = "选择需要检测的文件所在目录"

        # 设置底部工具栏布局

        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.operateButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)

        # 添加组件到分组中
        group = self.addGroup(None,"选择文件夹", self.content, self.chooseButton)

        group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)


class OCRInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.ocrOperateCard=OCROperateCard()
        self.textBrowser=QTextBrowser()
        self.progressBar = QProgressBar()

        # 设置取值范围
        self.progressBar.setRange(0, 100)

        # 设置当前值
        self.progressBar.setValue(0)
        self.__initWidget()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(10, 20, 0, 20)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName('ocrInterface')


        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 30)

        self.progressBar.setStyleSheet("QProgressBar {\n"
                                       "    border: 2px solid grey;\n"
                                       "    border-radius: 5px;\n"
                                       "    text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk {\n"
                                       "    background-color: #05B8CC;\n"
                                       "    width: 10px;\n"
                                       "    margin: 0.5px;\n"
                                       "}")
        self.textBrowser.setStyleSheet(
            "QTextBrowser {"
            "    background-color: #f5f5f5;" 
        "    border: 2px solid grey;" 
        "    border-radius: 8px;" 
        "    padding: 10px;" 
        "    font-family: '宋体';" 
        "    font-size: 20px;" 
        "    color: #333333;" 
        "}"
        )

        # initialize layout
        self.__initLayout()
        # self.__connectSignalToSlot()

    def __initLayout(self):
        self.vBoxLayout.addWidget(self.ocrOperateCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.progressBar, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.textBrowser, 1, Qt.AlignTop)
        self.textBrowser.append("曼波")
        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')

    def __onChooseButtonClicked(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择文件夹", "./")
        if not folder:
            return

        cfg.ocrFolderUrl=folder
        self.ocrOperateCard.groupWidgets[0].setContent(folder)
    def __onOperateButtonClicked(self):
        self.progressBar.setValue(0)

        self.thread = WorkerThread(classify_ocr_pdf,cfg.ocrFolderUrl)  # 逻辑函数
        self.thread.start()
        self.thread.message.connect(self.updateText)
        self.thread.process.connect(self.updateProcess)


    def __connectSignalToSlot(self):
        self.ocrOperateCard.chooseButton.clicked.connect(
            self.__onChooseButtonClicked)
        self.ocrOperateCard.operateButton.clicked.connect(
            self.__onOperateButtonClicked)
    def updateText(self,msg):
        self.textBrowser.append(msg)
        #self.textBrowser.repaint()
        self.cursor =  self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)
        QApplication.processEvents()
    def updateProcess(self,msg):
        self.progressBar.setValue(msg)
        QApplication.processEvents()