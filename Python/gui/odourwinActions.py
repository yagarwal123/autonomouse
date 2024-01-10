from PyQt6 import QtCore, QtWidgets, QtGui

from gui.odourwin import Ui_odourWin

from pathlib import Path
from odour_gen import odour_gen2
import numpy as np
from functools import partial
from config import CONFIG


class odourwinActions(QtWidgets.QWidget, Ui_odourWin):
    set_pattern = []
    set_target = []
    def __init__(self,mutex,last_test,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.mutex = mutex
        self.title = "Odour Pattern Generator (Select input file or generate pattern)"
        self.pattern = np.zeros((1,15)) # stim pattern
        self.target = "1,2"
        self.trials = 1
        self.dir = CONFIG.application_path
        
        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        
        self.myactions()
        
    def myactions(self):  
        self.generateButton.clicked.connect(self.generateOdour)
        self.saveButton.clicked.connect(partial(self.savePattern,"pattern"))
        self.saveTargetButton.clicked.connect(partial(self.savePattern,"target"))
        self.selectFileButton.clicked.connect(partial(self.showDialog,"pattern"))
        self.selectTargetButton.clicked.connect(partial(self.showDialog,"target"))

    def savePattern(self, mode): # save pattern and target array
        S__File = QtWidgets.QFileDialog.getSaveFileName(None,'SaveTextFile',self.dir, "Text Files (*.txt)")
        # This will prevent you from an error if pressed cancel on file dialog.
        if S__File[0]: 
            if mode == 'pattern':
                np.savetxt(S__File[0], self.pattern, delimiter='\t', fmt='%i') # save as integer
            if mode == 'target':
                np.savetxt(S__File[0], self.target, delimiter='\t', fmt='%i') # save as integer
            else: pass
        
    @classmethod
    def update_pattern(cls, new_pattern):
        cls.set_pattern = new_pattern
        #print(cls.patterns)

    @classmethod
    def update_target(cls, new_target):
        cls.set_target = new_target
        #print(cls.patterns)
    
    @classmethod
    def return_pattern(cls):
        return cls.set_pattern

    @classmethod
    def return_target(cls):
        return cls.set_target

    def showDialog(self, mode):
        #home_dir = str(Path.home())
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.dir)

        if fname[0]:
            if mode == "pattern":
                self.fileDisp.setText(fname[0])
                self.pattern = np.loadtxt(fname[0], dtype=int, delimiter="\t")
                self.pattern.astype(int)
                self.model = TableModel(self.pattern)
                self.patternEdit.setModel(self.model)
                #print(self.pattern)
                odourwinActions.update_pattern(self.pattern)
            if mode == "target":
                self.targetFileDisp.setText(fname[0])
                self.target = np.loadtxt(fname[0], dtype=int, delimiter="\t")
                odourwinActions.update_target(self.target)
                self.target = str(self.target)
                self.targetDisp.setText(self.target)
            else: pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid file') 
            msg.exec()

    def generateOdour(self, last_test):
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
        prbArray = []
        if self.checkBox.isChecked(): # and self.TP1.text() != '': 
            target.append(0)
        prbArray.append(self.TP1.text())
        
        if self.checkBox_2.isChecked(): # and self.TP2.text() != '': 
            target.append(1)
        prbArray.append(self.TP2.text())
        
        if self.checkBox_3.isChecked():# and self.TP3.text() != '': 
            target.append(2)
        prbArray.append(self.TP3.text())
        
        if self.checkBox_4.isChecked():# and self.TP4.text() != '': 
            target.append(3)
        prbArray.append(self.TP4.text())
        
        if self.checkBox_5.isChecked():# and self.TP5.text() != '': 
            target.append(4)
        prbArray.append(self.TP5.text())
        
        if self.checkBox_6.isChecked():# and self.TP6.text() != '': 
            target.append(5)
        prbArray.append(self.TP6.text())
        
        if self.checkBox_7.isChecked():# and self.TP7.text() != '': 
            target.append(6)
        prbArray.append(self.TP7.text())
        
        if self.checkBox_8.isChecked():# and self.TP7.text() != '': 
            target.append(7)
        prbArray.append(self.TP8.text())
    
        self.target = np.asarray(target, dtype=int) 
        #target = list(map(int, target))
        #targetProb = list(map(float, targetProb))
        try:
            #prbArray = np.asarray(prbArray, dtype=float)
            prbArray = np.array(prbArray, dtype=np.float32)
        except:
            msg = QtWidgets.QMessageBox()
            msg.setText('Assign probability to all available odours') 
            msg.exec()
        if sum(nPrbArray)!=1 or (nPrbArray < 0).any() or round(sum(prbArray),2) !=1 or (prbArray < 0).any():      # has to add up to 1 in 2dp          
            msg = QtWidgets.QMessageBox()
            msg.setText('Probabilities must be non-negative and sum to 1') 
            msg.exec()
        elif np.count_nonzero(prbArray) < (np.max(np.where(nPrbArray))+1): # There need to be more odour choices than # of odours possible
            msg = QtWidgets.QMessageBox()
            msg.setText('More odours than available choices') 
            msg.exec()
        else:
            # call odour_gen function
            l = self.trialEdit.text()
            if l !='' and l.isnumeric():
                self.trials = int(l)
            self.pattern = odour_gen2(prbArray, nPrbArray, nChan=8, trialNo=self.trials)
            self.pattern.astype(int)
            #last_test.odours = self.pattern

            self.model = TableModel(self.pattern)
            odourwinActions.update_pattern(self.pattern)
            odourwinActions.update_target(self.target)
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


