from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect

import sys
import os
os.system(r"pyuic5 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py")
#from gui import mainwin
from gui.mainwin import Ui_MainWindow
from gui.mousewin_actions import mousewinActions
from gui.doorwin_actions import doorwinActions


class mainwinActions(Ui_MainWindow):
    def __init__(self, all_mice = {},doors=[]):
        self.all_mice = all_mice
        self.doors = doors
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

        self.myactions() # add actions for different buttons

    # define actions here
    def myactions(self):
        self.mouse_button.clicked.connect(self.open_mouse)
        self.doorButton.clicked.connect(self.open_door)


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

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwinActions("Main Window")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())