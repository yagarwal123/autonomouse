import logging
import re
import os
from multiprocessing import Process
from myTime import myTime
from Test import Trial
import rasp_camera
import serial
from config import CONFIG
import pickle
from PyQt6 import QtWidgets
#from odour_gen import odour_gen
from gui.odourwinActions import odourwinActions
from PyQt6.QtCore import QMutex

logger = logging.getLogger(__name__)

def dataUpdate(START_TIME,mutex,ser, inSer,all_mice,doors,live_licks,last_test,experiment_parameters,test_start_signal):
    KNOWNSTATEMENTS = ['^Weight Sensor - Weight (\d+\.?\d*)g$',                     #1
                      '^Door Sensor - ID (.+) - Door (\d) - Time (\d+)$',           #2
                      '^(\d+\.?\d*)$',                                              #3
                      '^Starting test now - (\d+)$',                                #4
                      '^Lick - Stimulus (\d+) - Trial (\d+) - Time (-?\d+)$',       #5
                      '^Test complete - Start saving to file$',                     #6
                      '^Sending raw data$',                                         #7
                      '^Waiting for the save to complete$',                         #8
                      '^Check whether to start test - (.+)$',                       #9
                      '^Send parameters: Incoming mouse ID - (.+)$',                #10
                      '^LOGGER:',                                                   #11
                      '^Stop recording$'                                            #12
                      ] 
    stat_mean, search = matchCommand(inSer,KNOWNSTATEMENTS)
    match stat_mean:
        case 0:
            return
        case 1:
            weight = float(search.group(1)) # extract things in 1st bracket
            #t = myTime(START_TIME,int(search.group(2)))
            last_test.weights.append(weight)
        case 2:
            if len(doors)>50: # save the last 50 door entries
                append_door_entries(doors) # option to save door entries in csv files: comment to disable
                del doors[-25:]
            m = all_mice[search.group(1)]
            d = int(search.group(2)) # 2nd bracket
            t = myTime(START_TIME,int(search.group(3)))
            last_entry = doors[0] if doors else None
            if last_entry is None or (str(last_entry[0]) != str(t)) or (last_entry[1] != m) or (last_entry[2] != d):
                doors.insert(0,[t,m,d])
        case 3:
            amp = float(search.group(1))
            live_licks.append(amp)
        case 4:
            t = myTime(START_TIME,int(search.group(1)))
            last_test.add_starting_time(t)
            rasp_camera.start_record(last_test.id)
            last_test.vid_recording = True
        case 5:
            s = int(search.group(1))
            trial = int(search.group(2))
            t = int(search.group(3))
            if ( len(last_test.trials) != (trial-1) ):   #Trial-1 since the newest one hasnt been added yet
                logger.error("Retrieving the wrong test")
            if experiment_parameters.trial_lim is not None and trial >= (experiment_parameters.trial_lim - 1):
                # if n trials happened already, and a signal is end, trials end at n+1
                last_test.trials_over = True
                ser.write('End\n'.encode()) # equivalent to clicking Stop test in test window
            soundStim = [s] # stimulus pattern, can be a dict of 1s and 0s
            o = odourwinActions(QMutex)
            # assume pattern already generated and displayed in the window
            od_size = len(o.pattern)
            index = trial % od_size # pull a line of odour stim from odourwinActions pattern
            if index < 0.1: index = od_size # if od_size is a multiple of trial no., i.e. last line of odour pattern
            stimPattern = o.pattern[index-1,:]
            stimPattern.astype(int) 
            #ser.write('oStim\n'.encode())
            #ser.write(stimPattern.encode()) # send it to teensy
            print(stimPattern) # TESTING PUROSE
            last_test.add_trial(Trial(trial,t,soundStim)) # add odour stim here after testing: [soundStim,stimPattern]
        case 6:
            test = last_test
            fileFolder = test.id
            if not os.path.exists(fileFolder):
                os.makedirs(fileFolder)
            filename = f'Test data - {test.id}.csv'
            filename = os.path.join(CONFIG.application_path, fileFolder, filename)
            with open(filename, 'w') as csvfile: 
                # creating a csv writer object 
                csvfile.write("Test Parameters:\n")
                csvfile.write(str(test.test_parameters))
                csvfile.write(f"\n\nWeight(max):{test.final_weight()}\n\n")
                csvfile.write('Trial No,Lick Time,Stim\n')
                for idx,trial in enumerate(test.trials):
                    row = f"{idx+1},{trial.value},{trial.stimuli}\n"
                    csvfile.write(row)
            live_licks.clear()
            try:
                rasp_camera.getVideofile(test.id)
            except Exception as e:
                logger.error(f'{e}: Error while recieving video from pi') # in case no video gets recorded

            
        case 7:
            test = last_test
            fileFolder = test.id
            filename = f'Raw lick data - {test.id}.csv'
            filePath = os.path.join(CONFIG.application_path,fileFolder,filename)
            mutex.unlock()
            ser.close()
            if CONFIG.TEENSY:
                p = Process(target=get_raw_data,args=[filePath,CONFIG.PORT])
                p.start()
                p.join()
            ser.open()
            ser.write("Reconnected\n".encode())
            mutex.lock()

        case 8:
            ser.write("Save complete\n".encode())
            last_test.ongoing = False
            m = last_test.get_mouse()
            m.add_test(last_test) # add data to mouse object
            # save mouse object to file with mouse id name
            fileFolder = 'MouseObjects'
            if not os.path.exists(fileFolder):
                os.makedirs(fileFolder)
            filename = os.path.join(CONFIG.application_path, fileFolder, f'{m.get_id()}.obj')
            filehandler = open(filename, 'wb') 
            pickle.dump(m, filehandler)
            filehandler.close()      

        case 9:
            m = all_mice[search.group(1)]
            if experiment_parameters.paused:
                logger.info('Experiment is paused')
                ser.write("Do not start\n".encode())
            elif m.reached_limit():
                logger.info(f'Mouse Limit is reached - {m.id}')
                ser.write("Do not start\n".encode())
            else:
                ser.write("Start experiment\n".encode())
                last_test.reset(m)
        case 10:
            test_start_signal.emit() # emit signal to open all windows (in mainwin_actions.py)
            m = all_mice[search.group(1)]
            t = last_test
            t.test_parameters.set_parameters(m.lick_threshold,m.liquid_amount,m.waittime,m.response_time,m.stim_prob)
            ser.write( ( str(m.lick_threshold) + "\n" ).encode() )
            ser.write( ( str(m.liquid_amount) + "\n" ).encode() )
            ser.write( ( str(m.waittime) + "\n" ).encode() )
            ser.write( ( str(m.response_time) + "\n" ).encode() )
            ser.write( ( str(m.stim_prob) + "\n" ).encode() ) # TODO: need changing to accommodate both sound and odour

        case 11:
            pass
        case 12:
            rasp_camera.stop_record()
            test = last_test
            test.vid_recording = False
            ser.write("Camera closed\n".encode())
                

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

