from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect

#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.mousewin import Ui_mouseWin


class mousewinActions(QtWidgets.QWidget,Ui_mouseWin):
    def __init__(self, Mouse):
        super().__init__()
        self.setupUi(self)
        self.Mouse = Mouse
        self.title = str(Mouse.get_id()) + ' - ' + str(Mouse.get_name())

        # MainWindow.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title