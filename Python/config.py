import sys, os
import argparse

class Config:
    def __init__(self):
        self.arduinoPath = "C:/PROGRA~2/Arduino/arduino_debug.exe"
        self.sketchPath = "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"
        self.TEENSY = True
        self.RASPBERRY = True
        self.PORT = 'COM3'
        self.OPEN_WINDOWS = True
        if getattr(sys, "frozen", False): # make sure the csv and log files are in the correct location to be read
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.getcwd()

    def parse_arg(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--arduinoPath',metavar='',help="Arduino exe location")
        parser.add_argument('--sketchPath',metavar='',help="Sketch ino location")
        parser.add_argument('--TEENSY',action=argparse.BooleanOptionalAction)
        parser.add_argument('--RASPBERRY',action=argparse.BooleanOptionalAction)
        parser.add_argument('--PORT',metavar='',help="Specify port")
        parser.add_argument('--OPEN_WINDOWS',action=argparse.BooleanOptionalAction)
        # parser.add_argument('--application_path',metavar='',help="Specify mouse_info location and where to save files")
        arg = parser.parse_args()

        if arg.arduinoPath is not None: self.arduinoPath = arg.arduinoPath
        if arg.sketchPath is not None: self.sketchPath = arg.sketchPath
        if arg.TEENSY is not None: self.TEENSY = arg.TEENSY
        if arg.RASPBERRY is not None: self.RASPBERRY = arg.RASPBERRY
        if arg.PORT is not None: self.PORT = arg.PORT
        if arg.OPEN_WINDOWS is not None: self.OPEN_WINDOWS = arg.OPEN_WINDOWS
        # if arg.application_path is not None: self.application_path = arg.application_path

        if not self.TEENSY: 
            self.RASPBERRY = False

CONFIG = Config()

