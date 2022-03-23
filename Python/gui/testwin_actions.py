from PyQt6 import QtCore, QtWidgets

from gui.testwin import Ui_testWin

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,mutex,all_tests,ser,pos=None):
        super().__init__()
        self.setupUi(self)
        self.all_tests = all_tests
        self.mutex = mutex
        self.ser = ser
        self.title = "Latest test"

        self.rewardButton.clicked.connect(self.give_reward)
        self.stopButton.clicked.connect(self.stop_test)
        self.manStartButton.clicked.connect(self.manual_start_test)

        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.popData())
        self.timer.start(2000)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 


    def popData(self):
        if not self.all_tests: return
        self.mutex.lock()
        test = self.all_tests[-1]
        self.m_name.setText(test.mouse.get_name())
        self.m_id.setText(test.mouse.get_id())
        self.test_start_time.setText(str(test.starting_time))
        self.tableWidget.setRowCount(len(test.trials))
        for i,trial in enumerate(test.trials):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(trial.idx)))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(trial.value)))
        #self.tableWidget.scrollToBottom()
        self.mutex.unlock()

    def give_reward(self):
        if not self.all_tests: return
        test = self.all_tests[-1]
        if test.vid_recording:
            self.ser.write('Reward\n'.encode())
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('No mouse is in')
            msg.exec()

    def stop_test(self):
        if not self.all_tests: return
        test = self.all_tests[-1]
        if not test.trials_over:
            test.trials_over = True
            self.ser.write('End\n'.encode())

    def manual_start_test(self):
        if not self.all_tests: return
        test = self.all_tests[-1]
        if test.vid_recording and test.starting_time is None:
            self.ser.write('Manual Start\n'.encode())