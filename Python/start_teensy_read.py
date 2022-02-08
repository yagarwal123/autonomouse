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


def startTeensyRead(all_mice,doors,live_licks):
    while True:
        #Uncomment
        serIn = str(ser.readline()) # Read the newest output from the Arduino
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
        data_update.dataUpdate(serIn,all_mice,doors,live_licks)  
        mutex.unlock()