from PyQt6 import QtCore, QtWidgets, QtGui

from gui.odourwin import Ui_odourWin

class odourwinActions(QtWidgets.QWidget, Ui_odourWin):
    def __init__(self,mutex,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.mutex = mutex
        self.title = "Odour Pattern Generator"
        
        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)