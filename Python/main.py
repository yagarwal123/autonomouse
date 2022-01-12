import logging
import logging.config
import multiprocessing

from Mouse import Mouse
from start_teensy_read import startTeensyRead
from gui.start_gui import startGUI

import os
os.system(r"pyuic5 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py")

MICE_INIT_INFO = {'A11111':['Stuart',67],
              'A22222': ['Little',45]}

#Uncomment
#ser = serial.Serial('/dev/ttyACM0', 9600) # Establish the connection on a specific port

#logging.config.fileConfig('loging.conf') set file location
logger = logging.getLogger(__name__)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

#Inititate Mice
all_mice = {}
for id, info in MICE_INIT_INFO.items():
    all_mice[id] = Mouse(id,info[0],info[1])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=startGUI) 
    p2 = multiprocessing.Process(target=startTeensyRead, args=(all_mice,))
    p1.start() 
    p2.start()

    p1.join()       #Wait till Process 1 ends (Till GUI is closed)
    p2.terminate()  #Terminate Process 2 (Stop reading Teensy)
    

