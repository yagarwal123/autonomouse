# Form implementation generated from reading ui file './Python/gui/mainwin.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(312, 185)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.openAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.openAllButton.setObjectName("openAllButton")
        self.gridLayout_2.addWidget(self.openAllButton, 0, 1, 1, 1)
        self.cameraButton = QtWidgets.QPushButton(self.centralwidget)
        self.cameraButton.setObjectName("cameraButton")
        self.gridLayout_2.addWidget(self.cameraButton, 1, 1, 1, 1)
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setObjectName("testButton")
        self.gridLayout_2.addWidget(self.testButton, 1, 2, 1, 1)
        self.detMouseButton = QtWidgets.QPushButton(self.centralwidget)
        self.detMouseButton.setObjectName("detMouseButton")
        self.gridLayout_2.addWidget(self.detMouseButton, 0, 2, 1, 1)
        self.doorButton = QtWidgets.QPushButton(self.centralwidget)
        self.doorButton.setObjectName("doorButton")
        self.gridLayout_2.addWidget(self.doorButton, 0, 0, 1, 1)
        self.lickButton = QtWidgets.QPushButton(self.centralwidget)
        self.lickButton.setObjectName("lickButton")
        self.gridLayout_2.addWidget(self.lickButton, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 3)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 5, 0, 1, 3)
        self.mouse_button = QtWidgets.QPushButton(self.centralwidget)
        self.mouse_button.setObjectName("mouse_button")
        self.gridLayout.addWidget(self.mouse_button, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(202, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)
        self.label_blah = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_blah.setFont(font)
        self.label_blah.setObjectName("label_blah")
        self.gridLayout.addWidget(self.label_blah, 0, 0, 1, 1)
        self.mouse_id_select = QtWidgets.QComboBox(self.centralwidget)
        self.mouse_id_select.setObjectName("mouse_id_select")
        self.gridLayout.addWidget(self.mouse_id_select, 1, 0, 1, 1)
        self.label_blah_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_blah_2.setFont(font)
        self.label_blah_2.setObjectName("label_blah_2")
        self.gridLayout.addWidget(self.label_blah_2, 3, 0, 1, 1)
        self.expButton = QtWidgets.QPushButton(self.centralwidget)
        self.expButton.setObjectName("expButton")
        self.gridLayout.addWidget(self.expButton, 6, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 312, 18))
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
        self.actioniii = QtGui.QAction(MainWindow)
        self.actioniii.setObjectName("actioniii")
        self.actionhij = QtGui.QAction(MainWindow)
        self.actionhij.setObjectName("actionhij")
        self.actionko = QtGui.QAction(MainWindow)
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
        self.openAllButton.setText(_translate("MainWindow", "Open all Windows"))
        self.cameraButton.setText(_translate("MainWindow", "Cameras"))
        self.testButton.setText(_translate("MainWindow", "Last test"))
        self.detMouseButton.setText(_translate("MainWindow", "Mouse Details"))
        self.doorButton.setText(_translate("MainWindow", "Door"))
        self.lickButton.setText(_translate("MainWindow", "Lick Detector"))
        self.mouse_button.setText(_translate("MainWindow", "Go"))
        self.label_blah.setText(_translate("MainWindow", "Mouse details"))
        self.label_blah_2.setText(_translate("MainWindow", "Sensor Readings"))
        self.expButton.setText(_translate("MainWindow", "Experiment Parameters"))
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
    sys.exit(app.exec())
