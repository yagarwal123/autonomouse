import logging
logger = logging.getLogger(__name__)

class Test:
    """description of class"""
    def __init__(self,mouse):
        self.mouse = mouse
        self.starting_time = None
        self.trials=[]
        self.odours = []
        self.ttl = []
        self.ongoing = True
    
    def add_trial(self,new_trial):
        self.trials.append(new_trial)

    def add_ttl(self,ttl_time):
        self.ttl.append(ttl_time)

    def add_starting_time(self,t):
        if self.starting_time is None:
            self.starting_time = t
        else:
            logger.error('Unexpected starting time message. Not updated')

class Trial:
    """description of class"""
    def __init__(self,idx, value):
        self.idx = idx
        self.value = value
    

