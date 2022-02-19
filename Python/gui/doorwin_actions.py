from PyQt6 import QtCore, QtWidgets
from gui.doorwin import Ui_doorWin

class doorwinActions(QtWidgets.QWidget, Ui_doorWin):
    def __init__(self,mutex,doors):
        super().__init__()
        self.setupUi(self)
        self.doors = doors
        self.mutex = mutex
        self.title = "Doors"

        self.setWindowTitle(self.title) # change title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.popTable())
        self.timer.start(1000)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents) 

    def popTable(self):
        self.mutex.lock()
        entries = len(self.doors)
        self.tableWidget.setRowCount(entries)
        for i in range(entries):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.doors[i][0])))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(self.doors[i][1].get_id()))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(self.doors[i][1].get_name()))
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(self.doors[i][2])))
        self.mutex.unlock()