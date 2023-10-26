import sys, os
import argparse

class Config:
    def __init__(self):
        #if getattr(sys, "frozen", False): # make sure the csv and log files are in the correct location to be read
        #    self.application_path = os.path.dirname(sys.executable)
        #elif __file__:
        #    self.application_path = os.getcwd()
        self.application_path = 'C:/Users/lab/Desktop/autonomouse'
        self.EMAIL_ID = 'autonomouse.error@gmail.com'
        self.PASSWORD = 'strcjmjpictxddjj'

    def parse_arg(self): 
        arduinoPath = "C:/PROGRA~2/Arduino/arduino_debug.exe"
        sketchPath = "C:/Users/lab/Desktop/autonomouse/Arduino/demo_code/demo_code.ino"
        teensy = True
        raspberry = True
        port = 'COM3'
        open_windows = True
        self.TO_EMAIL = ['autonomouse.error@gmail.com']
        parser = argparse.ArgumentParser()
        parser.add_argument('--arduinoPath',metavar='',help="Arduino exe location",default=arduinoPath)
        parser.add_argument('--sketchPath',metavar='',help="Sketch ino location",default=sketchPath)
        parser.add_argument('--TEENSY',action=argparse.BooleanOptionalAction,default=teensy)
        parser.add_argument('--RASPBERRY',action=argparse.BooleanOptionalAction,default=raspberry)
        parser.add_argument('--PORT',metavar='',help="Specify port",default=port)
        parser.add_argument('--OPEN_WINDOWS',action=argparse.BooleanOptionalAction,default=open_windows)
        parser.add_argument('--TO_EMAIL', nargs='+', metavar='', help='Emails to send error messages to')
        # parser.add_argument('--application_path',metavar='',help="Specify mouse_info location and where to save files")
        arg = parser.parse_args()

        self.arduinoPath = arg.arduinoPath
        self.sketchPath = arg.sketchPath
        self.TEENSY = arg.TEENSY
        self.RASPBERRY = arg.RASPBERRY
        self.PORT = arg.PORT
        self.OPEN_WINDOWS = arg.OPEN_WINDOWS
        if arg.TO_EMAIL is not None: self.TO_EMAIL.extend(arg.TO_EMAIL)
        # if arg.application_path is not None: self.application_path = arg.application_path

        if not self.TEENSY: 
            self.RASPBERRY = False

CONFIG = Config()

