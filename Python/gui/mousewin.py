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
        mouseWin.resize(626, 623)
        self.gridLayout_2 = QtWidgets.QGridLayout(mouseWin)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.test_no_disp = QtWidgets.QLabel(mouseWin)
        self.test_no_disp.setObjectName("test_no_disp")
        self.gridLayout_2.addWidget(self.test_no_disp, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.testLimLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.testLimLineEdit.setObjectName("testLimLineEdit")
        self.gridLayout.addWidget(self.testLimLineEdit, 4, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(mouseWin)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.test_lim_disp = QtWidgets.QLabel(mouseWin)
        self.test_lim_disp.setObjectName("test_lim_disp")
        self.gridLayout.addWidget(self.test_lim_disp, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(mouseWin)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.waittimeLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.waittimeLineEdit.setObjectName("waittimeLineEdit")
        self.gridLayout.addWidget(self.waittimeLineEdit, 2, 2, 1, 1)
        self.resp_disp = QtWidgets.QLabel(mouseWin)
        self.resp_disp.setObjectName("resp_disp")
        self.gridLayout.addWidget(self.resp_disp, 6, 1, 1, 1)
        self.changeTestLimButton = QtWidgets.QPushButton(mouseWin)
        self.changeTestLimButton.setObjectName("changeTestLimButton")
        self.gridLayout.addWidget(self.changeTestLimButton, 4, 3, 1, 1)
        self.changeliquidButton = QtWidgets.QPushButton(mouseWin)
        self.changeliquidButton.setObjectName("changeliquidButton")
        self.gridLayout.addWidget(self.changeliquidButton, 0, 3, 1, 1)
        self.lick_thresh_disp = QtWidgets.QLabel(mouseWin)
        self.lick_thresh_disp.setObjectName("lick_thresh_disp")
        self.gridLayout.addWidget(self.lick_thresh_disp, 1, 1, 1, 1)
        self.changewaittimeButton = QtWidgets.QPushButton(mouseWin)
        self.changewaittimeButton.setObjectName("changewaittimeButton")
        self.gridLayout.addWidget(self.changewaittimeButton, 2, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(mouseWin)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.liquidLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.liquidLineEdit.setObjectName("liquidLineEdit")
        self.gridLayout.addWidget(self.liquidLineEdit, 0, 2, 1, 1)
        self.stimProbLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.stimProbLineEdit.setObjectName("stimProbLineEdit")
        self.gridLayout.addWidget(self.stimProbLineEdit, 7, 2, 1, 1)
        self.stim_prob_disp = QtWidgets.QLabel(mouseWin)
        self.stim_prob_disp.setObjectName("stim_prob_disp")
        self.gridLayout.addWidget(self.stim_prob_disp, 7, 1, 1, 1)
        self.changeStimButton = QtWidgets.QPushButton(mouseWin)
        self.changeStimButton.setObjectName("changeStimButton")
        self.gridLayout.addWidget(self.changeStimButton, 7, 3, 1, 1)
        self.respLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.respLineEdit.setObjectName("respLineEdit")
        self.gridLayout.addWidget(self.respLineEdit, 6, 2, 1, 1)
        self.changeRespButton = QtWidgets.QPushButton(mouseWin)
        self.changeRespButton.setObjectName("changeRespButton")
        self.gridLayout.addWidget(self.changeRespButton, 6, 3, 1, 1)
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
        self.label_10 = QtWidgets.QLabel(mouseWin)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.trial_lim_disp = QtWidgets.QLabel(mouseWin)
        self.trial_lim_disp.setObjectName("trial_lim_disp")
        self.gridLayout.addWidget(self.trial_lim_disp, 5, 1, 1, 1)
        self.liq_am_disp = QtWidgets.QLabel(mouseWin)
        self.liq_am_disp.setObjectName("liq_am_disp")
        self.gridLayout.addWidget(self.liq_am_disp, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(mouseWin)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.trialLimLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.trialLimLineEdit.setObjectName("trialLimLineEdit")
        self.gridLayout.addWidget(self.trialLimLineEdit, 5, 2, 1, 1)
        self.label = QtWidgets.QLabel(mouseWin)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.changeTrialLimButton = QtWidgets.QPushButton(mouseWin)
        self.changeTrialLimButton.setObjectName("changeTrialLimButton")
        self.gridLayout.addWidget(self.changeTrialLimButton, 5, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(mouseWin)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.punishtime_disp = QtWidgets.QLabel(mouseWin)
        self.punishtime_disp.setObjectName("punishtime_disp")
        self.gridLayout.addWidget(self.punishtime_disp, 3, 1, 1, 1)
        self.punishtimeLineEdit = QtWidgets.QLineEdit(mouseWin)
        self.punishtimeLineEdit.setObjectName("punishtimeLineEdit")
        self.gridLayout.addWidget(self.punishtimeLineEdit, 3, 2, 1, 1)
        self.changepunishtimeButton = QtWidgets.QPushButton(mouseWin)
        self.changepunishtimeButton.setObjectName("changepunishtimeButton")
        self.gridLayout.addWidget(self.changepunishtimeButton, 3, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 4)
        self.line = QtWidgets.QFrame(mouseWin)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 4)
        self.speedSlider = QtWidgets.QSlider(mouseWin)
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(30)
        self.speedSlider.setSliderPosition(15)
        self.speedSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.speedSlider.setTickPosition(QtWidgets.QSlider.TickPosition.NoTicks)
        self.speedSlider.setTickInterval(1)
        self.speedSlider.setObjectName("speedSlider")
        self.gridLayout_2.addWidget(self.speedSlider, 5, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(mouseWin)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(mouseWin)
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 3, 1, 1)
        self.test_select = QtWidgets.QComboBox(mouseWin)
        self.test_select.setObjectName("test_select")
        self.gridLayout_2.addWidget(self.test_select, 4, 0, 1, 3)
        self.line_2 = QtWidgets.QFrame(mouseWin)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 3, 0, 1, 4)
        self.showAnalysisButton = QtWidgets.QPushButton(mouseWin)
        self.showAnalysisButton.setObjectName("showAnalysisButton")
        self.gridLayout_2.addWidget(self.showAnalysisButton, 4, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(mouseWin)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)
        self.plotWid = MplWidget(mouseWin)
        self.plotWid.setMinimumSize(QtCore.QSize(491, 281))
        self.plotWid.setObjectName("plotWid")
        self.gridLayout_2.addWidget(self.plotWid, 6, 0, 1, 4)

        self.retranslateUi(mouseWin)
        QtCore.QMetaObject.connectSlotsByName(mouseWin)

    def retranslateUi(self, mouseWin):
        _translate = QtCore.QCoreApplication.translate
        mouseWin.setWindowTitle(_translate("mouseWin", "Form"))
        self.test_no_disp.setText(_translate("mouseWin", "0"))
        self.label_6.setText(_translate("mouseWin", "Response Time (ms):"))
        self.test_lim_disp.setText(_translate("mouseWin", "10"))
        self.label_4.setText(_translate("mouseWin", "Test Limit:"))
        self.resp_disp.setText(_translate("mouseWin", "2500"))
        self.changeTestLimButton.setText(_translate("mouseWin", "Change"))
        self.changeliquidButton.setText(_translate("mouseWin", "Change"))
        self.lick_thresh_disp.setText(_translate("mouseWin", "2000"))
        self.changewaittimeButton.setText(_translate("mouseWin", "Change"))
        self.label_2.setText(_translate("mouseWin", "Current Lick Threshold:"))
        self.stim_prob_disp.setText(_translate("mouseWin", "70"))
        self.changeStimButton.setText(_translate("mouseWin", "Change"))
        self.changeRespButton.setText(_translate("mouseWin", "Change"))
        self.changelickButton.setText(_translate("mouseWin", "Change"))
        self.label_3.setText(_translate("mouseWin", "Current Wait Time (ms):"))
        self.waittime_disp.setText(_translate("mouseWin", "5000"))
        self.label_10.setText(_translate("mouseWin", "Current Liquid Amount:"))
        self.trial_lim_disp.setText(_translate("mouseWin", "None"))
        self.liq_am_disp.setText(_translate("mouseWin", "2000"))
        self.label_9.setText(_translate("mouseWin", "Stimulus Probability:"))
        self.label.setText(_translate("mouseWin", "Trial Limit"))
        self.changeTrialLimButton.setText(_translate("mouseWin", "Change"))
        self.label_11.setText(_translate("mouseWin", "Current Punish Time (ms):"))
        self.punishtime_disp.setText(_translate("mouseWin", "0"))
        self.changepunishtimeButton.setText(_translate("mouseWin", "Change"))
        self.label_5.setText(_translate("mouseWin", "Tests attempted today:"))
        self.label_8.setText(_translate("mouseWin", "Faster"))
        self.showAnalysisButton.setText(_translate("mouseWin", "Show analysis window"))
        self.label_7.setText(_translate("mouseWin", "Slower"))
from gui.mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mouseWin = QtWidgets.QWidget()
    ui = Ui_mouseWin()
    ui.setupUi(mouseWin)
    mouseWin.show()
    sys.exit(app.exec())
