# Form implementation generated from reading ui file './Python/gui/doorwin.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_doorWin(object):
    def setupUi(self, doorWin):
        doorWin.setObjectName("doorWin")
        doorWin.resize(426, 275)
        self.gridLayout = QtWidgets.QGridLayout(doorWin)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(doorWin)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)

        self.retranslateUi(doorWin)
        QtCore.QMetaObject.connectSlotsByName(doorWin)

    def retranslateUi(self, doorWin):
        _translate = QtCore.QCoreApplication.translate
        doorWin.setWindowTitle(_translate("doorWin", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("doorWin", "Time"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("doorWin", "Mouse ID"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("doorWin", "Mouse Name"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("doorWin", "Door No"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    doorWin = QtWidgets.QWidget()
    ui = Ui_doorWin()
    ui.setupUi(doorWin)
    doorWin.show()
    sys.exit(app.exec())