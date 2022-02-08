import logging
import re
import serial
from Test import Test

logger = logging.getLogger(__name__)

def dataUpdate(ser, inSer,all_mice,doors,live_licks):
    KNOWNSTATEMENTS = ['^Weight Sensor - Weight (\d*)g - Time (\d*)$',
                      '^Door Sensor - ID (.*) - Door (\d) - Time (\d*)$',
                      '^(^\d*\.?\d*)$',
                      '^Lick Sensor - Trial (\d*) - Time (-?\d*)$',
                      'Test complete - Start saving to file'
                      ] 
    stat_mean, search = matchCommand(inSer,KNOWNSTATEMENTS)
    match stat_mean:
        case 0:
            return
        case 1:
            weight = float(search.group(1))
            t = int(search.group(2))
            m = getLastMouse(doors)
            m.add_weight(weight)
            m.add_weighing_times(t)
        case 2:
            m = all_mice[search.group(1)]
            d = int(search.group(2))
            t = int(search.group(3))
            doors.append([t,m,d])
        case 3:
            amp = float(search.group(1))
            live_licks.append(amp)
        case 4:
            trial = int(search.group(1))
            t = int(search.group(2))
            m = getLastMouse(doors)
            if trial == 1:
                new_test = Test(m.get_id(),t)
                m.tests.append(new_test)
            else:
                old_test = m.tests[-1]
                old_test.add_trial(t)
        case 5:
            #TODO Save data in file
            ser.write("Save complete".encode())

def getLastMouse(doors):
    for entry in reversed(doors):
        if entry[2] == 2:
            return entry[1]

def matchCommand(inSer,KNOWNSTATEMENTS):
    stat_mean = 0
    search = None
    for idx,item in enumerate(KNOWNSTATEMENTS):
        search = re.search(item,inSer)
        if search is not None:
            stat_mean = idx+1
            break
    if stat_mean == 0:
        logger.error("Unknown message recieved : " + inSer)
    return stat_mean, search
