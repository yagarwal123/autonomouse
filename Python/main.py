import logging
import serial
import datetime
from PyQt6 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys
#import multiprocessing

from Mouse import Mouse
#from start_teensy_read import startTeensyRead

import os
os.system(r"pyuic6 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py")
os.system(r"pyuic6 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
os.system(r"pyuic6 -x ./Python/gui/doorwin.ui -o ./Python/gui/doorwin.py")
os.system(r"pyuic6 -x ./Python/gui/lickwin.ui -o ./Python/gui/lickwin.py")
os.system(r"pyuic6 -x ./Python/gui/testwin.ui -o ./Python/gui/testwin.py")

MICE_INIT_INFO = {'A11111':['Stuart',67],
              'A22222': ['Little',45],
              '0007A0F7C4': ['Real',27.4]}

START_TIME = datetime.datetime.now()

#Uncomment
#ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

#Inititate Mice
all_mice = {}
for id, info in MICE_INIT_INFO.items():
    all_mice[id] = Mouse(id,info[0],info[1])

#Comment out
doors = [
    [12367, all_mice['A22222'], 1],
    [33333, all_mice['A11111'], 2]
    ]
live_licks = [0,0,0,7,100,60]
all_tests = []


if __name__ == "__main__":
    #startGUI(START_TIME,all_mice,doors,live_licks,all_tests)
    app = QtWidgets.QApplication(sys.argv)
    mainwin = mainwinActions(START_TIME,all_mice, doors,live_licks,all_tests)
    #mainwin = mainwinActions(START_TIME,all_mice)
    mainwin.show()
    sys.exit(app.exec())
    
    

