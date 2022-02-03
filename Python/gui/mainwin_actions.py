from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QThread

import sys

#from gui import mainwin
from gui.mainwin import Ui_MainWindow
from gui.mousewin_actions import mousewinActions
from gui.doorwin_actions import doorwinActions
from gui.lickwin_actions import lickwinActions
from start_teensy_read import startTeensyRead


class mainwinActions(Ui_MainWindow):
    def __init__(self, all_mice = {},doors=[],live_licks=[]):
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.title = 'Main Window'
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150

    # update setupUi
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # MainWindow.resize(400, 300) # do not modify it
        MainWindow.move(self.left, self.top)  # set location for window
        MainWindow.setWindowTitle(self.title) # change title

        self.worker = TeensyRead(self.all_mice,self.doors,self.live_licks)
        self.worker.start()
        self.myactions() # add actions for different buttons

    # define actions here
    def myactions(self):
        self.mouse_button.clicked.connect(self.open_mouse)
        self.doorButton.clicked.connect(self.open_door)
        self.lickButton.clicked.connect(self.open_lick)


    def open_mouse(self):
        #app = QtWidgets.QApplication(sys.argv)
        self.mousewin = QtWidgets.QWidget()
        ID = self.mouse_id_select.currentText().split(' - ')[0]
        self.mouseui = mousewinActions(self.all_mice[ID])
        self.mouseui.setupUi(self.mousewin)
        self.mousewin.show()

    def open_door(self):
        #app = QtWidgets.QApplication(sys.argv)
        self.doorwin = QtWidgets.QWidget()
        self.doorui = doorwinActions(self.doors)
        self.doorui.setupUi(self.doorwin)
        self.doorwin.show()

    def open_lick(self):
        #app = QtWidgets.QApplication(sys.argv)
        self.lickwin = QtWidgets.QWidget()
        self.lickui = lickwinActions(self.live_licks)
        self.lickui.setupUi(self.lickwin)
        self.lickwin.show()

class TeensyRead(QThread):
    def __init__(self, all_mice = {},doors=[],live_licks=[]):
        super(TeensyRead, self).__init__()
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks

    def run(self):
        startTeensyRead(self.all_mice,self.doors,self.live_licks)