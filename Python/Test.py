import logging
logger = logging.getLogger(__name__)

from dataclasses import dataclass

class Test:
    """description of class"""
    def reset(self,mouse):
        self.mouse = mouse
        self.starting_time = None
        self.trials=[]
        self.ttl = []
        self.weights = [0]
        self.test_parameters = TestParameters()
        self.vid_recording = True
        self.ongoing = True
        self.trials_over = False
        self.id = f'{self.mouse.get_id()}_{len(self.mouse.test_ids) + 1}'
    
    def add_trial(self,new_trial):
        self.trials.append(new_trial)

    def add_ttl(self,ttl_time):
        if (not self.ttl) or (ttl_time.millis-self.ttl[-1].millis>15):
            self.ttl.append(ttl_time)

    def add_starting_time(self,t):
        if self.starting_time is None:
            self.starting_time = t
        else:
            logger.error('Unexpected starting time message. Not updated')
    
    def final_weight(self):
        return max(self.weights)

@dataclass
class Trial:
    idx: int
    value: int
    stimuli: list

class TestParameters:

    def set_parameters(self,lick_threshold,liquid_amount,waittime,response_time):
        self.lick_threshold = lick_threshold
        self.liquid_amount = liquid_amount
        self.waittime = waittime
        self.response_time = response_time

    def __str__(self):
        attrs = vars(self)
        return('\n'.join("%s,%s" % item for item in attrs.items()))
    

