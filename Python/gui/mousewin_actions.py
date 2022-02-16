from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSlot, QRect, QTimer

import matplotlib.pyplot
#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.mousewin import Ui_mouseWin

class mousewinActions(QtWidgets.QWidget, Ui_mouseWin):
    def __init__(self,mutex,mouse):
        super().__init__()
        self.setupUi(self)
        self.mouse = mouse
        self.mutex = mutex
        self.title = self.mouse.get_id() +  ' - ' + self.mouse.get_name()

        # MainWindow.resize(400, 300) # do not modify it
        #self.move(self.left, self.top)  # set location for window
        self.setWindowTitle(self.title) # change title
        self.pltax = None
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.pltgraph())
        self.timer.start(1000)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

        self.liq_am_disp.setText(str(self.mouse.liquid_amount))
        self.lick_thresh_disp.setText(str(self.mouse.lick_threshold))

        self.myactions()

    # define actions here
    def myactions(self):
        self.changeliquidButton.clicked.connect(self.change_liquid)
        self.changelickButton.clicked.connect(self.change_lick)

    def change_liquid(self):
        try:
            l = float(self.liquidLineEdit.text())
            self.liq_am_disp.setText(str(l))
            self.mouse.liquid_amount = l
            self.liquidLineEdit.clear()
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()
        

    def change_lick(self):
        try:
            l = float(self.lickLineEdit.text())
            self.lick_thresh_disp.setText(str(l))
            self.mouse.lick_threshold = l
            self.lickLineEdit.clear()
        except ValueError:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def pltgraph(self):
        self.mutex.lock()
        if self.pltax:
            self.pltax.clear()
        
        x = [0] + [i.millis for i in self.mouse.weight_times]
        x_lab = ['Start'] + [str(i) for i in self.mouse.weight_times]
        y = [self.mouse.init_weight] + self.mouse.weights

        self.pltax = self.plotWid.canvas.ax
        matplotlib.pyplot.setp(self.pltax, xticks=x, xticklabels=x_lab)
        matplotlib.pyplot.setp(self.pltax.xaxis.get_majorticklabels(), rotation=90)
        self.pltax.plot(x,y)
        self.pltax.set_xlim(left=0)
        #self.plotWid.canvas.fig.set_tight_layout(True)

        self.plotWid.canvas.draw()
        self.mutex.unlock()