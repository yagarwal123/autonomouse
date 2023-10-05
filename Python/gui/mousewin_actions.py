from PyQt6 import QtCore, QtWidgets, QtGui
from multiprocessing import Process
import matplotlib.pyplot
import logging
import numpy as np
from gui.mousewin import Ui_mouseWin
from analysis import analysis_window
import os
import pickle
from config import CONFIG

logger = logging.getLogger(__name__)

class mousewinActions(QtWidgets.QWidget, Ui_mouseWin):
    def __init__(self,mutex,mouse):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.mouse = mouse
        self.mutex = mutex
        self.title = self.mouse.get_id() +  ' - ' + self.mouse.get_name()

        self.setWindowTitle(self.title) # change title
        self.pltax = None
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatedisplays) # called every 1s
        self.timer.start(1000)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

        self.liquidLineEdit.returnPressed.connect(self.changeliquidButton.click)
        self.lickLineEdit.returnPressed.connect(self.changelickButton.click)
        self.waittimeLineEdit.returnPressed.connect(self.changewaittimeButton.click)
        self.punishtimeLineEdit.returnPressed.connect(self.changepunishtimeButton.click)
        self.testLimLineEdit.returnPressed.connect(self.changeTestLimButton.click)
        self.trialLimLineEdit.returnPressed.connect(self.changeTrialLimButton.click)
        self.respLineEdit.returnPressed.connect(self.changeRespButton.click)
        self.stimProbLineEdit.returnPressed.connect(self.changeStimButton.click)

        self.myactions()

    # define actions here
    def myactions(self):  
        self.changeliquidButton.clicked.connect(self.change_liquid)
        self.changelickButton.clicked.connect(self.change_lick)
        self.changewaittimeButton.clicked.connect(self.change_waittime)
        self.changepunishtimeButton.clicked.connect(self.change_punishtime)
        self.changeTestLimButton.clicked.connect(self.change_testlim)
        self.changeTrialLimButton.clicked.connect(self.change_triallim)
        self.showAnalysisButton.clicked.connect(self.analysis_win)
        self.changeRespButton.clicked.connect(self.change_resp)
        self.changeStimButton.clicked.connect(self.change_stim_prob)
        self.saveButton.clicked.connect(self.save_parameters)

    def save_parameters(self):
        fileFolder = 'MouseObjects'
        if not os.path.exists(fileFolder):
            os.makedirs(fileFolder)
        filename = os.path.join(CONFIG.application_path, fileFolder, f'{self.mouse.get_id()}.obj')
        filehandler = open(filename, 'wb') 
        pickle.dump(self.mouse, filehandler)
        filehandler.close()   

    def change_liquid(self):
        l = self.liquidLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.liq_am_disp.setText(l)
            self.mouse.liquid_amount = int(l)
            self.liquidLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()
        

    def change_lick(self):
        l = self.lickLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.lick_thresh_disp.setText(l)
            self.mouse.lick_threshold = int(l)
            self.lickLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_waittime(self):
        l = self.waittimeLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.waittime_disp.setText(l)
            self.mouse.waittime = int(l)
            self.waittimeLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_punishtime(self):
        l = self.punishtimeLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.punishtime_disp.setText(l)
            self.mouse.punishtime = int(l)
            self.punishtimeLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_testlim(self):
        l = self.testLimLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.test_lim_disp.setText(l)
            self.mouse.test_limit = int(l)
            self.testLimLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_triallim(self):
        l = self.trialLimLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            if l=='0':
                self.trial_lim_disp.setText(None) # input limit of 0 means no limit
                self.mouse.trial_lim = None
            else:
                self.trial_lim_disp.setText(l)
                self.mouse.trial_lim = int(l)
            self.trialLimLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_resp(self):
        l = self.respLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.resp_disp.setText(l)
            self.mouse.response_time = int(l)
            self.respLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_stim_prob(self):
        l = self.stimProbLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.stim_prob_disp.setText(l)
            self.mouse.stim_prob = int(l)
            self.stimProbLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def pltgraph(self): # weight: matplotlib here (can rotate label) and pyqt in licks
        self.mutex.lock()
        if self.pltax:
            self.pltax.clear()
        
        x = [0]
        x_lab = ['Start']
        y = [self.mouse.get_init_weight()]
        for t in self.mouse.test_times:
            if t is None: continue
            x.append(t.millis)
            x_lab.append(str(t))
        y = y + self.mouse.final_weights # max weight from a list in test object
        y = [float(i) for i in y]

        self.pltax = self.plotWid.canvas.ax
        #assert len(np.unique(x)) == len(x_lab)
        matplotlib.pyplot.setp(self.pltax, xticks=np.unique(x), xticklabels=x_lab)
        matplotlib.pyplot.setp(self.pltax.xaxis.get_majorticklabels(), rotation=90)
        self.pltax.plot(x,y,'o')
        self.pltax.set_xlim(left=0)
        self.pltax.set_ylabel('Weight (g)')

        self.plotWid.canvas.draw()
        self.mutex.unlock()

    def updatedisplays(self):
        self.liq_am_disp.setText(str(self.mouse.liquid_amount))
        self.lick_thresh_disp.setText(str(self.mouse.lick_threshold))
        self.waittime_disp.setText(str(self.mouse.waittime))
        self.punishtime_disp.setText(str(self.mouse.punishtime))
        self.test_lim_disp.setText(str(self.mouse.test_limit))
        self.trial_lim_disp.setText(str(self.mouse.trial_lim))
        self.test_no_disp.setText(str(self.mouse.get_tests_today()))
        self.resp_disp.setText(str(self.mouse.response_time))
        self.stim_prob_disp.setText(str(self.mouse.stim_prob))
        if self.test_select.count() != len(self.mouse.test_ids):
            self.test_select.clear()
            for id in self.mouse.test_ids:
                self.test_select.addItem(id)
            self.pltgraph()

    def analysis_win(self):
        test_id = self.test_select.currentText()
        if test_id:
            try:
                f = 31 - self.speedSlider.value() # 0-30
                p = Process(target=analysis_window,args=(test_id,f))
                p.start()
            except Exception as e:
                logger.error(f'Error in opening analysis window - Test ID {test_id}')
            #analysis_window(test_id)