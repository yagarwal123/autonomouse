from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect

import sys
import os
os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.mousewin import Ui_Dialog


class mousewinActions(Ui_Dialog):
    def __init__(self, title=" "):
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150

    # update setupUi
    def setupUi(self, QDialog):
        super().setupUi(QDialog)
        # MainWindow.resize(400, 300) # do not modify it
        QDialog.move(self.left, self.top)  # set location for window
        QDialog.setWindowTitle(self.title) # change title


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = mousewinActions("Mouse Details")
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())