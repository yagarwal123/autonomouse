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
        self.test_parameters = TestParameters()
        self.vid_recording = True
        self.ongoing = True
    
    def add_trial(self,new_trial):
        self.trials.append(new_trial)

    def add_ttl(self,ttl_time):
        if (not self.ttl) or (self.ttl[-1] != ttl_time):
            self.ttl.append(ttl_time)

    def add_starting_time(self,t):
        if self.starting_time is None:
            self.starting_time = t
        else:
            logger.error('Unexpected starting time message. Not updated')
    
    def get_id(self):
        return f'{self.mouse.get_id()}_{len(self.mouse.tests)}'

class Trial:
    """description of class"""
    def __init__(self,idx, value):
        self.idx = idx
        self.value = value

class TestParameters:

    def __init__(self):
        self.lick_threshold = None
        self.liquid_amount = None
        self.waittime = None

    def set_parameters(self,lick_threshold,liquid_amount,waittime):
        self.lick_threshold = lick_threshold
        self.liquid_amount = liquid_amount
        self.waittime = waittime

    def __str__(self):
        attrs = vars(self)
        return('\n'.join("%s, %s" % item for item in attrs.items()))
    

