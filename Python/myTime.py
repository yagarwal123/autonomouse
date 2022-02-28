import datetime

#Open question: Is it better to inherit class since we need to get the START_TIME obj anyway?
#Question: Best way to display time
class myTime:
    """description of class"""
    def __init__(self,START_TIME, millis):
        self.START_TIME = START_TIME
        self.millis = millis
        self.time = self.START_TIME + datetime.timedelta(milliseconds=self.millis)
    
    def __str__(self):
        return self.time.strftime("%m-%d-%Y-%H-%M-%S")


