# Form implementation generated from reading ui file './Python/gui/detmousewin.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_detmouseWin(object):
    def setupUi(self, detmouseWin):
        detmouseWin.setObjectName("detmouseWin")
        detmouseWin.resize(301, 237)
        self.gridLayout = QtWidgets.QGridLayout(detmouseWin)
        self.gridLayout.setObjectName("gridLayout")
        self.m_name = QtWidgets.QLabel(detmouseWin)
        self.m_name.setLineWidth(1)
        self.m_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.m_name.setWordWrap(True)
        self.m_name.setObjectName("m_name")
        self.gridLayout.addWidget(self.m_name, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(detmouseWin)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.retranslateUi(detmouseWin)
        QtCore.QMetaObject.connectSlotsByName(detmouseWin)

    def retranslateUi(self, detmouseWin):
        _translate = QtCore.QCoreApplication.translate
        detmouseWin.setWindowTitle(_translate("detmouseWin", "Form"))
        self.m_name.setText(_translate("detmouseWin", "Please check if all the details are correct. If not, please quit the experiment and correct the mouse_info.csv file"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("detmouseWin", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("detmouseWin", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("detmouseWin", "Initial Weight"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    detmouseWin = QtWidgets.QWidget()
    ui = Ui_detmouseWin()
    ui.setupUi(detmouseWin)
    detmouseWin.show()
    sys.exit(app.exec())
