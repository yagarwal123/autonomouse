from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer

import sys
import os
#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.lickwin import Ui_lickWin

class lickwinActions(QtWidgets.QWidget, Ui_lickWin):
    def __init__(self,mutex,live_licks):
        super().__init__()
        self.setupUi(self)
        self.live_licks = live_licks
        self.mutex = mutex
        self.title = "Lick Sensor"

    # update setupUi
    # def setupUi(self, Widget):
    #     super().setupUi(Widget)
        # MainWindow.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title
        self.pltax = None
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.pltgraph())
        self.timer.start(15)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

    def pltgraph(self):
        self.mutex.lock()
        if self.pltax:
            self.pltax.clear()

        self.pltax = self.plotWid.canvas.ax
        #matplotlib.pyplot.setp(self.pltax, xticks=x, xticklabels=x_lab)
        #matplotlib.pyplot.setp(self.pltax.xaxis.get_majorticklabels(), rotation=90)
        self.pltax.plot(self.live_licks[-5000:])
        #self.pltax.set_xlim(left=0)
        #self.plotWid.canvas.fig.set_tight_layout(True)

        self.plotWid.canvas.draw()
        self.mutex.unlock()

