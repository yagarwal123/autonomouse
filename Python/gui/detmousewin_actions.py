from PyQt6 import QtCore, QtWidgets, QtGui

from gui.detmousewin import Ui_detmouseWin

class detmousewinActions(QtWidgets.QWidget, Ui_detmouseWin):
    def __init__(self,mutex,all_mice,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.all_mice = all_mice
        self.mutex = mutex
        self.title = "Mouse details"

        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title
        
        self.popData()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers) # to make table non editable
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) # make table size with window size


    def popData(self): # show all mouse data in mouse details window
        self.mutex.lock()

        self.tableWidget.setRowCount(len(self.all_mice))
        for i,mouse in enumerate(self.all_mice.values()):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(mouse.get_id())))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(mouse.get_name())))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(mouse.get_init_weight())))
        #self.tableWidget.scrollToBottom()
        self.mutex.unlock()