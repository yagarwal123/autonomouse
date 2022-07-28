import subprocess
import logging.config
import traceback
from time import sleep
from unittest.mock import Mock
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

import datetime
from PyQt6 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys
import serial
import multiprocessing
import pickle
import os

from Mouse import Mouse
import rasp_camera

# copy inside the bracket to convert .ui file into .py
# subprocess.run(r"pyuic6 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/doorwin.ui -o ./Python/gui/doorwin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/lickwin.ui -o ./Python/gui/lickwin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/testwin.ui -o ./Python/gui/testwin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/expwin.ui -o ./Python/gui/expwin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/detmousewin.ui -o ./Python/gui/detmousewin.py".split())
# subprocess.run(r"pyuic6 -x ./Python/gui/odourwin.ui -o ./Python/gui/odourwin.py".split())

# MICE_INIT_INFO = {'A11111':['Stuart',67],
#               'A22222': ['Little',45],
#               '0007A0F7C4': ['Real',27.4]}

if __name__ == "__main__":
    multiprocessing.freeze_support() # here for pyinstaller (.exe file) to work properly

    from config import CONFIG
    CONFIG.parse_arg()
    from logging_conf import LOGGING_CONFIG
    logging.config.dictConfig(LOGGING_CONFIG)
    #Optional - matplotlib spams a lot of debugs, so setting its level to info

    logger = logging.getLogger(__name__)
    rasp_camera.start_rpi_host()
    try:
        if CONFIG.TEENSY:
            l = subprocess.run([CONFIG.arduinoPath, "--upload", CONFIG.sketchPath,'--port', CONFIG.PORT])
            assert l.returncode == 0, 'Could not upload sketch to the teensy'

        START_TIME = datetime.datetime.now()

        sleep(5)
        
        if CONFIG.TEENSY:
            ser = serial.Serial(CONFIG.PORT, 9600)
        else:
            ser = Mock() # does nothing when ser object is called
            ser.readline.side_effect = lambda: input().encode() # add function to MOCK object
            ser.write.side_effect = lambda x: print(x.decode("utf-8").strip())
    except Exception as e:
        rasp_camera.close_record()
        print(e)
        sys.exit()

    all_mice = {} # dict object, key is ID value is the Mouse object
    # load all mouse objects into dict
    
    with open(f'{CONFIG.application_path}/mouse_info.csv',mode='r') as f:
        assert(f.readline().strip() == 'ID,Name,Weight') # check if csv file format is correct
        for line in f:
            info = line.strip().split(',') # split lines in mouse_info
            filename = os.path.join(CONFIG.application_path, 'MouseObjects', f'{info[0]}.obj')
            if os.path.exists(filename): # if the mouse object already exist
                filehandler = open(filename, 'rb') 
                all_mice[info[0]] = pickle.load(filehandler) # load into all_mice dictionary
                filehandler.close()
            else:
                all_mice[info[0]] = Mouse(info[0],info[1],info[2]) # put new mouse info into the dict by key


    # #Inititate Mice
    # all_mice = {}
    # for id, info in MICE_INIT_INFO.items():
    #     all_mice[id] = Mouse(id,info[0],info[1])

    #Comment out
    # doors = [
    #     [myTime(START_TIME,12367), all_mice['A22222'], 1],
    #     [myTime(START_TIME,33333), all_mice['A11111'], 2]
    #     ]
    # live_licks = [0,0,0,7,100,60]
    # all_tests = []

    #ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
    #ser = serial.Serial('/dev/cu.usbmodem105683101', 9600)

    

    #
    try:
        app = QtWidgets.QApplication(sys.argv)
        #mainwin = mainwinActions(ser,START_TIME,all_mice, doors,live_licks,all_tests)
        mainwin = mainwinActions(ser,START_TIME,all_mice)
        mainwin.show()
        sys.exit(app.exec()) # dont end program until GUI closed
    except Exception:
        logger.critical(f"Experiment has stopped\n{traceback.format_exc()}")
    
    

