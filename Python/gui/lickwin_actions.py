from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer, QMutex

import sys
import os
#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.lickwin import Ui_lickWin
# import matplotlib 
# import matplotlib.pyplot as plt
# matplotlib.use('Qt5Agg')
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.ticker as ticker
# import queue
import pyqtgraph as pg
import numpy as np

mutex = QMutex()

class lickwinActions(QtWidgets.QWidget, Ui_lickWin):
    def __init__(self,live_licks):
        super().__init__()
        self.setupUi(self)
        self.live_licks = live_licks
        self.title = "Lick Sensor"

    # update setupUi
    # def setupUi(self, Widget):
    #     super().setupUi(Widget)
        # MainWindow.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.pltgraph())
        self.timer.start(1)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

    def pltgraph(self):
        mutex.lock()
        self.plotWid.plot(self.live_licks[-5000:])
        mutex.unlock()

