from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QThread, QMutex
from PyQt6.QtWidgets import QMessageBox

import logging

from gui.mainwin import Ui_MainWindow
from gui.mousewin_actions import mousewinActions
from gui.doorwin_actions import doorwinActions
from gui.lickwin_actions import lickwinActions
from gui.testwin_actions import testwinActions
from start_teensy_read import startTeensyRead

logger = logging.getLogger(__name__)


class mainwinActions(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, START_TIME, all_mice,doors=[],live_licks=[],all_tests=[]):
        super().__init__()
        self.setupUi(self)
        self.title = 'Main Window'

        self.START_TIME = START_TIME
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.all_tests = all_tests
        self.experiment_paused = [False]

        self.mutex = QMutex()

        self.setWindowTitle(self.title) # change title

        #self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.worker = TeensyRead(self.mutex,self.START_TIME,self.all_mice,self.doors,self.live_licks,self.all_tests,self.experiment_paused)
        self.worker.start()
        self.myactions() # add actions for different buttons

        self.all_mousewin = []

        for id, m in self.all_mice.items():
            self.mouse_id_select.addItem(id + ' - ' + m.get_name())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        close = QMessageBox()
        close.setText("Do you want to end the experiment?")
        close.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        close = close.exec()

        if close == QMessageBox.StandardButton.Yes:
            a0.accept()
        else:
            a0.ignore()

    # define actions here
    def myactions(self):
        self.mouse_button.clicked.connect(self.open_mouse)
        self.doorButton.clicked.connect(self.open_door)
        self.lickButton.clicked.connect(self.open_lick)
        self.testButton.clicked.connect(self.open_test)
        self.pauseButton.clicked.connect(self.pause_exp)


    def open_mouse(self):
        #TODO: Think of a better way to handle this
        if len(self.all_mousewin) > 100:
            self.all_mousewin.clear()
        ID = self.mouse_id_select.currentText().split(' - ')[0]
        self.all_mousewin.append(mousewinActions(self.mutex,self.all_mice[ID]))
        self.all_mousewin[-1].show()

    def open_door(self):
        try:
            self.doorwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.doorwin = doorwinActions(self.mutex,self.doors)
        self.doorwin.show()

    def open_lick(self):
        try:
            self.lickwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.lickwin = lickwinActions(self.mutex,self.live_licks)
        self.lickwin.show()

    def open_test(self):
        try:
            self.testwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        if self.all_tests:
            self.testwin = testwinActions(self.mutex,self.all_tests)
            self.testwin.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('No tests have been conducted yet')
            msg.exec()

    def pause_exp(self):
        self.experiment_paused[0] = not self.experiment_paused[0]
        if self.experiment_paused[0]:       #Experiment is paused
            self.pauseButton.setText('Unpause Experiment')
            self.pauseLabel.setText('Experiment is now paused')
        else:                               #Experiment is not paused
            self.pauseButton.setText('Pause Experiment')
            self.pauseLabel.setText('Experiment is ongoing')


class TeensyRead(QThread):
    def __init__(self, mutex, START_TIME, all_mice,doors,live_licks,all_tests,experiment_paused):
        super(TeensyRead, self).__init__()
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.all_tests = all_tests
        self.START_TIME = START_TIME
        self.mutex = mutex
        self.experiment_paused = experiment_paused

    def run(self):
        startTeensyRead(self.mutex,self.START_TIME,self.all_mice,self.doors,self.live_licks,self.all_tests,self.experiment_paused)