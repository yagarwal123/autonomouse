from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect, QTimer

import sys
import os
#os.system(r"pyuic5 -x ./Python/gui/mousewin.ui -o ./Python/gui/mousewin.py")
#from gui import mainwin
from gui.doorwin import Ui_doorWin


class doorwinActions(Ui_doorWin):
    def __init__(self,doors):
        self.doors = doors
        self.title = "Doors"
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150

    # update setupUi
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # MainWindow.resize(400, 300) # do not modify it
        MainWindow.move(self.left, self.top)  # set location for window
        MainWindow.setWindowTitle(self.title) # change title
        self.timer = QTimer()
        self.timer.timeout.connect(lambda:self.popTable())
        self.timer.start(1000)

    def popTable(self):
        entries = len(self.doors)
        self.tableWidget.setRowCount(entries)
        for i in range(entries):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.doors[i][0])))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(self.doors[i][1].get_id()))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(self.doors[i][1].get_name()))

            #delete this
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(self.doors[i][1].weight[-1])))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Wid = QtWidgets.QWidget()
    ui = doorwinActions()
    ui.setupUi(Wid)
    Wid.show()
    sys.exit(app.exec_())