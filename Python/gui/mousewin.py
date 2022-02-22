# Form implementation generated from reading ui file './Python/gui/mousewin.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_mouseWin(object):
    def setupUi(self, mouseWin):
        mouseWin.setObjectName("mouseWin")
        mouseWin.resize(509, 395)
        self.gridLayout = QtWidgets.QGridLayout(mouseWin)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(mouseWin)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.liq_am_disp = QtWidgets.QLabel(mouseWin)
        self.liq_am_disp.setObjectName("liq_am_disp")
        self.gridLayout.addWidget(self.liq_am_disp, 0, 1, 1, 1)
        self.liquidLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.liquidLineEdit.setObjectName("liquidLineEdit")
        self.gridLayout.addWidget(self.liquidLineEdit, 0, 2, 1, 1)
        self.changeliquidButton = QtWidgets.QPushButton(mouseWin)
        self.changeliquidButton.setObjectName("changeliquidButton")
        self.gridLayout.addWidget(self.changeliquidButton, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(mouseWin)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lick_thresh_disp = QtWidgets.QLabel(mouseWin)
        self.lick_thresh_disp.setObjectName("lick_thresh_disp")
        self.gridLayout.addWidget(self.lick_thresh_disp, 1, 1, 1, 1)
        self.lickLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.lickLineEdit.setObjectName("lickLineEdit")
        self.gridLayout.addWidget(self.lickLineEdit, 1, 2, 1, 1)
        self.changelickButton = QtWidgets.QPushButton(mouseWin)
        self.changelickButton.setObjectName("changelickButton")
        self.gridLayout.addWidget(self.changelickButton, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(mouseWin)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.waittime_disp = QtWidgets.QLabel(mouseWin)
        self.waittime_disp.setObjectName("waittime_disp")
        self.gridLayout.addWidget(self.waittime_disp, 2, 1, 1, 1)
        self.waittimeLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.waittimeLineEdit.setObjectName("waittimeLineEdit")
        self.gridLayout.addWidget(self.waittimeLineEdit, 2, 2, 1, 1)
        self.changewaittimeButton = QtWidgets.QPushButton(mouseWin)
        self.changewaittimeButton.setObjectName("changewaittimeButton")
        self.gridLayout.addWidget(self.changewaittimeButton, 2, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(mouseWin)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 4)
        self.plotWid = MplWidget(mouseWin)
        self.plotWid.setMinimumSize(QtCore.QSize(491, 281))
        self.plotWid.setObjectName("plotWid")
        self.gridLayout.addWidget(self.plotWid, 4, 0, 1, 4)

        self.retranslateUi(mouseWin)
        QtCore.QMetaObject.connectSlotsByName(mouseWin)

    def retranslateUi(self, mouseWin):
        _translate = QtCore.QCoreApplication.translate
        mouseWin.setWindowTitle(_translate("mouseWin", "Form"))
        self.label.setText(_translate("mouseWin", "Current Liquid Amount:"))
        self.liq_am_disp.setText(_translate("mouseWin", "1000"))
        self.changeliquidButton.setText(_translate("mouseWin", "Change"))
        self.label_2.setText(_translate("mouseWin", "Current Lick Threshold:"))
        self.lick_thresh_disp.setText(_translate("mouseWin", "2000"))
        self.changelickButton.setText(_translate("mouseWin", "Change"))
        self.label_3.setText(_translate("mouseWin", "Current Wait Time (ms):"))
        self.waittime_disp.setText(_translate("mouseWin", "5000"))
        self.changewaittimeButton.setText(_translate("mouseWin", "Change"))
from gui.mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mouseWin = QtWidgets.QWidget()
    ui = Ui_mouseWin()
    ui.setupUi(mouseWin)
    mouseWin.show()
    sys.exit(app.exec())
