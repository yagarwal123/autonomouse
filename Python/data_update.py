import logging
import re

logger = logging.getLogger(__name__)

def dataUpdate(inSer,all_mice,doors,live_licks):
    KNOWNSTATEMENTS = ['^Weight Sensor - ID (.*) - Weight (\d*)g - Time (\d*)$',
                      '^Door Sensor - ID (.*) - Door (\d) - Time (\d*)$',
                      ] 
    stat_mean, search = matchCommand(inSer,KNOWNSTATEMENTS)
    match stat_mean:
        case 0:
            return
        case 1:
            id = search.group(1)
            weight = search.group(2)
            t = search.group(3)
            m = all_mice[id]
            m.add_weight(weight)
            m.add_weighing_times(t)
        case 2:
            id = search.group(1)
            d = search.group(2)
            t = search.group(3)
            doors.append([t,all_mice[id],d])

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
