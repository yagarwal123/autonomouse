import logging
import logging.config
import multiprocessing

from Mouse import Mouse
from start_teensy_read import startTeensyRead
from start_gui import startGUI

import os
os.system(r"pyuic5 -x ./Python/gui/mainwin.ui -o ./Python/gui/mainwin.py")
os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
os.system(r"pyuic5 -x ./Python/gui/doorwin.ui -o ./Python/gui/doorwin.py")

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

doors = [
    [12367, all_mice['A22222']],
    [33333, all_mice['A11111']]
    ]
#Uncomment
#doors = []

if __name__ == "__main__":
    startGUI(all_mice,doors)
    

