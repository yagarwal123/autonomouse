from datetime import date
import numpy as np

class Mouse:
    """description of class"""
    def __init__(self,id,name,init_weight):
        self.__id = id # underscore in front self._id - make this uneditable from outside this class
        self.__name = name
        self.__init_weight = init_weight
        self.final_weights = []
        self.test_times = []
        self.test_ids = []
        self.tests_today = 0
        self.last_test_date = None
        self.liquid_amount = 50
        self.lick_threshold = 50
        self.waittime = 5000
        self.punishtime = 0
        self.test_limit = 10
        self.trial_lim = None
        self.response_time = 2500
        self.stim_prob = 70
        self.n_odours = 0
        self.od_stim = np.zeros((1,15)) # stim pattern default
        self.od_target = []
        

    def get_name(self):
        return self.__name # to access this need to use get_name() everytime in any other funciton if use _name in init()
    
    def get_id(self):
        return self.__id

    def get_init_weight(self):
        return self.__init_weight

    def add_test(self,test): # add data from test object to mouse object
        self.test_ids.append(test.id)
        self.test_times.append(test.starting_time)
        self.final_weights.append(test.final_weight())
        if self.last_test_date == test.starting_time.time.date():
            self.tests_today += 1
        else:
            self.tests_today = 1
            self.last_test_date = test.starting_time.time.date()

    def reached_limit(self):
        return self.tests_today >= self.test_limit

    def get_tests_today(self):
        if date.today() != self.last_test_date:
            self.tests_today = 0
        return self.tests_today
        

