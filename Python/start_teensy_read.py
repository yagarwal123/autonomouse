import logging
import serial
import re
from time import sleep
from PyQt5.QtCore import QMutex

from Mouse import Mouse
import data_update

logger = logging.getLogger(__name__)

mutex = QMutex()

def startTeensyRead(all_mice,doors):
    while True:
        # m = all_mice['A11111']
        # print(m.weight[-1])
        # print(m.weight_times[-1])
        #Uncomment
        #serIn = str(ser.readline()) # Read the newest output from the Arduino
        serIn = "b'Weight Sensor - ID A11111 - Weight 675g - Time 123456\\r\\n"
        serIn = re.search(r"b'(.*)\\r\\n",serIn).group(1)
        print(serIn)
        mutex.lock()
        data_update.dataUpdate(serIn,all_mice,doors)  
        mutex.unlock()

        #Comment out
        sleep(5)
        serIn = "b'Door Sensor - ID A11111 - Door 1 - Time 34567\\r\\n"
        serIn = re.search(r"b'(.*)\\r\\n",serIn).group(1)
        print(serIn)
        mutex.lock()
        data_update.dataUpdate(serIn,all_mice,doors)  
        mutex.unlock()
        sleep(5)
        # m = all_mice['A11111']
        # print(m.weight[-1])
        # print(m.weight_times[-1])
