import datetime

class Mouse:
    """description of class"""
    def __init__(self,id,name,init_weight):
        self.id = id
        self.name = name
        self.init_weight = init_weight
        self.final_weights = []
        self.test_times = []
        self.test_ids = []
        self.tests_today = 0
        self.last_test_date = None
        self.liquid_amount = 50
        self.lick_threshold = 50
        self.waittime = 5000
        self.test_limit = 10
        self.response_time = 2500

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def add_test(self,test):
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
        

