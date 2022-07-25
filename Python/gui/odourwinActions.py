from PyQt6 import QtCore, QtWidgets, QtGui

from gui.odourwin import Ui_odourWin

from pathlib import Path
import odour_gen
import numpy as np

class odourwinActions(QtWidgets.QWidget, Ui_odourWin):
    def __init__(self,mutex,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.mutex = mutex
        self.title = "Odour Pattern Generator (Select input file or generate pattern)"
        
        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        
        self.myactions()
        
    def myactions(self):  
        self.selectFileButton.clicked.connect(self.showDialog)
        self.generateButton.clicked.connect(self.generateOdour)
        
    
    def showDialog(self):

        home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            f = open(fname[0], 'r')
            self.fileDisp.setText(fname[0])
            with f:
                data = f.read()
                self.patternEdit.setText(data)

    def generateOdour(self):
        # probability array for the number of odours
        nPrbArray = [0,0,0,0,0,0,0,0]
        if self.p1.text() != '':
            nPrbArray[0] = self.p1.text()
        if self.p2.text() != '':
            nPrbArray[1] = self.p2.text()
        if self.p3.text() != '':
            nPrbArray[2] = self.p3.text()
        if self.p4.text() != '':
            nPrbArray[3] = self.p4.text()
        if self.p5.text() != '':
            nPrbArray[4] = self.p5.text()
        if self.p6.text() != '':
            nPrbArray[5] = self.p6.text()
        if self.p7.text() != '':
            nPrbArray[6] = self.p7.text()
        if self.p8.text() != '':
            nPrbArray[7] = self.p8.text()
        nPrbArray = np.asarray(nPrbArray, dtype=float) # need to fill out all the boxes even if p=0
        if sum(nPrbArray)!=1:                   #Only number np.isnan(nPrbArray).any() 
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid odour probability input') 
            msg.exec()
        
        # make the target array
        target = []
        targetProb = []
        if self.checkBox.isChecked() and self.TP1.text() != '': 
            target.append(0)
            targetProb.append(self.TP1.text())
        if self.checkBox_2.isChecked() and self.TP2.text() != '': 
            target.append(1)
            targetProb.append(self.TP2.text())
        if self.checkBox_3.isChecked() and self.TP3.text() != '': 
            target.append(2)
            targetProb.append(self.TP3.text())
        if self.checkBox_4.isChecked() and self.TP4.text() != '': 
            target.append(3)
            targetProb.append(self.TP4.text())
        if self.checkBox_5.isChecked() and self.TP5.text() != '': 
            target.append(4)
            targetProb.append(self.TP5.text())
        if self.checkBox_6.isChecked() and self.TP6.text() != '': 
            target.append(5)
            targetProb.append(self.TP6.text())
        if self.checkBox_7.isChecked() and self.TP7.text() != '': 
            target.append(6)
            targetProb.append(self.TP7.text())
        if self.checkBox_8.isChecked() and self.TP7.text() != '': 
            target.append(7)
            targetProb.append(self.TP8.text())
    
        target = np.asarray(target, dtype=float) 
        targetProb = np.asarray(targetProb, dtype=float) 
        if sum(targetProb)!=1:                  
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid target input') 
            msg.exec()
        
        # call odour_gen function
        