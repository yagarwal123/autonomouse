from PyQt6 import QtCore, QtWidgets
from gui.expwin import Ui_expWin
from ExperimentParameters import ExperimentParameters

class expwinActions(QtWidgets.QWidget, Ui_expWin):
    def __init__(self,mutex,experiment_parameters,all_mice):
        super().__init__()
        self.setupUi(self)
        self.experiment_parameters = experiment_parameters
        self.all_mice = all_mice
        self.mutex = mutex
        self.title = "Experiment Parameters"

        self.setWindowTitle(self.title) # change title

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

        self.liquidLineEdit.returnPressed.connect(self.changeliquidButton.click)
        self.lickLineEdit.returnPressed.connect(self.changelickButton.click)
        self.waittimeLineEdit.returnPressed.connect(self.changewaittimeButton.click)
        self.mouseLimLineEdit.returnPressed.connect(self.changeMouseLimButton.click)

        self.myactions()

    # define actions here
    def myactions(self):  
        self.pauseButton.clicked.connect(self.pause_exp)
        self.changeliquidButton.clicked.connect(self.change_liquid)
        self.changelickButton.clicked.connect(self.change_lick)
        self.changewaittimeButton.clicked.connect(self.change_waittime)
        self.changeMouseLimButton.clicked.connect(self.change_mouse_lim)

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

    def pause_exp(self):
        self.experiment_parameters.paused = not self.experiment_parameters.paused
        if self.experiment_parameters.paused:       #Experiment is paused
            self.pauseButton.setText('Unpause Experiment')
            self.pauseLabel.setText('Experiment is now paused')
        else:                               #Experiment is not paused
            self.pauseButton.setText('Pause Experiment')
            self.pauseLabel.setText('Experiment is ongoing')