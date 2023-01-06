import logging
logger = logging.getLogger(__name__)

from dataclasses import dataclass

class Test:
    """description of class"""
    def reset(self,mouse):
        self.__mouse = mouse
        self.starting_time = None
        self.trials=[]
        self.weights = [0]
        self.test_parameters = TestParameters()
        self.vid_recording = False
        self.ongoing = True
        self.trials_over = False
        self.id = None
    
    def add_trial(self,new_trial):
        self.trials.append(new_trial)

    def get_mouse(self):
        return self.__mouse

    def add_starting_time(self,t):
        if self.starting_time is None:
            self.starting_time = t
            self.id = f'{self.__mouse.get_id()}_{self.starting_time}'
        else:
            logger.error('Unexpected starting time message. Not updated')
    
    def final_weight(self):
        return max(self.weights)

@dataclass
class Trial: # trial class containing index, response and stim
    idx: int
    value: int
    stimuli: list # can be a list instead of 1 number now

class TestParameters:

    def set_parameters(self,lick_threshold,liquid_amount,waittime,response_time,stim_prob):
        self.lick_threshold = [lick_threshold]
        self.liquid_amount = [liquid_amount]
        self.waittime = [waittime]
        self.response_time = [response_time]
        self.stim_prob = [stim_prob]

    def __str__(self):
        attrs = vars(self)
        return('\n'.join("%s,%s" % item for item in attrs.items()))
    

