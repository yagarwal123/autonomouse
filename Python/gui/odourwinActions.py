from PyQt6 import QtCore, QtWidgets, QtGui

from gui.odourwin import Ui_odourWin

from pathlib import Path
from odour_gen import odour_gen
import numpy as np

class odourwinActions(QtWidgets.QWidget, Ui_odourWin):
    def __init__(self,mutex,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.mutex = mutex
        self.title = "Odour Pattern Generator (Select input file or generate pattern)"
        self.pattern = [] # stim pattern
        self.trials = 5
        
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
            #f = open(fname[0], 'r')
            self.fileDisp.setText(fname[0])
            #with f:
                #self.pattern = f.read()
                #self.patternEdit.setText(self.pattern)
            self.pattern = np.loadtxt(fname[0], dtype=int, delimiter="\t")
            self.model = TableModel(self.pattern)
            self.patternEdit.setModel(self.model)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid file') 
            msg.exec()
            

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
        #nPrbArray = list(map(float, nPrbArray))
        nPrbArray = np.asarray(nPrbArray, dtype=float) 
        
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
    
        target = np.asarray(target, dtype=int) 
        #target = list(map(int, target))
        #targetProb = list(map(float, targetProb))
        targetProb = np.asarray(targetProb, dtype=float) 
        
        if sum(nPrbArray)!=1 or (nPrbArray < 0).any():        # has to add up to 1          
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid odour probability input') 
            msg.exec()
            
        elif (targetProb < 0).any():       # doesn't have to add up to 1           
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid target input') 
            msg.exec()
        else:
            # call odour_gen function
            l = self.trialEdit.text()
            if l !='' and l.isnumeric():
                self.trials = int(l)
            self.pattern = odour_gen(target, targetProb, nPrbArray, nChan=8, trialNo=self.trials)
            # self.patternEdit.setText(self.pattern)
            self.model = TableModel(self.pattern)
            self.patternEdit.setModel(self.model)
            self.fileDisp.setText('')

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            # Note: self._data[index.row()][index.column()] will also work
            value = self._data[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]


