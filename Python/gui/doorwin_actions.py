from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer, QMutex

import sys
import os

#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.doorwin import Ui_doorWin

mutex = QMutex()

class doorwinActions(QtWidgets.QWidget, Ui_doorWin):
    def __init__(self,doors):
        super().__init__()
        self.setupUi(self)
        self.doors = doors
        self.title = "Doors"

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

    def popTable(self):
        mutex.lock()
        entries = len(self.doors)
        self.tableWidget.setRowCount(entries)
        for i in range(entries):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.doors[i][0])))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(self.doors[i][1].get_id()))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(self.doors[i][1].get_name()))
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(self.doors[i][2])))
        mutex.unlock()