class ExperimentParameters:
    """description of class"""
    def __init__(self):
        self.paused = False
        self.valve_open = False

    @staticmethod
    def update_all_mice_liquid(all_mice,amount):
        for m in all_mice.values():
            m.liquid_amount = amount

    @staticmethod
    def update_all_mice_lick(all_mice,lick):
        for m in all_mice.values():
            m.lick_threshold = lick

    @staticmethod
    def update_all_mice_waittime(all_mice,waittime):
        for m in all_mice.values():
            m.waittime = waittime

    @staticmethod
    def update_all_mice_limit(all_mice,limit):
        for m in all_mice.values():
            m.test_limit = limit

    @staticmethod
    def update_all_mice_resp(all_mice,resp):
        for m in all_mice.values():
            m.response_time = resp

