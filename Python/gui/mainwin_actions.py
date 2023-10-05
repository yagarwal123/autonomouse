from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QThread, QMutex, QPoint, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

import logging
import os
from Test import Test

from gui.mainwin import Ui_MainWindow
from gui.mousewin_actions import mousewinActions
from gui.doorwin_actions import doorwinActions
from gui.lickwin_actions import lickwinActions
from gui.testwin_actions import testwinActions
from gui.expwin_actions import expwinActions
from gui.detmousewin_actions import detmousewinActions
from gui.odourwinActions import odourwinActions
from start_teensy_read import startTeensyRead
import rasp_camera
from config import CONFIG
from ExperimentParameters import ExperimentParameters

logger = logging.getLogger(__name__)


class mainwinActions(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, ser, START_TIME, all_mice,doors=[],live_licks=[],last_test=Test()):
        super().__init__() # calls init of the UI main window
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.title = 'Main Window'
        self.ser = ser
        self.START_TIME = START_TIME
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.last_test = last_test
        self.experiment_parameters = ExperimentParameters()

        self.mutex = QMutex() # mutex object, need to lock whenever you are editing an object

        self.setWindowTitle(self.title) # change title

        #self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.worker = TeensyRead(self.ser,self.mutex,self.START_TIME,self.all_mice,self.doors,self.live_licks,self.last_test,self.experiment_parameters)
        self.worker.test_start_signal.connect(self.open_all_win) # open window when the signal "emits" in data_update.py
        self.worker.start() # runs run fucntion in teensyread
        self.myactions() # add actions for different buttons

        self.all_mousewin = [] # list of pointers to all the mouse windows because we dont want to override everytime we open a new window

        for id, m in self.all_mice.items():
            self.mouse_id_select.addItem(f'{id} - {m.get_name()}') # drop down value

        if CONFIG.OPEN_WINDOWS:
            self.open_all_win()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        close = QMessageBox()
        close.setText("Do you want to end the experiment?")
        close.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        close = close.exec()

        if close == QMessageBox.StandardButton.Yes:
            self.worker.terminate() # self.worker is the teensyread thread
            if CONFIG.TEENSY:
                self.worker.wait() # wait for the thread to be terminated 
                self.ser.close()
            rasp_camera.close_record()
            a0.accept() # close window
        else:
            a0.ignore() # not close window

    # define actions here
    def myactions(self): # connect button to function - do it whenever you create new button
        self.mouse_button.clicked.connect(lambda: self.open_mouse())
        self.doorButton.clicked.connect(lambda: self.open_door())
        self.lickButton.clicked.connect(lambda: self.open_lick())
        self.testButton.clicked.connect(lambda: self.open_test())
        self.expButton.clicked.connect(lambda: self.open_exp())
        self.cameraButton.clicked.connect(lambda: self.open_cam())
        self.openAllButton.clicked.connect(lambda: self.open_all_win())
        self.detMouseButton.clicked.connect(lambda: self.open_detmouse())
        self.odour_button.clicked.connect(lambda: self.open_odour())


    def open_mouse(self):
        #TODO: Think of a better way to handle this
        if len(self.all_mousewin) > 100: # when the list gets more than 100 close all other windows - user has to open them again but whatever
            self.all_mousewin.clear()
        ID = self.mouse_id_select.currentText().split(' - ')[0]
        self.all_mousewin.append(mousewinActions(self.mutex,self.all_mice[ID]))
        self.all_mousewin[-1].show()

    def open_door(self,pos=None):
        try: # deletes previous window before opening a new one
            self.doorwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.doorwin = doorwinActions(self.mutex,self.doors,pos)
        self.doorwin.show()

    def open_lick(self,pos=None):
        try:
            self.lickwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.lickwin = lickwinActions(self.mutex,self.live_licks,pos)
        self.lickwin.show()

    def open_test(self,pos=None):
        try:
            self.testwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.testwin = testwinActions(self.mutex,self.last_test,self.ser,pos)
        self.testwin.show()

    def open_exp(self,pos=None):
        try:
            self.expwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.expwin = expwinActions(self.mutex,self.experiment_parameters,self.all_mice,self.ser,self.last_test,pos)
        self.expwin.show()

    def open_detmouse(self,pos=None):
        try:
            self.detmouse.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.detmouse = detmousewinActions(self.mutex,self.all_mice,pos)
        self.detmouse.show()

    def open_cam(self):
        os.system("start microsoft.windows.camera:")
    
    def open_odour(self, pos=None):
        try:
            self.odourwin.close()
        except (RuntimeError, AttributeError) as e:
            pass
        self.odourwin = odourwinActions(self.mutex,self.last_test,pos)
        self.odourwin.show()
        
    def open_all_win(self):
        self.open_exp(QPoint(0,0))
        self.open_lick(QPoint(380,0))
        self.open_door(QPoint(756,0))
        self.open_test(QPoint(1182,0))
        self.open_cam()
        self.open_detmouse(QPoint(0,292))
        self.open_odour(QPoint(0,450))

class TeensyRead(QThread): # inherit QThread class

    test_start_signal = pyqtSignal() # communicate between threads

    def __init__(self, ser, mutex, START_TIME, all_mice,doors,live_licks,last_test,experiment_parameters):
        super(TeensyRead, self).__init__() # calls qthread class init
        self.ser = ser
        self.all_mice = all_mice
        self.doors = doors
        self.live_licks = live_licks
        self.last_test = last_test
        self.START_TIME = START_TIME
        self.mutex = mutex
        self.experiment_parameters = experiment_parameters

    def run(self): # all objects are passed to startteensyread
        startTeensyRead(self.ser, self.mutex,self.START_TIME,self.all_mice,self.doors,self.live_licks,self.last_test,self.experiment_parameters,self.test_start_signal)