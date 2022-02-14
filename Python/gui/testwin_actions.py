from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer

import sys
import os

#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.testwin import Ui_testWin

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,mutex,all_tests):
        super().__init__()
        self.setupUi(self)
        self.all_tests = all_tests
        self.mutex = mutex
        self.title = "Latest test"

    # # update setupUi
    # def setupUi(self, Widget):
    #     super().setupUi(Widget)
        # Widget.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.popData())
        self.timer.start(1000)
        #self.Widget.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 


    def popData(self):
        self.mutex.lock()
        test = self.all_tests[-1]
        self.m_name.setText(test.mouse.get_name())
        self.m_id.setText(test.mouse.get_id())
        self.test_start_time.setText(str(test.starting_time))
        self.tableWidget.setRowCount(len(test.trials))
        for idx,t_time in enumerate(test.trials):
            self.tableWidget.setItem(idx,0,QtWidgets.QTableWidgetItem(str(idx + 1)))
            self.tableWidget.setItem(idx,1,QtWidgets.QTableWidgetItem(str(t_time)))
        self.mutex.unlock()