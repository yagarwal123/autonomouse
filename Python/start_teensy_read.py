import logging
import serial
import re

import data_update

logger = logging.getLogger(__name__)

serInlogger = logging.getLogger('Logger')
formatter = logging.Formatter('%(asctime)s - "%(message)s"')
fileHandler = logging.FileHandler('Serial_inputs.log', mode='w')   
fileHandler.setFormatter(formatter)
serInlogger.addHandler(fileHandler)
#This will overwrite files, do we want that? Or we do want to save previous runs?
#Mode a adds to the file, Mode w rewrites. Same question for info/warning log files

#ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port
ser = serial.Serial('/dev/cu.usbmodem105683101', 9600)
#ser = None

def startTeensyRead(mutex,START_TIME,all_mice,doors,live_licks,all_tests,experiment_paused):
    while True:
        #Uncomment
        try:
            serIn = (ser.readline()).decode("utf-8").strip() # Read the newest output from the Arduino
            #serIn = input()
        except Exception as e:
            logger.error(e)
            continue
        serInlogger.info(serIn)
        #print(serIn)
        #Comment out
        # b'Door Sensor - ID A11111 - Door 1 - Time 34567\r\n
        # b'Weight Sensor - Weight 75g - Time 123456\r\n
        # b'Lick Sensor - Trial 1 - Time 6792\r\n
        # b'792\r\n
        #serIn = input()

        #serIn = re.search(r"b'(.*)\\r\\n",serIn).group(1)
        #serIn = serIn.decode("utf-8")
        #print(serIn)
        
        mutex.lock()
        data_update.dataUpdate(START_TIME,ser,serIn,all_mice,doors,live_licks,all_tests,experiment_paused)  
        mutex.unlock()