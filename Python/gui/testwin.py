# Form implementation generated from reading ui file './Python/gui/testwin.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_testWin(object):
    def setupUi(self, testWin):
        testWin.setObjectName("testWin")
        testWin.resize(432, 418)
        self.gridLayout = QtWidgets.QGridLayout(testWin)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(testWin)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.m_name = QtWidgets.QLabel(testWin)
        self.m_name.setObjectName("m_name")
        self.gridLayout.addWidget(self.m_name, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(198, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(testWin)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.m_id = QtWidgets.QLabel(testWin)
        self.m_id.setObjectName("m_id")
        self.gridLayout.addWidget(self.m_id, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(198, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(testWin)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.test_start_time = QtWidgets.QLabel(testWin)
        self.test_start_time.setObjectName("test_start_time")
        self.gridLayout.addWidget(self.test_start_time, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(198, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 2)
        self.manStartButton = QtWidgets.QPushButton(testWin)
        self.manStartButton.setObjectName("manStartButton")
        self.gridLayout.addWidget(self.manStartButton, 3, 0, 1, 1)
        self.stopButton = QtWidgets.QPushButton(testWin)
        self.stopButton.setObjectName("stopButton")
        self.gridLayout.addWidget(self.stopButton, 3, 1, 1, 1)
        self.rewardButton = QtWidgets.QPushButton(testWin)
        self.rewardButton.setObjectName("rewardButton")
        self.gridLayout.addWidget(self.rewardButton, 3, 2, 1, 1)
        self.eDoorButton = QtWidgets.QPushButton(testWin)
        self.eDoorButton.setObjectName("eDoorButton")
        self.gridLayout.addWidget(self.eDoorButton, 3, 3, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(testWin)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 4)

        self.retranslateUi(testWin)
        QtCore.QMetaObject.connectSlotsByName(testWin)

    def retranslateUi(self, testWin):
        _translate = QtCore.QCoreApplication.translate
        testWin.setWindowTitle(_translate("testWin", "Form"))
        self.label.setText(_translate("testWin", "Mouse Name -"))
        self.m_name.setText(_translate("testWin", "TextLabel"))
        self.label_2.setText(_translate("testWin", "Mouse ID - "))
        self.m_id.setText(_translate("testWin", "TextLabel"))
        self.label_3.setText(_translate("testWin", "Test start time - "))
        self.test_start_time.setText(_translate("testWin", "TextLabel"))
        self.manStartButton.setText(_translate("testWin", "Manual Start"))
        self.stopButton.setText(_translate("testWin", "Stop test"))
        self.rewardButton.setText(_translate("testWin", "Emergency reward"))
        self.eDoorButton.setText(_translate("testWin", "Emergency Door"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("testWin", "Trial"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("testWin", "Time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    testWin = QtWidgets.QWidget()
    ui = Ui_testWin()
    ui.setupUi(testWin)
    testWin.show()
    sys.exit(app.exec())
