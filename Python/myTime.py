import datetime

class myTime:
    """description of class"""
    def __init__(self,START_TIME, millis):
        self.START_TIME = START_TIME
        self.millis = millis
        self.time = self.START_TIME + datetime.timedelta(milliseconds=self.millis)
    
    def __str__(self):
        return self.time.isoformat(timespec='milliseconds')


