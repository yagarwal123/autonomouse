from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer, QMutex

import sys
import os

#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.testwin import Ui_testWin

mutex = QMutex()

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,latest_test):
        super().__init__()
        self.setupUi(self)
        self.latest_test = latest_test
        self.title = "Latest test"

    # # update setupUi
    # def setupUi(self, Widget):
    #     super().setupUi(Widget)
        # Widget.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.popTable())
        self.timer.start(1000)
        #self.Widget.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 

        self.m_name.setText(self.latest_test.mouse.get_name())
        self.m_id.setText(self.latest_test.mouse.get_id())
        self.test_start_time.setText(str(self.latest_test.starting_time))

    def popTable(self):
        mutex.lock()
        trials = self.latest_test.trials
        self.tableWidget.setRowCount(len(trials))
        for idx,t_time in enumerate(trials):
            self.tableWidget.setItem(idx,0,QtWidgets.QTableWidgetItem(str(idx + 1)))
            self.tableWidget.setItem(idx,1,QtWidgets.QTableWidgetItem(str(t_time)))
        mutex.unlock()