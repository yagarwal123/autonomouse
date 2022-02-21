import logging.config
from logging_conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

logging.getLogger('matplotlib').setLevel(logging.INFO)
#Optional - matplotlib spams a lot of debugs, so setting its level to info

import os
os.system(r"pyuic6 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py")
os.system(r"pyuic6 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
os.system(r"pyuic6 -x ./Python/gui/doorwin.ui -o ./Python/gui/doorwin.py")
os.system(r"pyuic6 -x ./Python/gui/lickwin.ui -o ./Python/gui/lickwin.py")
os.system(r"pyuic6 -x ./Python/gui/testwin.ui -o ./Python/gui/testwin.py")

import logging
import datetime
from PyQt6 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys
import serial

from Mouse import Mouse
from myTime import myTime

MICE_INIT_INFO = {'A11111':['Stuart',67],
              'A22222': ['Little',45],
              '0007A0F7C4': ['Real',27.4]}

START_TIME = datetime.datetime.now()


if __name__ == "__main__":
    #Inititate Mice
    all_mice = {}
    for id, info in MICE_INIT_INFO.items():
        all_mice[id] = Mouse(id,info[0],info[1])

    #Comment out
    doors = [
        [myTime(START_TIME,12367), all_mice['A22222'], 1],
        [myTime(START_TIME,33333), all_mice['A11111'], 2]
        ]
    live_licks = [0,0,0,7,100,60]
    all_tests = []

    #ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
    #ser = serial.Serial('/dev/cu.usbmodem105683101', 9600)
    ser = serial.Serial('COM4', 9600)
    #ser = None

    app = QtWidgets.QApplication(sys.argv)
    mainwin = mainwinActions(ser,START_TIME,all_mice, doors,live_licks,all_tests)
    #mainwin = mainwinActions(START_TIME,all_mice)
    mainwin.show()
    sys.exit(app.exec())
    
    

