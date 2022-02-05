from PyQt6 import QtWidgets
from gui.mainwin_actions import mainwinActions
import sys


def startGUI(all_mice,doors,live_licks):

    app = QtWidgets.QApplication(sys.argv)
    mainwin = mainwinActions(all_mice, doors,live_licks)
    #ui = mainwinActions(all_mice)
    mainwin.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    startGUI()