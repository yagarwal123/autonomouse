# JP this calls test_menu.py and demonstrates how to generate action on clicking menu item
import sys
from PyQt6 import QtWidgets
from gui.test_menu import mainwinActions

app = QtWidgets.QApplication(sys.argv)
#mainwin = mainwinActions(ser,START_TIME,all_mice, doors,live_licks,all_tests)
mainwin = mainwinActions()
mainwin.show()
sys.exit(app.exec()) 