def get_raw_data(filePath, port):
    rec_pause = False
    ser = serial.Serial(port, 9600)
    with open(filePath, 'w') as csvfile: 
        l = ''
        ser.write("Ready\n".encode())
        while (l.strip()[-22:] != 'Raw data send complete'):
            try:
                l = ser.readline().decode("utf-8") #l = ser.read(ser.in_waiting).decode("utf-8")
            except Exception as e:
                logger.error(f'{e}: Error while recieving raw data')
                continue
            csvfile.write(l)
            #logger.error(ser.in_waiting)
            if not rec_pause and (ser.in_waiting > 3000):
                ser.write("Pause\n".encode())
                rec_pause = True
            if rec_pause and (ser.in_waiting < 100):
                ser.write("Resume\n".encode())
                rec_pause = False
    ser.close()

def append_door_entries(doors):
    # save door entries?
    fileFolder = 'doorEntries'
    if not os.path.exists(fileFolder):
        os.makedirs(fileFolder)
    filename = f'Door data.csv' # save in file named by the time of saving
    filename = os.path.join(CONFIG.application_path, fileFolder, filename)
    with open(filename, 'a') as csvfile: 
        old_entries = doors[-25:]
        old_entries.reverse()
        for d in old_entries:
            csvfile.write(f'{d[0]},{d[1].get_id()},{d[2]}\n') # write all entry history in file