import subprocess
import logging.config
from time import sleep
from logging_conf import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

logging.getLogger('matplotlib').setLevel(logging.WARNING)
#Optional - matplotlib spams a lot of debugs, so setting its level to info

subprocess.run(r"pyuic6 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py",shell=True)
subprocess.run(r"pyuic6 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py",shell=True)
subprocess.run(r"pyuic6 -x ./Python/gui/doorwin.ui -o ./Python/gui/doorwin.py",shell=True)
subprocess.run(r"pyuic6 -x ./Python/gui/lickwin.ui -o ./Python/gui/lickwin.py",shell=True)
subprocess.run(r"pyuic6 -x ./Python/gui/testwin.ui -o ./Python/gui/testwin.py",shell=True)

import logging
import datetime
from PyQt6 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys
import serial

from Mouse import Mouse
import rasp_camera
from myTime import myTime

# MICE_INIT_INFO = {'A11111':['Stuart',67],
#               'A22222': ['Little',45],
#               '0007A0F7C4': ['Real',27.4]}

START_TIME = datetime.datetime.now()


if __name__ == "__main__":

    #m = subprocess.run(['C:/Program Files (x86)/Arduino/arduino.exe','--upload','C:\\Users\\lab\\AppData\\Local\\Temp\\arduino_build_680162/demo_code.ino.hex'])
    #m = subprocess.run(['"C:/PROGRA~2/Arduino/arduino.exe" --upload "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"/Arduino/arduino.exe" --upload "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"'],shell=True,encoding='UTF-8')
    #os.system("\"C:/Program Files (x86)/Arduino/arduino.exe\" --upload \"C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino\"")
    #"C:/Program Files (x86)/Arduino/arduino.exe" --upload "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"
    #os.system("C:/PROGRA~2/Arduino/arduino.exe --port COM4 --upload C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino")
    cmd = "C:/PROGRA~2/Arduino/arduino_debug.exe --upload C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"
    l = subprocess.run(cmd.split())
    assert(l.returncode == 0)

    all_mice = {}
    with open('mouse_info.csv',mode='r') as f:
        assert(f.readline().strip() == 'ID,Name,Weight')
        for line in f:
            info = line.strip().split(',')
            all_mice[info[0]] = Mouse(info[0],info[1],info[2])

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
    ser = serial.Serial('COM4', 9600)
    #ser = None

    rasp_camera.start_rpi_host()

    app = QtWidgets.QApplication(sys.argv)
    #mainwin = mainwinActions(ser,START_TIME,all_mice, doors,live_licks,all_tests)
    mainwin = mainwinActions(ser,START_TIME,all_mice)
    mainwin.show()
    sys.exit(app.exec())
    
    

