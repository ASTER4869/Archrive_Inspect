# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths,QThread
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog,QHBoxLayout,QVBoxLayout
class WorkerThread(QThread):
    resultReady = pyqtSignal(object)
    process = pyqtSignal(object)
    message = pyqtSignal(object)
    def __init__(self, func, *args, **kwargs):
        QThread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def run(self):
        self.result = self.func(self,*self.args, **self.kwargs)
        self.resultReady.emit(self.result)
    # 返回执行的结果
    def get_result(self):
        return self.result