class Test:
    """description of class"""
    def __init__(self,id, first_trial):
        self.id = id
        self.trials = [first_trial]
    
    def add_trial(self,new_trial):
        return self.trials.append(new_trial)


