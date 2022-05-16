from PyQt6 import QtCore, QtWidgets, QtGui

from gui.testwin import Ui_testWin

class testwinActions(QtWidgets.QWidget, Ui_testWin):
    def __init__(self,mutex,last_test,ser,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.last_test = last_test
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
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 


    def popData(self):
        if not vars(self.last_test): return
        self.mutex.lock()
        test = self.last_test
        self.m_name.setText(test.mouse.get_name())
        self.m_id.setText(test.mouse.get_id())
        self.test_start_time.setText(str(test.starting_time))
        self.weight_max.setText(str(max(test.weights)))
        if self.tableWidget.rowCount() != len(test.trials):
            self.tableWidget.setRowCount(len(test.trials))
            for i,trial in enumerate(test.trials):
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(trial.idx)))
                self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(trial.value)))
            #self.tableWidget.scrollToBottom()
        self.mutex.unlock()

    def give_reward(self):
        if not vars(self.last_test): return
        test = self.last_test
        if test.vid_recording:
            self.ser.write('Reward\n'.encode())
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('No mouse is in')
            msg.exec()

    def stop_test(self):
        if not vars(self.last_test): return
        test = self.last_test
        if not test.trials_over:
            test.trials_over = True
            self.ser.write('End\n'.encode())

    def manual_start_test(self):
        if not vars(self.last_test): return
        test = self.last_test
        if test.vid_recording and test.starting_time is None:
            self.ser.write('Manual Start\n'.encode())