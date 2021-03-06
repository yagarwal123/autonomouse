import logging
from config import CONFIG
import data_update

logger = logging.getLogger(__name__)

serInlogger = logging.getLogger('Logger')
formatter = logging.Formatter('%(asctime)s - "%(message)s"')
fileHandler = logging.FileHandler(f'{CONFIG.application_path}/Serial_inputs.log', mode='a')   
fileHandler.setFormatter(formatter)
serInlogger.addHandler(fileHandler)
#Question: This will overwrite files, do we want that? Or we do want to save previous runs?
#Mode a adds to the file, Mode w rewrites. Same question for info/warning log files

def startTeensyRead(ser,mutex,START_TIME,all_mice,doors,live_licks,last_test,experiment_parameters,test_start_signal):
    while True:
        try:
            #Uncomment
            serIn = (ser.readline()).decode("utf-8").strip() # Read the newest output from the Arduino
            #serIn = input()
        except Exception as e:
            logger.error(e)
            continue
        serInlogger.debug(serIn)
        # b'Door Sensor - ID A11111 - Door 1 - Time 34567\r\n
        # b'Weight Sensor - Weight 75g - Time 123456\r\n
        # b'Lick Sensor - Trial 1 - Time 6792\r\n
        # b'792\r\n
        
        mutex.lock()
        data_update.dataUpdate(START_TIME,mutex,ser,serIn,all_mice,doors,live_licks,last_test,experiment_parameters,test_start_signal)  
        mutex.unlock()