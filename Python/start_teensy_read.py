import logging
import serial
import re
from time import sleep
from PyQt6.QtCore import QMutex

from Mouse import Mouse
import data_update

logger = logging.getLogger(__name__)

mutex = QMutex()

#ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
ser = serial.Serial('/dev/cu.usbmodem105683101', 9600)


def startTeensyRead(START_TIME,all_mice,doors,live_licks,all_tests):
    while True:
        #Uncomment
        try:
            serIn = str(ser.readline()) # Read the newest output from the Arduino
        except Exception as e:
            print(e)
            continue
        #print(serIn)
        #Comment out
        # b'Door Sensor - ID A11111 - Door 1 - Time 34567\r\n
        # b'Weight Sensor - Weight 75g - Time 123456\r\n
        # b'Lick Sensor - Trial 1 - Time 6792\r\n
        # b'792\r\n
        #serIn = input()

        serIn = re.search(r"b'(.*)\\r\\n",serIn).group(1)
        #print(serIn)

        mutex.lock()
        data_update.dataUpdate(START_TIME,ser,serIn,all_mice,doors,live_licks,all_tests)  
        mutex.unlock()