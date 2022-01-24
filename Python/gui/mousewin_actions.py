from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect

import sys
import os
#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.mousewin import Ui_mouseWin


class mousewinActions(Ui_mouseWin):
    def __init__(self, Mouse):
        self.Mouse = Mouse
        self.title = str(Mouse.get_id()) + ' - ' + str(Mouse.get_name())
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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Wid = QtWidgets.QWidget()
    ui = mousewinActions()
    ui.setupUi(Wid)
    Wid.show()
    sys.exit(app.exec_())