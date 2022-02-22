import datetime

class Mouse:
    """description of class"""
    def __init__(self,id,name,init_weight):
        self.id = id
        self.name = name
        self.init_weight = init_weight
        self.weights = []
        self.weight_times = []
        self.doortimes = []
        self.tests = []
        self.liquid_amount = 200
        self.lick_threshold = 1000
        self.waittime = 5000
        self.test_limit = 10

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def add_weight(self,w):
        self.weights.append(w)

    def add_weighing_times(self,t):
        self.weight_times.append(t)

    def add_doortimes(self,t):
        self.doortimes.append(t)

    def tests_today(self):
        d = datetime.date.today()
        no_of_tests = 0
        for t in reversed(self.tests):
            if t.starting_time.time.date() == d:
                no_of_tests += 1
            else:
                return no_of_tests

    def reached_limit(self):
        return self.tests_today() >= self.test_limit
        

