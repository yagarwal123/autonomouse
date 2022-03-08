import logging
import re
import os
from myTime import myTime
from Test import Test, Trial
import rasp_camera

logger = logging.getLogger(__name__)

def dataUpdate(START_TIME,ser, inSer,all_mice,doors,live_licks,all_tests,experiment_parameters):
    KNOWNSTATEMENTS = ['^Weight Sensor - Weight (\d+\.?\d*)g - Time (\d+)$',        #1
                      '^Door Sensor - ID (.+) - Door (\d) - Time (\d+)$',           #2
                      '^(\d+\.?\d*)$',                                              #3
                      '^Starting test now - (\d+)$',                                #4
                      '^Lick Sensor - Trial (\d+) - Time (-?\d+)$',                 #5
                      '^Test complete - Start saving to file$',                     #6
                      '^Sending raw data$',                                         #7
                      '^Waiting for the save to complete$',                         #8
                      '^Check whether to start test - (.+)$',                       #9
                      '^Send parameters: Incoming mouse ID - (.+)$',                #10
                      '^LOGGER:',                                                   #11
                      '^TTL - (\d+)$',                                              #12
                      '^Stop recording$'                                            #13                    
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
            all_tests[-1].add_starting_time(t)
        case 5:
            trial = int(search.group(1))
            t = int(search.group(2))
            m = getLastMouse(doors)
            old_test = m.tests[-1]
            if ( len(old_test.trials) != (trial-1) ):   #Trial-1 since the newest one hasnt been added yet
                logger.error("Retrieving the wrong test")
            old_test.add_trial(Trial(trial,t))
        case 6:
            test = all_tests[-1]
            fileFolder = test.get_id()
            filename = f'Test data - {test.get_id()}.csv'
            filename = os.path.join(fileFolder, filename)
            with open(filename, 'w') as csvfile: 
                # creating a csv writer object 
                csvfile.write("Test Parameters:\n")
                csvfile.write(str(test.test_parameters))
                csvfile.write('\n\n')
                csvfile.write('Trial No,Lick Time\n')
                for idx,trial in enumerate(test.trials):
                    row = f"{idx+1},{trial.value}\n"
                    csvfile.write(row)
            test.ongoing = False
            live_licks.clear()

            ttl_filename = f'TTL high millis - {test.get_id()}.csv'
            ttl_filename = os.path.join(fileFolder, ttl_filename)
            with open(ttl_filename, 'w') as ttlfile:
                for t in test.ttl:
                    ttlfile.write(f'{t.millis}\n')

            rasp_camera.getVideofile(test.get_id())
            
        case 7:
            test = all_tests[-1]
            fileFolder = test.get_id()
            if not os.path.exists(fileFolder):
                os.makedirs(fileFolder)
            filename = f'Raw lick data - {test.get_id()}.csv'
            filePath = os.path.join(fileFolder,filename)
            with open(filePath, 'w') as csvfile: 
                l = ''
                while (l.strip() != 'Raw data send complete'):
                    #logger.error(ser.in_waiting)
                    l = ser.readline().decode("utf-8")
                    csvfile.write(l)
                    if (ser.in_waiting > 6000):
                        #logger.error('Panic')
                        ser.write("Pause\n".encode())
                        while (ser.in_waiting > 100):
                            #logger.error(ser.in_waiting)
                            l = ser.readline().decode("utf-8")
                            csvfile.write(l)
                        ser.write("Resume\n".encode())
                    
        case 8:
            ser.write("Save complete\n".encode())
        case 9:
            m = all_mice[search.group(1)]
            if experiment_parameters.paused or m.reached_limit():
                ser.write("Do not start\n".encode())
            else:
                ser.write("Start experiment\n".encode())
                new_test = Test(m)
                m.tests.append(new_test)
                all_tests.append(new_test)
                rasp_camera.start_record(new_test.get_id())
        case 10:
            m = all_mice[search.group(1)]
            t = all_tests[-1]
            t.test_parameters.set_parameters(m.lick_threshold,m.liquid_amount,m.waittime)
            ser.write( ( str(m.lick_threshold) + "\n" ).encode() )
            ser.write( ( str(m.liquid_amount) + "\n" ).encode() )
            ser.write( ( str(m.waittime) + "\n" ).encode() )
        case 11:
            pass
        case 12:
            if all_tests:
                test = all_tests[-1]
                if test.ongoing:
                    t = myTime(START_TIME,int(search.group(1)))
                    test.add_ttl(t)
                else:
                    logger.warning("Printing TTL with no test ongoing")
            else:
                logger.warning("Printing TTL with no test conducted")
        case 13:
            rasp_camera.stop_record()
            ser.write("Camera closed\n".encode())
                


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
