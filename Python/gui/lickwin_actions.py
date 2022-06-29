from PyQt6 import QtCore, QtWidgets, QtGui
from gui.lickwin import Ui_lickWin

class lickwinActions(QtWidgets.QWidget, Ui_lickWin):
    def __init__(self,mutex,live_licks,pos=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.live_licks = live_licks
        self.mutex = mutex
        self.title = "Lick Sensor"

        if pos is not None: self.move(pos)
        self.setWindowTitle(self.title) # change title
        self.pltax = None
        
        self.timer = QtCore.QTimer(self) # doesnt stop itself when window isc losed by default
        self.timer.timeout.connect(lambda:self.pltgraph())
        self.timer.start(100) # runs every 100ms

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose) # delete object (including timer) whenever window is closed
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False) # to close this window whenever main window is closed because everything except for mainwindow is secondary window

    def pltgraph(self):
        if self.live_licks:
            self.mutex.lock() # need to be done whever anything is being edited
            if self.pltax:
                self.pltax.clear()

            self.pltax = self.plotWid.canvas.ax

            self.pltax.plot(self.live_licks[-1000:])
            self.pltax.set_xticks([])

            self.plotWid.canvas.draw()
            self.mutex.unlock()

