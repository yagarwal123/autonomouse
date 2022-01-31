import logging
import re

logger = logging.getLogger(__name__)

def dataUpdate(inSer,all_mice,doors,live_licks):
    KNOWNSTATEMENTS = ['^Weight Sensor - Weight (\d*)g - Time (\d*)$',
                      '^Door Sensor - ID (.*) - Door (\d) - Time (\d*)$',
                      '^(\d*)',
                      '^Lick Sensor - Time (\d*)$'
                      ] 
    stat_mean, search = matchCommand(inSer,KNOWNSTATEMENTS)
    match stat_mean:
        case 0:
            return
        case 1:
            weight = search.group(1)
            t = search.group(2)
            m = getLastMouse(doors)
            m.add_weight(weight)
            m.add_weighing_times(t)
        case 2:
            m = getLastMouse(doors)
            d = search.group(2)
            t = search.group(3)
            doors.append([t,m,d])
        case 3:
            amp = search.group(1)
            live_licks.append(float(amp))

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
