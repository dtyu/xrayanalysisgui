# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed Jul 30 13:55:01 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
	Dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	Dialog.setWindowFlags(QtCore.Qt.Window)
        Dialog.resize(1339, 650)
        self.ModifyElement = QtGui.QPushButton(Dialog)
        self.ModifyElement.setGeometry(QtCore.QRect(230, 320, 101, 23))
        self.ModifyElement.setObjectName(_fromUtf8("ModifyElement"))
        self.TopLeftX = QtGui.QLineEdit(Dialog)
        self.TopLeftX.setGeometry(QtCore.QRect(70, 300, 41, 20))
        self.TopLeftX.setObjectName(_fromUtf8("TopLeftX"))
        self.TopLeftY = QtGui.QLineEdit(Dialog)
        self.TopLeftY.setGeometry(QtCore.QRect(160, 300, 41, 20))
        self.TopLeftY.setObjectName(_fromUtf8("TopLeftY"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(53, 270, 171, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 350, 171, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(50, 30, 201, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(50, 50, 21, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(130, 50, 21, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(210, 50, 21, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.MotorPositionX = QtGui.QLineEdit(Dialog)
        self.MotorPositionX.setEnabled(False)
        self.MotorPositionX.setGeometry(QtCore.QRect(70, 50, 41, 20))
        self.MotorPositionX.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.MotorPositionX.setObjectName(_fromUtf8("MotorPositionX"))
        self.MotorPositionY = QtGui.QLineEdit(Dialog)
        self.MotorPositionY.setEnabled(False)
        self.MotorPositionY.setGeometry(QtCore.QRect(150, 50, 41, 21))
        self.MotorPositionY.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.MotorPositionY.setObjectName(_fromUtf8("MotorPositionY"))
        self.MotorPositionZ = QtGui.QLineEdit(Dialog)
        self.MotorPositionZ.setEnabled(False)
        self.MotorPositionZ.setGeometry(QtCore.QRect(230, 50, 41, 21))
        self.MotorPositionZ.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.MotorPositionZ.setObjectName(_fromUtf8("MotorPositionZ"))
        self.toMotorPositionY = QtGui.QLineEdit(Dialog)
        self.toMotorPositionY.setGeometry(QtCore.QRect(150, 90, 41, 21))
        self.toMotorPositionY.setObjectName(_fromUtf8("toMotorPositionY"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(50, 90, 21, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.toMotorPositionZ = QtGui.QLineEdit(Dialog)
        self.toMotorPositionZ.setGeometry(QtCore.QRect(230, 90, 41, 21))
        self.toMotorPositionZ.setObjectName(_fromUtf8("toMotorPositionZ"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(210, 90, 21, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(130, 90, 21, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.toMotorPositionX = QtGui.QLineEdit(Dialog)
        self.toMotorPositionX.setGeometry(QtCore.QRect(70, 90, 41, 20))
        self.toMotorPositionX.setObjectName(_fromUtf8("toMotorPositionX"))
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(50, 300, 21, 21))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(140, 300, 21, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(140, 370, 21, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(50, 370, 21, 21))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.ScanAreaWidth = QtGui.QLineEdit(Dialog)
        self.ScanAreaWidth.setGeometry(QtCore.QRect(70, 370, 41, 20))
        self.ScanAreaWidth.setObjectName(_fromUtf8("ScanAreaWidth"))
        self.ScanAreaHeight = QtGui.QLineEdit(Dialog)
        self.ScanAreaHeight.setGeometry(QtCore.QRect(160, 370, 41, 20))
        self.ScanAreaHeight.setObjectName(_fromUtf8("ScanAreaHeight"))
        self.shiftMotorPositionX = QtGui.QLineEdit(Dialog)
        self.shiftMotorPositionX.setGeometry(QtCore.QRect(70, 160, 41, 20))
        self.shiftMotorPositionX.setObjectName(_fromUtf8("shiftMotorPositionX"))
        self.shiftMotorPositionY = QtGui.QLineEdit(Dialog)
        self.shiftMotorPositionY.setGeometry(QtCore.QRect(150, 160, 41, 20))
        self.shiftMotorPositionY.setObjectName(_fromUtf8("shiftMotorPositionY"))
        self.shiftMotorPositionZ = QtGui.QLineEdit(Dialog)
        self.shiftMotorPositionZ.setGeometry(QtCore.QRect(230, 160, 41, 20))
        self.shiftMotorPositionZ.setObjectName(_fromUtf8("shiftMotorPositionZ"))
        self.changeMotorPositionX = QtGui.QPushButton(Dialog)
        self.changeMotorPositionX.setGeometry(QtCore.QRect(70, 120, 41, 23))
        self.changeMotorPositionX.setObjectName(_fromUtf8("changeMotorPositionX"))
        self.changeMotorPositionY = QtGui.QPushButton(Dialog)
        self.changeMotorPositionY.setGeometry(QtCore.QRect(150, 120, 41, 23))
        self.changeMotorPositionY.setObjectName(_fromUtf8("changeMotorPositionY"))
        self.changeMotorPositionZ = QtGui.QPushButton(Dialog)
        self.changeMotorPositionZ.setGeometry(QtCore.QRect(230, 120, 41, 23))
        self.changeMotorPositionZ.setObjectName(_fromUtf8("changeMotorPositionZ"))
        self.minusMotorPositionX = QtGui.QPushButton(Dialog)
        self.minusMotorPositionX.setGeometry(QtCore.QRect(50, 180, 41, 23))
        self.minusMotorPositionX.setObjectName(_fromUtf8("minusMotorPositionX"))
        self.plusMotorPositionX = QtGui.QPushButton(Dialog)
        self.plusMotorPositionX.setGeometry(QtCore.QRect(90, 180, 41, 23))
        self.plusMotorPositionX.setObjectName(_fromUtf8("plusMotorPositionX"))
        self.plusMotorPositionY = QtGui.QPushButton(Dialog)
        self.plusMotorPositionY.setGeometry(QtCore.QRect(170, 180, 41, 23))
        self.plusMotorPositionY.setObjectName(_fromUtf8("plusMotorPositionY"))
        self.minusMotorPositionY = QtGui.QPushButton(Dialog)
        self.minusMotorPositionY.setGeometry(QtCore.QRect(130, 180, 41, 23))
        self.minusMotorPositionY.setObjectName(_fromUtf8("minusMotorPositionY"))
        self.plusMotorPositionZ = QtGui.QPushButton(Dialog)
        self.plusMotorPositionZ.setGeometry(QtCore.QRect(250, 180, 41, 23))
        self.plusMotorPositionZ.setObjectName(_fromUtf8("plusMotorPositionZ"))
        self.minusMotorPositionZ = QtGui.QPushButton(Dialog)
        self.minusMotorPositionZ.setGeometry(QtCore.QRect(210, 180, 41, 23))
        self.minusMotorPositionZ.setObjectName(_fromUtf8("minusMotorPositionZ"))
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setGeometry(QtCore.QRect(50, 420, 171, 21))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(50, 450, 21, 21))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.ScanStepSizeX = QtGui.QLineEdit(Dialog)
        self.ScanStepSizeX.setGeometry(QtCore.QRect(70, 450, 41, 20))
        self.ScanStepSizeX.setObjectName(_fromUtf8("ScanStepSizeX"))
        self.ScanStepSizeY = QtGui.QLineEdit(Dialog)
        self.ScanStepSizeY.setGeometry(QtCore.QRect(160, 450, 41, 20))
        self.ScanStepSizeY.setObjectName(_fromUtf8("ScanStepSizeY"))
        self.label_19 = QtGui.QLabel(Dialog)
        self.label_19.setGeometry(QtCore.QRect(140, 450, 21, 21))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.DwellTime = QtGui.QLineEdit(Dialog)
        self.DwellTime.setGeometry(QtCore.QRect(130, 500, 41, 20))
        self.DwellTime.setObjectName(_fromUtf8("DwellTime"))
        self.label_20 = QtGui.QLabel(Dialog)
        self.label_20.setGeometry(QtCore.QRect(50, 500, 71, 21))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_21 = QtGui.QLabel(Dialog)
        self.label_21.setGeometry(QtCore.QRect(180, 500, 31, 21))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_22 = QtGui.QLabel(Dialog)
        self.label_22.setGeometry(QtCore.QRect(420, 280, 71, 21))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.TimeLeft = QtGui.QLineEdit(Dialog)
        self.TimeLeft.setEnabled(False)
        self.TimeLeft.setGeometry(QtCore.QRect(490, 280, 111, 20))
        self.TimeLeft.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.TimeLeft.setObjectName(_fromUtf8("TimeLeft"))
        self.ExecuteScan = QtGui.QPushButton(Dialog)
        self.ExecuteScan.setGeometry(QtCore.QRect(70, 540, 101, 23))
        self.ExecuteScan.setObjectName(_fromUtf8("ExecuteScan"))
        self.label_23 = QtGui.QLabel(Dialog)
        self.label_23.setGeometry(QtCore.QRect(400, 10, 201, 21))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(Dialog)
        self.label_24.setGeometry(QtCore.QRect(750, 10, 201, 21))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.MoveToStartPoint = QtGui.QPushButton(Dialog)
        self.MoveToStartPoint.setGeometry(QtCore.QRect(50, 240, 131, 23))
        self.MoveToStartPoint.setObjectName(_fromUtf8("MoveToStartPoint"))
        self.graphicsView_VL = QtGui.QGraphicsView(Dialog)
        self.graphicsView_VL.setGeometry(QtCore.QRect(350, 30, 301, 241))
        self.graphicsView_VL.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.graphicsView_VL.setMouseTracking(False)
        self.graphicsView_VL.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.graphicsView_VL.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
        self.graphicsView_VL.setObjectName(_fromUtf8("graphicsView_VL"))
        self.graphicsView_XR = QtGui.QGraphicsView(Dialog)
        self.graphicsView_XR.setGeometry(QtCore.QRect(720, 30, 250, 250))
        self.graphicsView_XR.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.graphicsView_XR.setObjectName(_fromUtf8("graphicsView_XR"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(230, 360, 467, 231))
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.graphicsView_Plot = QtGui.QGraphicsView(Dialog)
        self.graphicsView_Plot.setGeometry(QtCore.QRect(720, 310, 600, 250))
        self.graphicsView_Plot.setObjectName(_fromUtf8("graphicsView_Plot"))
        self.Energy = QtGui.QRadioButton(Dialog)
        self.Energy.setGeometry(QtCore.QRect(900, 570, 89, 21))
        self.Energy.setChecked(False)
        self.Energy.setObjectName(_fromUtf8("Energy"))
        self.Channel = QtGui.QRadioButton(Dialog)
        self.Channel.setGeometry(QtCore.QRect(1080, 570, 89, 21))
        self.Channel.setChecked(True)
        self.Channel.setObjectName(_fromUtf8("Channel"))
        self.maxPixelValue = QtGui.QLineEdit(Dialog)
        self.maxPixelValue.setGeometry(QtCore.QRect(1010, 80, 51, 20))
        self.maxPixelValue.setObjectName(_fromUtf8("maxPixelValue"))
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(990, 60, 101, 21))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.minPixelValue = QtGui.QLineEdit(Dialog)
        self.minPixelValue.setGeometry(QtCore.QRect(1010, 220, 51, 20))
        self.minPixelValue.setObjectName(_fromUtf8("minPixelValue"))
        self.label_25 = QtGui.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(990, 200, 91, 21))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.MinPhotonEnergy = QtGui.QLineEdit(Dialog)
        self.MinPhotonEnergy.setGeometry(QtCore.QRect(410, 330, 71, 20))
        self.MinPhotonEnergy.setObjectName(_fromUtf8("MinPhotonEnergy"))
        self.label_27 = QtGui.QLabel(Dialog)
        self.label_27.setGeometry(QtCore.QRect(380, 310, 141, 21))
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.label_28 = QtGui.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(550, 310, 141, 21))
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.MaxPhotonEnergy = QtGui.QLineEdit(Dialog)
        self.MaxPhotonEnergy.setGeometry(QtCore.QRect(580, 330, 71, 20))
        self.MaxPhotonEnergy.setObjectName(_fromUtf8("MaxPhotonEnergy"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.ModifyElement.setText(_translate("Dialog", "Modify Element", None))
        self.label_3.setText(_translate("Dialog", "Top-Left Corner", None))
        self.label_4.setText(_translate("Dialog", "Scan Area", None))
        self.label_5.setText(_translate("Dialog", "Sample Motor Position", None))
        self.label_6.setText(_translate("Dialog", "X:", None))
        self.label_7.setText(_translate("Dialog", "Y:", None))
        self.label_8.setText(_translate("Dialog", "Z:", None))
        self.label_9.setText(_translate("Dialog", "To:", None))
        self.label_10.setText(_translate("Dialog", "To:", None))
        self.label_11.setText(_translate("Dialog", "To:", None))
        self.label_12.setText(_translate("Dialog", "X:", None))
        self.label_13.setText(_translate("Dialog", "Y:", None))
        self.label_14.setText(_translate("Dialog", "H:", None))
        self.label_15.setText(_translate("Dialog", "W:", None))
        self.changeMotorPositionX.setText(_translate("Dialog", "Go", None))
        self.changeMotorPositionY.setText(_translate("Dialog", "Go", None))
        self.changeMotorPositionZ.setText(_translate("Dialog", "Go", None))
        self.minusMotorPositionX.setText(_translate("Dialog", "-", None))
        self.plusMotorPositionX.setText(_translate("Dialog", "+", None))
        self.plusMotorPositionY.setText(_translate("Dialog", "+", None))
        self.minusMotorPositionY.setText(_translate("Dialog", "-", None))
        self.plusMotorPositionZ.setText(_translate("Dialog", "+", None))
        self.minusMotorPositionZ.setText(_translate("Dialog", "-", None))
        self.label_17.setText(_translate("Dialog", "Scan Step Size", None))
        self.label_18.setText(_translate("Dialog", "X:", None))
        self.label_19.setText(_translate("Dialog", "Y:", None))
        self.label_20.setText(_translate("Dialog", "Dwell Time:", None))
        self.label_21.setText(_translate("Dialog", "ms/pt", None))
        self.label_22.setText(_translate("Dialog", "Time Left:", None))
        self.ExecuteScan.setText(_translate("Dialog", "Execute Scan", None))
        self.label_23.setText(_translate("Dialog", "        Visible Light View", None))
        self.label_24.setText(_translate("Dialog", "            X-ray View", None))
        self.MoveToStartPoint.setText(_translate("Dialog", "Move to Start Point", None))
        self.Energy.setText(_translate("Dialog", "Energy", None))
        self.Channel.setText(_translate("Dialog", "Channel", None))
        self.label_16.setText(_translate("Dialog", "Max Pixel Value:", None))
        self.label_25.setText(_translate("Dialog", "Min Pixel Value:", None))
        self.label_27.setText(_translate("Dialog", "Min Photon Energy(eV):", None))
        self.label_28.setText(_translate("Dialog", "Max Photon Energy(eV):", None))
