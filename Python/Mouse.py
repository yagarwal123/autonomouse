import datetime

class Mouse:
    """description of class"""
    def __init__(self,id,name,init_weight):
        self.id = id
        self.name = name
        self.init_weight = init_weight
        self.doortimes = []
        self.tests = []
        self.liquid_amount = 50
        self.lick_threshold = 50
        self.waittime = 5000
        self.test_limit = 10
        self.response_time = 2500

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def add_doortimes(self,t):
        self.doortimes.append(t)

    def tests_today(self):
        d = datetime.date.today()
        no_of_tests = 0
        for t in reversed(self.tests):
            if t.starting_time is None:
                continue
            if t.starting_time.time.date() == d:
                no_of_tests += 1
            else:
                break
        return no_of_tests

    def reached_limit(self):
        return self.tests_today() >= self.test_limit
        

