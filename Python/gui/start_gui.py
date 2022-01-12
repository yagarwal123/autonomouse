from PyQt5 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys


def startGUI():

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwinActions("Main Window")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    startGUI()