from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect

import sys
import os
os.system("pyuic5 -x mainwin.ui -o mainwin.py")
from mainwin import Ui_MainWindow


class MyActions(Ui_MainWindow):
    def __init__(self, title=" "):
        self.title = title
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


    def open_mouse(self):
        self.label_blah.setText("Submit button is pressed ")

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyActions("Main Window")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())