from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QThread

import logging

#from gui import mainwin
from gui.mainwin import Ui_MainWindow
from gui.mousewin_actions import mousewinActions
from gui.doorwin_actions import doorwinActions
from gui.lickwin_actions import lickwinActions
from gui.testwin_actions import testwinActions
from start_teensy_read import startTeensyRead

logger = logging.getLogger(__name__)


class mainwinActions(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, START_TIME, all_mice,doors=[],live_licks=[],all_tests=[]):
        super().__init__()
        self.setupUi(self)
        self.title = 'Main Window'

        self.START_TIME = START_TIME
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.all_tests = all_tests

    # # update setupUi
    # def setupUi(self, MainWindow):
    #     super().setupUi(MainWindow)
        # MainWindow.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title

        self.worker = TeensyRead(self.START_TIME,self.all_mice,self.doors,self.live_licks,self.all_tests)
        self.worker.start()
        self.myactions() # add actions for different buttons

        #self.mouse_id_select.setItemText(3, ("MainWindow", "A11fvg111 - Stuart"))
        for id, m in self.all_mice.items():
            self.mouse_id_select.addItem(id + ' - ' + m.get_name())

    # define actions here
    def myactions(self):
        self.mouse_button.clicked.connect(self.open_mouse)
        self.doorButton.clicked.connect(self.open_door)
        self.lickButton.clicked.connect(self.open_lick)
        self.testButton.clicked.connect(self.open_test)


    def open_mouse(self):
        #app = QtWidgets.QApplication(sys.argv)
        ID = self.mouse_id_select.currentText().split(' - ')[0]
        self.mousewin = mousewinActions(self.all_mice[ID])
        self.mousewin.show()

    def open_door(self):
        #app = QtWidgets.QApplication(sys.argv)
        try:
            self.doorwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.doorwin = doorwinActions(self.doors)
        self.doorwin.show()

    def open_lick(self):
        try:
            self.lickwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        #app = QtWidgets.QApplication(sys.argv)
        self.lickwin = lickwinActions(self.live_licks)
        self.lickwin.show()

    def open_test(self):
        #app = QtWidgets.QApplication(sys.argv)
        try:
            self.testwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        if self.all_tests:
            self.testwin = testwinActions(self.all_tests)
            self.testwin.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('No tests have been conducted yet')
            msg.exec()

class TeensyRead(QThread):
    def __init__(self, START_TIME, all_mice,doors,live_licks,all_tests):
        super(TeensyRead, self).__init__()
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.all_tests = all_tests
        self.START_TIME = START_TIME

    def run(self):
        startTeensyRead(self.START_TIME,self.all_mice,self.doors,self.live_licks,self.all_tests)