from PyQt6 import QtCore, QtWidgets

from gui.testwin import Ui_testWin

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,mutex,all_tests):
        super().__init__()
        self.setupUi(self)
        self.all_tests = all_tests
        self.mutex = mutex
        self.title = "Latest test"

        self.setWindowTitle(self.title) # change title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.popData())
        self.timer.start(1000)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 


    def popData(self):
        self.mutex.lock()
        test = self.all_tests[-1]
        self.m_name.setText(test.mouse.get_name())
        self.m_id.setText(test.mouse.get_id())
        self.test_start_time.setText(str(test.starting_time))
        self.tableWidget.setRowCount(len(test.trials))
        for i,trial in enumerate(test.trials):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(trial.idx)))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(trial.value)))
        self.mutex.unlock()