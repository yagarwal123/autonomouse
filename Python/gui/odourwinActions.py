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
        nPrbArray[0] = self.p1.text()
        nPrbArray[1] = self.p2.text()
        nPrbArray[2] = self.p3.text()
        nPrbArray[3] = self.p4.text()
        nPrbArray[4] = self.p5.text()
        nPrbArray[5] = self.p6.text()
        nPrbArray[6] = self.p7.text()
        nPrbArray[7] = self.p8.text()
        nPrbArray = np.asarray(nPrbArray, dtype=float) # need to fill out all the boxes even if p=0
        if sum(nPrbArray)!=1:                   #Only number np.isnan(nPrbArray).any() 
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid odour probability input') 
            msg.exec()
        
        # make the target array
        target = []
        if self.checkBox.isChecked(): target.append(0)
        if self.checkBox_2.isChecked(): target.append(1)
        if self.checkBox_3.isChecked(): target.append(2)
        if self.checkBox_4.isChecked(): target.append(3)
        if self.checkBox_5.isChecked(): target.append(4)
        if self.checkBox_6.isChecked(): target.append(5)
        if self.checkBox_7.isChecked(): target.append(6)
        if self.checkBox_8.isChecked(): target.append(7)
        
        # make target probability array
        targetProb = []
        for i in target:
            # temp = self.TP1.text()
            #name = ['TP{}'.format(i)]
            temp = self."TP"+str(i).text() # TODO: convert entered string into float
            if temp.isnumeric() and temp<1:
                targetProb.append(temp)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setText('Invalid target probability input') 
                msg.exec()
        # call odour_gen function
        