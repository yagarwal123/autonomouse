import logging
import serial
import re
from time import sleep
from PyQt5.QtCore import QMutex

from Mouse import Mouse
import data_update

logger = logging.getLogger(__name__)

mutex = QMutex()

def startTeensyRead(all_mice,doors,live_licks):
    while True:
        #Uncomment
        #serIn = str(ser.readline()) # Read the newest output from the Arduino

        #Comment out
        # b'Door Sensor - ID A11111 - Door 1 - Time 34567\r\n
        # b'Weight Sensor - ID A22222 - Weight 75g - Time 123456\r\n
        serIn = input()

        serIn = re.search(r"b'(.*)\\r\\n",serIn).group(1)
        print(serIn)


        mutex.lock()
        data_update.dataUpdate(serIn,all_mice,doors,live_licks)  
        mutex.unlock()