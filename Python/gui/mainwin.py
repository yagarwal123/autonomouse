# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Python/gui/mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(369, 199)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_blah = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_blah.setFont(font)
        self.label_blah.setObjectName("label_blah")
        self.gridLayout.addWidget(self.label_blah, 0, 0, 1, 1)
        self.mouse_id_select = QtWidgets.QComboBox(self.centralwidget)
        self.mouse_id_select.setObjectName("mouse_id_select")
        self.mouse_id_select.addItem("")
        self.mouse_id_select.addItem("")
        self.gridLayout.addWidget(self.mouse_id_select, 1, 0, 1, 1)
        self.mouse_button = QtWidgets.QPushButton(self.centralwidget)
        self.mouse_button.setObjectName("mouse_button")
        self.gridLayout.addWidget(self.mouse_button, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(202, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)
        self.label_blah_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_blah_2.setFont(font)
        self.label_blah_2.setObjectName("label_blah_2")
        self.gridLayout.addWidget(self.label_blah_2, 3, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.irButton = QtWidgets.QPushButton(self.centralwidget)
        self.irButton.setObjectName("irButton")
        self.gridLayout_2.addWidget(self.irButton, 0, 1, 1, 1)
        self.doorButton = QtWidgets.QPushButton(self.centralwidget)
        self.doorButton.setObjectName("doorButton")
        self.gridLayout_2.addWidget(self.doorButton, 0, 0, 1, 1)
        self.lickButton = QtWidgets.QPushButton(self.centralwidget)
        self.lickButton.setObjectName("lickButton")
        self.gridLayout_2.addWidget(self.lickButton, 1, 0, 1, 1)
        self.weightButton = QtWidgets.QPushButton(self.centralwidget)
        self.weightButton.setObjectName("weightButton")
        self.gridLayout_2.addWidget(self.weightButton, 0, 2, 1, 1)
        self.cameraButton = QtWidgets.QPushButton(self.centralwidget)
        self.cameraButton.setObjectName("cameraButton")
        self.gridLayout_2.addWidget(self.cameraButton, 1, 1, 1, 1)
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setObjectName("testButton")
        self.gridLayout_2.addWidget(self.testButton, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 369, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuna = QtWidgets.QMenu(self.menuFile)
        self.menuna.setObjectName("menuna")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actioniii = QtWidgets.QAction(MainWindow)
        self.actioniii.setObjectName("actioniii")
        self.actionhij = QtWidgets.QAction(MainWindow)
        self.actionhij.setObjectName("actionhij")
        self.actionko = QtWidgets.QAction(MainWindow)
        self.actionko.setObjectName("actionko")
        self.menuna.addAction(self.actioniii)
        self.menuFile.addAction(self.menuna.menuAction())
        self.menuFile.addAction(self.actionko)
        self.menuEdit.addAction(self.actionhij)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_blah.setText(_translate("MainWindow", "Mouse details"))
        self.mouse_id_select.setItemText(0, _translate("MainWindow", "A11111 - Stuart"))
        self.mouse_id_select.setItemText(1, _translate("MainWindow", "222222 - Little"))
        self.mouse_button.setText(_translate("MainWindow", "Go"))
        self.label_blah_2.setText(_translate("MainWindow", "Sensor Readings"))
        self.irButton.setText(_translate("MainWindow", "IR Sensor"))
        self.doorButton.setText(_translate("MainWindow", "Door"))
        self.lickButton.setText(_translate("MainWindow", "Lick Detector"))
        self.weightButton.setText(_translate("MainWindow", "Weight Sensor"))
        self.cameraButton.setText(_translate("MainWindow", "Cameras"))
        self.testButton.setText(_translate("MainWindow", "Tests"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuna.setTitle(_translate("MainWindow", "na"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actioniii.setText(_translate("MainWindow", "iii"))
        self.actionhij.setText(_translate("MainWindow", "hij"))
        self.actionko.setText(_translate("MainWindow", "ko"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
