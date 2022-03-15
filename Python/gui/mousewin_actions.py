from PyQt6 import QtCore, QtWidgets
from multiprocessing import Process
import matplotlib.pyplot
import logging
from gui.mousewin import Ui_mouseWin
from analysis import analysis_window

logger = logging.getLogger(__name__)

class mousewinActions(QtWidgets.QWidget, Ui_mouseWin):
    def __init__(self,mutex,mouse):
        super().__init__()
        self.setupUi(self)
        self.mouse = mouse
        self.mutex = mutex
        self.title = self.mouse.get_id() +  ' - ' + self.mouse.get_name()

        self.setWindowTitle(self.title) # change title
        for t in self.mouse.tests:
            if not t.ongoing:
                self.test_select.addItem(f'{t.id} - {t.starting_time}')
        self.pltax = None
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda:self.updatedata())
        self.timer.start(1000)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_QuitOnClose,False)

        self.liq_am_disp.setText(str(self.mouse.liquid_amount))
        self.lick_thresh_disp.setText(str(self.mouse.lick_threshold))
        self.waittime_disp.setText(str(self.mouse.waittime))
        self.test_lim_disp.setText(str(self.mouse.test_limit))
        self.test_no_disp.setText(str(self.mouse.tests_today()))

        self.liquidLineEdit.returnPressed.connect(self.changeliquidButton.click)
        self.lickLineEdit.returnPressed.connect(self.changelickButton.click)
        self.waittimeLineEdit.returnPressed.connect(self.changewaittimeButton.click)
        self.testLimLineEdit.returnPressed.connect(self.changeTestLimButton.click)

        self.myactions()

    # define actions here
    def myactions(self):  
        self.changeliquidButton.clicked.connect(self.change_liquid)
        self.changelickButton.clicked.connect(self.change_lick)
        self.changewaittimeButton.clicked.connect(self.change_waittime)
        self.changeTestLimButton.clicked.connect(self.change_testlim)
        self.showAnalysisButton.clicked.connect(self.analysis_win)

    def change_liquid(self):
        l = self.liquidLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.liq_am_disp.setText(l)
            self.mouse.liquid_amount = int(l)
            self.liquidLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()
        

    def change_lick(self):
        l = self.lickLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.lick_thresh_disp.setText(l)
            self.mouse.lick_threshold = int(l)
            self.lickLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_waittime(self):
        l = self.waittimeLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.waittime_disp.setText(l)
            self.mouse.waittime = int(l)
            self.waittimeLineEdit.clear()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Invalid input')
            msg.exec()

    def change_testlim(self):
        l = self.testLimLineEdit.text()
        if l.isnumeric():                   #Only positive integers (0-9)
            self.test_lim_disp.setText(l)
            self.mouse.test_limit = int(l)
            self.testLimLineEdit.clear()
        else:
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
        y = [float(i) for i in y]

        self.pltax = self.plotWid.canvas.ax
        matplotlib.pyplot.setp(self.pltax, xticks=x, xticklabels=x_lab)
        matplotlib.pyplot.setp(self.pltax.xaxis.get_majorticklabels(), rotation=90)
        self.pltax.plot(x,y,'--o')
        self.pltax.set_xlim(left=0)
        self.pltax.set_ylabel('Weight (g)')

        self.plotWid.canvas.draw()
        self.mutex.unlock()

    def updatedisplays(self):
        self.liq_am_disp.setText(str(self.mouse.liquid_amount))
        self.lick_thresh_disp.setText(str(self.mouse.lick_threshold))
        self.waittime_disp.setText(str(self.mouse.waittime))
        self.test_lim_disp.setText(str(self.mouse.test_limit))
        self.test_no_disp.setText(str(self.mouse.tests_today()))
        self.test_select.clear()
        for t in self.mouse.tests:
            if not t.ongoing:
                self.test_select.addItem(f'{t.id} - {t.starting_time}')


    
    def updatedata(self):
        self.pltgraph()
        self.updatedisplays()

    def analysis_win(self):
        test_id = self.test_select.currentText().split(' ')[0]
        if test_id:
            try:
                p = Process(target=analysis_window,args=[test_id])
                p.start()
            except Exception as e:
                logger.error(f'Error in opening analysis window - Test ID {test_id}')
            #analysis_window(test_id)
