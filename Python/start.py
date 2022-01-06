import logging
import logging.config
from Mouse import Mouse
import dataUpdate

MICE_INIT_INFO = {'A11111':['Stuart',67],
              'A22222': ['Little',45]}

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

# m = all_mice['A11111']
# print(m.weight[-1])
# print(m.weight_times[-1])

dataUpdate.mouseUpdate('Weight Sensor - ID A11111 - Weight 675g - Time 123456',all_mice)   
m = all_mice['A11111']
print(m.weight[-1])
print(m.weight_times[-1])
