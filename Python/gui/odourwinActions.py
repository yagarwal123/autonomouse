from PyQt6 import QtCore, QtWidgets, QtGui

from gui.odourwin import Ui_odourWin

from pathlib import Path

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
        
        self.myactions()
        
    def myactions(self):  
        self.selectFileButton.clicked.connect(self.showDialog)
    
    def showDialog(self):

        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            f = open(fname[0], 'r')
            self.fileDisp.setText(fname[0])
            with f:
                data = f.read()
                self.patternEdit.setText(data)
