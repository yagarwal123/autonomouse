import os
import pickle
from config import CONFIG
class ExperimentParameters:
    """description of class"""
    def __init__(self):
        self.paused = False
        self.valve_open = False
        #self.trial_lim = None

    @staticmethod
    def saveAll(all_mice):
        fileFolder = 'MouseObjects'
        if not os.path.exists(fileFolder):
            os.makedirs(fileFolder)
        for m in all_mice.values():
            filename = os.path.join(CONFIG.application_path, fileFolder, f'{m.get_id()}.obj')
            filehandler = open(filename, 'wb') 
            pickle.dump(m, filehandler)
            filehandler.close()      
            #m.liquid_amount = amount

    @staticmethod
    def update_all_mice_liquid(all_mice,amount):
        for m in all_mice.values():
            m.liquid_amount = amount

    @staticmethod
    def update_all_mice_lick(all_mice,lick):
        for m in all_mice.values():
            m.lick_threshold = lick

    @staticmethod
    def update_all_mice_waittime(all_mice,waittime):
        for m in all_mice.values():
            m.waittime = waittime

    @staticmethod
    def update_all_mice_punishtime(all_mice,punishtime):
        for m in all_mice.values():
            m.punishtime = punishtime

    @staticmethod
    def update_all_mice_limit(all_mice,limit):
        for m in all_mice.values():
            m.test_limit = limit

    @staticmethod
    def update_all_trial_lim(all_mice,limit):
        for m in all_mice.values():
            m.trial_lim = limit

    @staticmethod
    def update_all_mice_resp(all_mice,resp):
        for m in all_mice.values():
            m.response_time = resp

    @staticmethod
    def update_all_stim_prob(all_mice,prob):
        for m in all_mice.values():
            m.stim_prob = prob
        

