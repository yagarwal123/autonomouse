from PyQt6 import QtCore, QtWidgets
from gui.lickwin import Ui_lickWin

class lickwinActions(QtWidgets.QWidget, Ui_lickWin):
    def __init__(self,mutex,live_licks):
        super().__init__()
        self.setupUi(self)
        self.live_licks = live_licks
        self.mutex = mutex
        self.title = "Lick Sensor"

        self.setWindowTitle(self.title) # change title
        self.pltax = None
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.pltgraph())
        self.timer.start(15)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

    def pltgraph(self):
        self.mutex.lock()
        if self.pltax:
            self.pltax.clear()

        self.pltax = self.plotWid.canvas.ax

        self.pltax.plot(self.live_licks[-5000:])
        self.pltax.set_xticks([])

        self.plotWid.canvas.draw()
        self.mutex.unlock()

