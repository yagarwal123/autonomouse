import logging
import re
import csv
from myTime import myTime
from Test import Test

logger = logging.getLogger(__name__)

def dataUpdate(START_TIME,ser, inSer,all_mice,doors,live_licks,all_tests):
    KNOWNSTATEMENTS = ['^Weight Sensor - Weight (\d*)g - Time (\d*)$',      #1
                      '^Door Sensor - ID (.*) - Door (\d) - Time (\d*)$',   #2
                      '^(^\d*\.?\d*)$',                                     #3
                      '^Starting test now - (\d*)$',                        #4
                      '^Lick Sensor - Trial (\d*) - Time (-?\d*)$',         #5
                      '^Test complete - Start saving to file$',             #6
                      '^Sending raw data$'                                  #7
                      ] 
    stat_mean, search = matchCommand(inSer,KNOWNSTATEMENTS)
    match stat_mean:
        case 0:
            return
        case 1:
            weight = float(search.group(1))
            t = myTime(START_TIME,int(search.group(2)))
            m = getLastMouse(doors)
            m.add_weight(weight)
            m.add_weighing_times(t)
        case 2:
            m = all_mice[search.group(1)]
            d = int(search.group(2))
            t = myTime(START_TIME,int(search.group(3)))
            doors.append([t,m,d])
        case 3:
            amp = float(search.group(1))
            live_licks.append(amp)
        case 4:
            t = myTime(START_TIME,int(search.group(1)))
            m = getLastMouse(doors)
            new_test = Test(m,t)
            m.tests.append(new_test)
            all_tests.append(new_test)
        case 5:
            trial = int(search.group(1))
            t = int(search.group(2))
            m = getLastMouse(doors)
            old_test = m.tests[-1]
            if ( len(old_test.trials) != (trial-1) ):   #Trial-1 since the newest one hasnt been added yet
                logger.error("Retrieving the wrong test")
                #print("Retrieving the wrong test")
            old_test.add_trial(t)
        case 6:
            #TODO Save data in file
            ser.write("Save complete".encode())
        case 7:
            m = getLastMouse(doors)
            filename = m.get_id() +  ' - ' +  m.tests[-1].starting_time
            with open(filename, 'w') as csvfile: 
                # creating a csv writer object 
                csvwriter = csv.writer(csvfile) 
                rows = ser.read() 
                csvwriter.writerows(rows)
               


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
