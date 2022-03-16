from PyQt6 import QtCore, QtWidgets
from gui.expwin import Ui_expWin
from ExperimentParameters import ExperimentParameters

class expwinActions(QtWidgets.QWidget, Ui_expWin):
    def __init__(self,mutex,experiment_parameters,all_mice,ser,all_tests):
        super().__init__()
        self.setupUi(self)
        self.experiment_parameters = experiment_parameters
        self.all_mice = all_mice
        self.mutex = mutex
        self.ser = ser
        self.all_tests = all_tests
        self.title = "Experiment Parameters"

        self.setWindowTitle(self.title) # change title

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

        self.liquidLineEdit.returnPressed.connect(self.changeliquidButton.click)
        self.lickLineEdit.returnPressed.connect(self.changelickButton.click)
        self.waittimeLineEdit.returnPressed.connect(self.changewaittimeButton.click)
        self.mouseLimLineEdit.returnPressed.connect(self.changeMouseLimButton.click)
        self.mouseRespLineEdit.returnPressed.connect(self.changeMouseRespButton.click)

        if self.experiment_parameters.paused:
            self.pauseButton.setText('Unpause Experiment')
            self.pauseLabel.setText('Experiment is now paused')
        else:
            self.pauseButton.setText('Pause Experiment')
            self.pauseLabel.setText('Experiment is ongoing')

        if self.experiment_parameters.valve_open:
            self.refillButton.setText('Stop Refill')
            self.refillLabel.setText('Valve is now open')
        else:
            self.refillButton.setText('Refill')
            self.refillLabel.setText('Valve is now closed')

        self.myactions()

    # define actions here
    def myactions(self):  
        self.pauseButton.clicked.connect(self.pause_exp)
        self.changeliquidButton.clicked.connect(self.change_liquid)
        self.changelickButton.clicked.connect(self.change_lick)
        self.changewaittimeButton.clicked.connect(self.change_waittime)
        self.changeMouseLimButton.clicked.connect(self.change_mouse_lim)
        self.changeMouseRespButton.clicked.connect(self.change_mouse_resp)
        self.refillButton.clicked.connect(self.refill)

    def change_liquid(self):
        l = self.liquidLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            ExperimentParameters.update_all_mice_liquid(self.all_mice,int(l))
            self.liquidLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()
        

    def change_lick(self):
        l = self.lickLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            ExperimentParameters.update_all_mice_lick(self.all_mice,int(l))
            self.lickLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_waittime(self):
        l = self.waittimeLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            ExperimentParameters.update_all_mice_waittime(self.all_mice,int(l))
            self.waittimeLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_mouse_lim(self):
        l = self.mouseLimLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            ExperimentParameters.update_all_mice_limit(self.all_mice,int(l))
            self.mouseLimLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_mouse_resp(self):
        l = self.mouseRespLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            ExperimentParameters.update_all_mice_resp(self.all_mice,int(l))
            self.mouseRespLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def pause_exp(self):
        self.experiment_parameters.paused = not self.experiment_parameters.paused
        if self.experiment_parameters.paused:       #Experiment is paused
            self.pauseButton.setText('Unpause Experiment')
            self.pauseLabel.setText('Experiment is now paused')
        else:                               #Experiment is not paused
            self.pauseButton.setText('Pause Experiment')
            self.pauseLabel.setText('Experiment is ongoing')

    def refill(self):
        self.experiment_parameters.valve_open = not self.experiment_parameters.valve_open
        if not self.all_tests or not self.all_tests[-1].ongoing:
            if self.experiment_parameters.valve_open:      
                if not self.experiment_parameters.paused:
                    self.pause_exp()
                self.refillButton.setText('Stop Refill')
                self.refillLabel.setText('Valve is now open')
                self.ser.write('Refill\n'.encode())
            else:                              
                self.refillButton.setText('Refill')
                self.refillLabel.setText('Valve is now closed')
                self.ser.write('Stop\n'.encode())
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('A test is ongoing, please wait till it finishes')
            msg.exec()
