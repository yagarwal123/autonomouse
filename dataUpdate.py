import logging
import re

logger = logging.getLogger(__name__)

def matchCommand(inSer,KNOWNSTATEMENTS):

    stat_mean = 0
    for idx,item in enumerate(KNOWNSTATEMENTS):
        if inSer[0:len(item)] == item:
            stat_mean = idx+1;
            break
    if stat_mean == 0:
        logger.error("Unknown message recieved : " + inSer)
    return stat_mean

def mouseUpdate(inSer,all_mice):
    KNOWNSTATEMENTS = ['Weight Sensor - ID ',
                      'Door Sensor - ID ',
                      ] 
    stat_mean = matchCommand(inSer,KNOWNSTATEMENTS)
    #TODO error handling
    match stat_mean:
        case 0:
            return
        case 1:
            id = re.search(r'Weight Sensor - ID (.*) - Weight .*g - Time .*',inSer).group(1)
            weight = re.search(r'Weight Sensor - ID .* - Weight (.*)g - Time .*',inSer).group(1)
            t = re.search(r'Weight Sensor - ID .* - Weight .*g - Time (.*)',inSer).group(1)
            m = all_mice[id]
            m.add_weight(weight)
            m.add_weighing_times(t)