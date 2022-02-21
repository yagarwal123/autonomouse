class Test:
    """description of class"""
    def __init__(self,mouse, starting_time):
        self.mouse = mouse
        self.starting_time = starting_time
        self.trials=[]
        self.odours = []
    
    def add_trial(self,new_trial):
        return self.trials.append(new_trial)

class Trial:
    """description of class"""
    def __init__(self,idx, value):
        self.idx = idx
        self.value = value
    

