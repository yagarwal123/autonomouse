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

        self.links = {self.changeliquidButton:[self.liquidLineEdit,self.liq_am_disp,"liquid\n"],
                    self.changelickButton:[self.lickLineEdit,self.lick_thresh_disp, "th\n" ],
                    self.changewaittimeButton:[self.waittimeLineEdit,self.waittime_disp,"wait\n"],
                    self.changepunishtimeButton:[self.punishtimeLineEdit,self.punishtime_disp,"punish\n"],
                    self.changeRespButton:[self.respLineEdit,self.resp_disp,"resp\n"],
                    self.changeStimButton:[self.stimProbLineEdit,self.stim_prob_disp,"stim\n"]
        }
        for but,vals in self.links.items():
            #but.clicked.connect(lambda:self.change_param(but))
            vals[0].returnPressed.connect(but.click)

        self.changeliquidButton.clicked.connect(lambda:self.change_param(self.changeliquidButton))
        self.changelickButton.clicked.connect(lambda:self.change_param(self.changelickButton))
        self.changewaittimeButton.clicked.connect(lambda:self.change_param(self.changewaittimeButton))
        self.changepunishtimeButton.clicked.connect(lambda:self.change_param(self.changepunishtimeButton))
        self.changeRespButton.clicked.connect(lambda:self.change_param(self.changeRespButton))
        self.changeStimButton.clicked.connect(lambda:self.change_param(self.changeStimButton))

        if vars(self.last_test) and self.last_test.vid_recording:
            self.liq_am_disp.setText(str(self.last_test.test_parameters.liquid_amount[-1]))
            self.lick_thresh_disp.setText(str(self.last_test.test_parameters.lick_threshold[-1]))
            self.waittime_disp.setText(str(self.last_test.test_parameters.waittime[-1]))
            self.punishtime_disp.setText(str(self.last_test.test_parameters.punishtime[-1]))
            self.resp_disp.setText(str(self.last_test.test_parameters.response_time[-1]))
            self.stim_prob_disp.setText(str(self.last_test.test_parameters.stim_prob[-1]))

    def popData(self):
        if not vars(self.last_test): return
        self.mutex.lock()
        test = self.last_test
        self.m_name.setText(test.get_mouse().get_name())
        self.m_id.setText(test.get_mouse().get_id())
        self.test_start_time.setText(str(test.starting_time))
        self.weight_max.setText(str(max(test.weights)))
        self.trial_lim.setText(str(test.trial_lim))
        #if self.tableWidget.rowCount() != len(test.trials):
        self.tableWidget.setRowCount(len(test.trials))
        
        if test.trials and (self.tableWidget.columnCount() != 2+len(test.trials[0].stimuli)):
            self.tableWidget.setColumnCount(2+len(test.trials[0].stimuli))
            h = ['-']*(len(self.last_test.trials[0].stimuli)-1)
            self.tableWidget.setHorizontalHeaderLabels(['Trial','Time','Stimuli']+h)
        for i,trial in enumerate(test.trials):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(trial.idx)))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(trial.value)))
            self.add_row(trial.stimuli,i,2)
            #self.tableWidget.scrollToBottom()
        self.mutex.unlock()

    def give_reward(self):
        if not vars(self.last_test): return
        test = self.last_test        
        if test.vid_recording:
            self.ser.write('Reward\n'.encode())
        else:
            self.ser.write('Reward\n'.encode())
            #msg = QtWidgets.QMessageBox()
            #msg.setText('No mouse is in')
            #msg.exec()

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

    def add_row(self,entries,row,start_column=0):
        for i,e in enumerate(entries):
            self.tableWidget.setItem(row,start_column+i,QtWidgets.QTableWidgetItem(str(e)))

    def change_param(self,but): # main function for changing param
        if not vars(self.last_test) or not self.last_test.vid_recording:
            msg = QtWidgets.QMessageBox()
            msg.setText('No test ongoing')
            msg.exec()
            return
        vals = self.links[but]
        l = vals[0].text()
        if l.isnumeric():                   #Only positive integers (0-9)
            vals[1].setText(l)
            vals[0].clear()
            self.ser.write( ( vals[2] ).encode() )
            self.ser.write( ( l + "\n" ).encode() )
            self.update_test_para(vals[2],int(l))
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def update_test_para(self,msg,l):
        if msg == "liquid\n":
            self.last_test.test_parameters.liquid_amount.append(l)
        elif msg == "th\n":
            self.last_test.test_parameters.lick_threshold.append(l)
        elif msg == "wait\n":
            self.last_test.test_parameters.waittime.append(l)
        elif msg == "punish\n":
            self.last_test.test_parameters.punishtime.append(l)
        elif msg == "resp\n":
            self.last_test.test_parameters.response_time.append(l)
        elif msg == "stim\n":
            self.last_test.test_parameters.stim_prob.append(l)