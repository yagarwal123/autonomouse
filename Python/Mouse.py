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


