from PyQt6 import QtCore, QtWidgets
from data_update import getLastTest
from gui.testwin import Ui_testWin

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,mutex,doors,ser):
        super().__init__()
        self.setupUi(self)
        self.doors = doors
        self.mutex = mutex
        self.ser = ser
        self.title = "Latest test"

        self.rewardButton.clicked.connect(self.give_reward)
        self.stopButton.clicked.connect(self.stop_test)

        self.setWindowTitle(self.title) # change title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.popData())
        self.timer.start(1000)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 


    def popData(self):
        self.mutex.lock()
        test = getLastTest(self.doors)
        if test is not None:
            self.m_name.setText(test.mouse.get_name())
            self.m_id.setText(test.mouse.get_id())
            self.test_start_time.setText(str(test.starting_time))
            self.tableWidget.setRowCount(len(test.trials))
            for i,trial in enumerate(test.trials):
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(trial.idx)))
                self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(trial.value)))
        self.mutex.unlock()

    def give_reward(self):
        test = getLastTest(self.doors)
        if test and test.vid_recording:
            self.ser.write('Reward\n'.encode())
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('No mouse is in')
            msg.exec()

    def stop_test(self):
        test = getLastTest(self.doors)
        if test and not test.trials_over:
            test.trials_over = True
            self.ser.write('End\n'.encode())