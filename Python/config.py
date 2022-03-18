import sys, os

class Config:
    def __init__(self):
        self.arduinoPath = "C:/PROGRA~2/Arduino/arduino_debug.exe"
        self.sketchPath = "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"
        self.TEENSY = True
        self.RASPBERRY = True
        self.PORT = 'COM4'
        self.OPEN_WINDOWS = True
        if getattr(sys, "frozen", False):
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.getcwd()

CONFIG = Config()

