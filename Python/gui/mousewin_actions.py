from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect

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
    def setupUi(self, Widget):
        super().setupUi(Widget)
        # MainWindow.resize(400, 300) # do not modify it
        Widget.move(self.left, self.top)  # set location for window
        Widget.setWindowTitle(self.title) # change title