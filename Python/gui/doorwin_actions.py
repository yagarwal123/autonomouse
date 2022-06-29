from PyQt6 import QtCore, QtWidgets, QtGui
from gui.doorwin import Ui_doorWin

class doorwinActions(QtWidgets.QWidget, Ui_doorWin):
    def __init__(self,mutex,doors,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.doors = doors
        self.mutex = mutex
        self.title = "Doors"

        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.popTable())
        self.timer.start(1000) # refreshes window every 1s
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose) # deletes timer
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False) # indicates it is a secondary window
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # first column is fixed in size

    def popTable(self):
        self.mutex.lock()
        self.tableWidget.setRowCount(len(self.doors))
        for i,door in enumerate(self.doors):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(door[0])))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(door[1].get_id()))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(door[1].get_name()))
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(door[2])))
        self.mutex.unlock()