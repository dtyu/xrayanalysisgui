#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from MainWindow import *
from ElementsDialog import *
from selectElements import *

import h5py
import numpy as np
import matplotlib 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from copy import deepcopy

import epics
import time

# Class for the main Dialog
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Set properties of buttons
        self.ui.ModifyElement.setDefault(False)
        self.ui.ModifyElement.setAutoDefault(False)
        self.ui.changeMotorPositionX.setDefault(False)
        self.ui.changeMotorPositionX.setAutoDefault(False)
        self.ui.changeMotorPositionY.setDefault(False)
        self.ui.changeMotorPositionY.setAutoDefault(False)
        self.ui.changeMotorPositionZ.setDefault(False)
        self.ui.changeMotorPositionZ.setAutoDefault(False)
        self.ui.minusMotorPositionX.setDefault(False)
        self.ui.minusMotorPositionX.setAutoDefault(False)
        self.ui.minusMotorPositionY.setDefault(False)
        self.ui.minusMotorPositionY.setAutoDefault(False)
        self.ui.minusMotorPositionZ.setDefault(False)
        self.ui.minusMotorPositionZ.setAutoDefault(False)
        self.ui.plusMotorPositionX.setDefault(False)
        self.ui.plusMotorPositionX.setAutoDefault(False)
        self.ui.plusMotorPositionY.setDefault(False)
        self.ui.plusMotorPositionY.setAutoDefault(False)
        self.ui.plusMotorPositionZ.setDefault(False)
        self.ui.plusMotorPositionZ.setAutoDefault(False)
        self.ui.MoveToStartPoint.setDefault(False)
        self.ui.MoveToStartPoint.setAutoDefault(False)
        self.ui.ExecuteScan.setDefault(False)
        self.ui.ExecuteScan.setAutoDefault(False)
        self.ui.ChangeDirectory.setDefault(False)
        self.ui.ChangeDirectory.setAutoDefault(False)
        self.ui.AbortScan.setDefault(False)
        self.ui.AbortScan.setAutoDefault(False)
        
        # Create scene_Plot
        self.scene_Plot = QGraphicsScene()
        # Set scene_Plot in graphicsView_Plot
        self.ui.graphicsView_Plot.setScene(self.scene_Plot)
        # Create scene_XR
        self.scene_XR = QGraphicsScene(self)
        # Set scene_XR in graphicsView_XR
        self.ui.graphicsView_XR.setScene(self.scene_XR)
        # Create scene_VL
        self.scene_VL = QGraphicsScene()
        # Set the scene in the first GraphicsView
        self.ui.graphicsView_VL.setScene(self.scene_VL)
        
        # Load the first image
        self.pixmap_VL = QtGui.QPixmap("image1.jpg")
        # Create the first GraphicsPixmapItem
        self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
        # Add the item to the first GraphicsScene
        self.scene_VL.addItem(self.pixmapItem_VL)
        
        # Create RubberBand in GraphicsView_VL
        self.rubberBand_VL = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,self.ui.graphicsView_VL)
        # Create rectangle & rectangleItem in GraphicsScene_VL
        self.selectedRect_VL = QRectF()
        self.selectedRectItem_VL = self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
        # Create RubberBand in GraphicsView_XR
        self.rubberBand_XR = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,self.ui.graphicsView_XR)
        # Create rectangle & rectangleItem in GraphicsScene_XR
        self.selectedRect_XR = QRectF()
        self.selectedRectItem_XR = self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
        
        '''
        [0] represents Li, [1] represents Be, [2] represents B, [3] represents C,
        [4] represents N, [5] represents O, [6] represents F, [7] represents Ne,
        [8] represents Na, [9] represents Mg, [10] represents Al, [11] represents Si,
        [12] represents P, [13] represents S, [14] represents Cl, [15] represents Ar,
        [16] represents K, [17] represents Ca, [18] represents Sc, [19] represents Ti,
        [20] represents V, [21] represents Cr, [22] represents Mn, [23] represents Fe,
        [24] represents Co, [25] represents Ni, [26] represents Cu, [27] represents Zn,
        [28] represents Ga, [29] represents Ge, [30] represents As, [31] represents Se,
        [32] represents Br, [33] represents Kr, [34] represents Rb, [35] represents Sr,
        [36] represents Y, [37] represents Zr, [38] represents Nb, [39] represents Mo,
        [40] represents Tc, [41] represents Ru, [42] represents Rh, [43] represents Pd,
        [44] represents Ag, [45] represents Cd, [46] represents In, [47] represents Sn,
        [48] represents Sb, [49] represents Te, [50] represents I, [51] represents Xe,
        [52] represents Cs, [53] represents Ba, [54] represents Hf, [55] represents Ta,
        [56] represents W, [57] represents Re, [58] represents Os, [59] represents Ir,
        [60] represents Pt, [61] represents Au, [62] represents Hg, [63] represents Tl,
        [64] represents Pb, [65] represents Bi, [66] represents Po, [67] represents At,
        [68] represents Rn, [69] represents Fr, [70] represents Ra, [71] represents La,
        [72] represents Ce, [73] represents Pr, [74] represents Nd, [75] represents Pm,
        [76] represents Sm, [77] represents Eu, [78] represents Gd, [79] represents Tb,
        [80] represents Dy, [81] represents Ho, [82] represents Er, [83] represents Tm,
        [84] represents Yb, [85] represents Lu, [86] represents Ac, [87] represents Th,
        [88] represents Pa, [89] represents U, [90] represents Np, [91] represents Pu,
        [92] represents Am,
        '''
        # element symbol (93 in total, from Li to Am)
        self.knownElements = ["Li","Be","B","C","N","O","F","Ne","Na","Mg",
                              "Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti",
                              "V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge",
                              "As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo",
                              "Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te",
                              "I","Xe","Cs","Ba","Hf","Ta","W","Re","Os","Ir",
                              "Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr",
                              "Ra","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb",
                              "Dy","Ho","Er","Tm","Yb","Lu","Ac","Th","Pa","U",
                              "Np","Pu","Am"]
        # current status (-1 means not available, 0 means not selected, 1 means selected)
        self.currentElementsStatus = [0]*len(self.knownElements)
        # previous status
        self.previousElementsStatus = self.currentElementsStatus
        # amount of energy levels within range for each element
        self.availableEnergyCount = [0]*len(self.knownElements)
        # photon energy data (from .txt file)
        self.PhotonEnergy = np.loadtxt('PhotonEnergy.txt')
        # modified photon energy data (using minEnergy & maxEnergy) 
        self.modifiedPhotonEnergy = deepcopy(self.PhotonEnergy)
        # min energy(KeV)
        self.minEnergy = 1
        # max energy(KeV)
        self.maxEnergy = 26000
        # energy level label (e.g. Kalpha1)
        self.energyLabel = [u"K\u03b11: ",u"K\u03b12: ",u"K\u03b21: ",
                            u"L\u03b11: ",u"L\u03b12: ",u"L\u03b21: ",
                            u"L\u03b22: ",u"L\u03b31: ",u"M\u03b11: "]
        # energy level selected for each element
        self.scanEnergyLevel = [0]*len(self.knownElements)
        # energy range entered for each element
        self.scanEnergyRange = [300]*len(self.knownElements)
        
        # Update availableEnergyCount, modifiedPhotonEnergy & currentElementsStatus
        for i in range(len(self.PhotonEnergy)):
            for j in range(len(self.PhotonEnergy[0])):
                # If PhotonEnergy[i][j] is in range, availableEnergyCount[i] ++
                if (self.PhotonEnergy[i][j] >= self.minEnergy) and (self.PhotonEnergy[i][j] <= self.maxEnergy):
                    self.availableEnergyCount[i] = self.availableEnergyCount[i] + 1
                # Otherwise, modifiedEnergyCount[i][j] = 0
                else:
                    self.modifiedPhotonEnergy[i][j] = 0
            # If no energy level is in range, currentElementsStatus = -1
            if (self.availableEnergyCount[i] == 0):
                self.currentElementsStatus[i] = -1
        # Show min energy, Connect "editingFinished" event handler
        self.ui.MinPhotonEnergy.setText(unicode(self.minEnergy))
        self.ui.MinPhotonEnergy.editingFinished.connect(self.MinPhotonEnergy_EditingFinished)
        # Show max energy, Connect "editingFinished" event handler
        self.ui.MaxPhotonEnergy.setText(unicode(self.maxEnergy))
        self.ui.MaxPhotonEnergy.editingFinished.connect(self.MaxPhotonEnergy_EditingFinished)

        # Total Scan Count
        self.scanCount = 1
        # Abort Signal
        self.abort = 0
        # File Directory (Default is current working directory)
        self.directory = QDir.currentPath() + "/"
        # Show File Directory
        self.ui.Directory.setText(self.directory)
        # File Name
        self.fileName = unicode(QDate.currentDate().year()) \
                        + unicode(format(QDate.currentDate().month(), '02d')) \
                        + unicode(format(QDate.currentDate().day(), '02d')) \
                        + "_" + unicode(format(self.scanCount, '03d')) \
                        + "_Sample"
        # Show File Name
        self.ui.FileName.setText(self.fileName)
        # Connect "editingFinished" event handler
        self.ui.FileName.editingFinished.connect(self.FileName_EditingFinished)
        
        # motor position
        ## self.motor1 = epics.PV('test:motorx1.VAL')
        self.motor1 = epics.Device('test:motorx1.', attrs=('VAL', 'RBV', 'DESC', 'RVAL', 'LVIO', 'HLS', 'LLS'))
        self.xPos = self.motor1.get('RBV')
        self.motor2 = epics.Device('test:motorx2.', attrs=('VAL', 'RBV', 'DESC', 'RVAL', 'LVIO', 'HLS', 'LLS'))
        self.yPos = self.motor2.get('RBV')
        self.motor3 = epics.Device('test:motorx3.', attrs=('VAL', 'RBV', 'DESC', 'RVAL', 'LVIO', 'HLS', 'LLS'))
        self.zPos = self.motor3.get('RBV')
        # motor position shift (initialized as 0,0,0)
        self.xStep = 0
        self.yStep = 0
        self.zStep = 0
        # scan step size (initialized as 1,1)
        self.scanStepX = 1
        self.scanStepY = 1
        # dwell time (initialized as 0.1)
        self.dwellTime = 0.1
        
        # width & height of ROI in GraphicsView_VL (initialized as 0,0)
        self.width_VL = 0
        self.height_VL = 0
        # top-left point of ROI in GraphicsView_VL (initialized as (0,0))
        self.startPos_VL = QPoint(0,0)
        # width & height of ROI in GraphicsView_XR (initialized as 0,0)
        self.width_XR = 0
        self.height_XR = 0
        # top-left point of ROI in GraphicsView_XR (initialized as (0,0))
        self.startPos_XR = QPoint(0,0)
        # whether ROI has been selected in GraphicsView_VL (1 means has, 0 means not)
        self.selected_VL = 0
        # whether ROI has been selected in GraphicsView_XR (1 means has, 0 means not)
        self.selected_XR = 0
        
        # Show top-left point of ROI (x,y), Connect "editingFinished" event handler
        self.ui.TopLeftX.setText(unicode(self.startPos_XR.x()))
        self.ui.TopLeftX.editingFinished.connect(self.TopLeftX_EditingFinished)
        self.ui.TopLeftY.setText(unicode(self.startPos_XR.y()))
        self.ui.TopLeftY.editingFinished.connect(self.TopLeftY_EditingFinished)
        # Show width of ROI, Connect "editingFinished" event handler
        self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
        self.ui.ScanAreaWidth.editingFinished.connect(self.ScanAreaWidth_EditingFinished)
        # Show width of ROI, Connect "editingFinished" event handler
        self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
        self.ui.ScanAreaHeight.editingFinished.connect(self.ScanAreaHeight_EditingFinished)
        # Show current motor position
        self.ui.MotorPositionX.setText(unicode(self.xPos))
        self.ui.MotorPositionY.setText(unicode(self.yPos))
        self.ui.MotorPositionZ.setText(unicode(self.zPos))
        # Show new motor position
        self.ui.toMotorPositionX.setText(unicode(self.xPos))
        self.ui.toMotorPositionY.setText(unicode(self.yPos))
        self.ui.toMotorPositionZ.setText(unicode(self.zPos))
        # Show motor position shift
        self.ui.shiftMotorPositionX.setText(unicode(self.xStep))
        self.ui.shiftMotorPositionY.setText(unicode(self.yStep))
        self.ui.shiftMotorPositionZ.setText(unicode(self.zStep))
        # Show scan step size (in x & y coordinate)
        self.ui.ScanStepSizeX.setText(unicode(self.scanStepX))
        self.ui.ScanStepSizeY.setText(unicode(self.scanStepY))
        # Show dwell time
        self.ui.DwellTime.setText(unicode(self.dwellTime))
        
        # Set titles in table widget
        self.ui.tableWidget.setHorizontalHeaderLabels([QString("Element"),
                                                       QString("Energy(KeV)"),
                                                       QString("Range(eV)"),
                                                       QString("Count")])
        # Set column width in table widget
        self.ui.tableWidget.setColumnWidth(0,100)
        self.ui.tableWidget.setColumnWidth(1,150)
        self.ui.tableWidget.setColumnWidth(2,100)
        self.ui.tableWidget.setColumnWidth(3,100)
        # Connect "cellDoubleClicked" event handler
        self.ui.tableWidget.cellDoubleClicked.connect(self.handleCellDoubleClicked)
        # Connect "cellChanged" event handler
        self.ui.tableWidget.cellChanged.connect(self.handleCellChanged)
        
        # Connect "radio button clicked" event handlers
        self.ui.Energy.toggled.connect(self.Energy_clicked)
        self.ui.Channel.toggled.connect(self.Channel_clicked)

        # Connect "window close" event handler
        self.connect(self, QtCore.SIGNAL('triggered()'),self.closeEvent)

    '''
    "main window close" event handler
    '''
    def closeEvent(self, event):
        print "Closing"
        # Clear scene_Plot, sccene_XR & scene_VL
        self.scene_Plot.clear()
        self.scene_XR.clear()
        self.scene_VL.clear()
        
    '''
    "mouse press" event handler, "mouse move" event handler &
    "mouse release" event handler in graphicsView_VL & graphicsView_XR
    '''
    def eventFilter(self, source, event):
        # "mouse press" event in graphicsView_VL
        if (event.type() == QtCore.QEvent.GraphicsSceneMousePress
                and source is self.scene_VL):
            if event.button() == QtCore.Qt.LeftButton:
                # Remove selectedRectItem_VL OR selectedRectItem_XR
                if (self.selected_VL == 1):
                    self.scene_VL.removeItem(self.selectedRectItem_VL)
                elif (self.selected_XR == 1):
                    self.scene_XR.removeItem(self.selectedRectItem_XR)
                # Set selected_VL & selected_XR = 0
                self.selected_VL = 0
                self.selected_XR = 0
                # Set width & height of ROI to 0
                self.width_VL = 0
                self.height_VL = 0
                # Show width & height of ROI
                self.ui.ScanAreaWidth.setText(unicode(self.width_VL))
                self.ui.ScanAreaHeight.setText(unicode(self.height_VL))
                
                # Get mouse coordinates
                self.startPos_VL = self.ui.graphicsView_VL.mapFromScene(event.scenePos())
                # Show top-left point coordinates
                self.ui.TopLeftX.setText(unicode(self.startPos_VL.x()))
                self.ui.TopLeftY.setText(unicode(self.startPos_VL.y()))
                # Start rubberBand
                self.rubberBand_VL.setGeometry(QtCore.QRect(self.startPos_VL,
                                                            QtCore.QSize()))
                self.rubberBand_VL.show()
                
                return super(MyForm, self).eventFilter(source, event)
        # "mouse move" event in graphicsView_VL
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseMove
                and source is self.scene_VL):
            if event.buttons() == Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_VL = self.ui.graphicsView_VL.mapFromScene(event.scenePos())
                # Update the rubberBand
                if self.rubberBand_VL.isVisible():
                    self.rubberBand_VL.setGeometry(QtCore.QRect(self.startPos_VL,
                                                                self.currentPos_VL).normalized())
    
                return super(MyForm, self).eventFilter(source, event)
        # "mouse release" event in graphicsView_VL
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseRelease
                and source is self.scene_VL):
            if event.button() == QtCore.Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_VL = self.ui.graphicsView_VL.mapFromScene(event.scenePos())
                # Calculate width & height of ROI
                self.width_VL = self.currentPos_VL.x() - self.startPos_VL.x()
                self.height_VL = self.currentPos_VL.y() - self.startPos_VL.y()
                # Set selected_VL = 1
                self.selected_VL = 1
                # Hide rubberBand_VL
                self.rubberBand_VL.hide()
                # Draw a red rectangle to show ROI
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.selectedRectItem_VL = self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
                # Show width & height of ROI
                self.ui.ScanAreaWidth.setText(unicode(self.width_VL))
                self.ui.ScanAreaHeight.setText(unicode(self.height_VL))
                
                return super(MyForm, self).eventFilter(source, event)

        # "mouse press" event in graphicsView_XR
        if (event.type() == QtCore.QEvent.GraphicsSceneMousePress
                and source is self.scene_XR):
            if event.button() == QtCore.Qt.LeftButton:
                # Remove selectedRectItem_VL OR selectedRectItem_XR
                if (self.selected_VL == 1):
                    self.scene_VL.removeItem(self.selectedRectItem_VL)
                elif (self.selected_XR == 1):
                    self.scene_XR.removeItem(self.selectedRectItem_XR)
                # Set selected_VL & selected_XR = 0
                self.selected_VL = 0
                self.selected_XR = 0
                # Set width & height of ROI to 0
                self.width_XR = 0
                self.height_XR = 0
                # Show width & height of ROI
                self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
                self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
                
                # Get mouse coordinates
                self.startPos_XR = self.ui.graphicsView_XR.mapFromScene(event.scenePos())
                # Show top-left point coordinates
                self.ui.TopLeftX.setText(unicode(self.startPos_XR.x()))
                self.ui.TopLeftY.setText(unicode(self.startPos_XR.y()))
                # Start rubberBand
                self.rubberBand_XR.setGeometry(QtCore.QRect(self.startPos_XR, QtCore.QSize()))
                self.rubberBand_XR.show()
                
                return super(MyForm, self).eventFilter(source, event)
        # "mouse move" event in graphicsView_XR
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseMove
                and source is self.scene_XR):
            if event.buttons() == Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_XR = self.ui.graphicsView_XR.mapFromScene(event.scenePos())
                # Update the rubberBand
                if self.rubberBand_XR.isVisible():
                    self.rubberBand_XR.setGeometry(QtCore.QRect(self.startPos_XR,
                                                                self.currentPos_XR).normalized())
    
                return super(MyForm, self).eventFilter(source, event)
        # "mouse release" event in graphicsView_XR
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseRelease
                and source is self.scene_XR):
            if event.button() == QtCore.Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_XR = self.ui.graphicsView_XR.mapFromScene(event.scenePos())
                # Calculate width & height of ROI
                self.width_XR = self.currentPos_XR.x() - self.startPos_XR.x()
                self.height_XR = self.currentPos_XR.y() - self.startPos_XR.y()
                # Set selected_XR = 1
                self.selected_XR = 1
                # Hide rubberBand_XR
                self.rubberBand_XR.hide()
                # Draw a red rectangle to show ROI
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
                # Show width & height of ROI
                self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
                self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
                
                return super(MyForm, self).eventFilter(source, event)
        
        return False

    '''
    "MotorPositionX clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_changeMotorPositionX_clicked(self, checked=None):
        # Update xPos
        self.xPos = float(self.ui.toMotorPositionX.text())
        # Move motor1
        self.motor1.put('VAL',self.xPos)
        while (self.motor1.get('RBV') != self.xPos):
            time.sleep(0.001)
            self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
            self.ui.MotorPositionX.repaint()
    '''
    "MotorPositionY clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_changeMotorPositionY_clicked(self, checked=None):
        # Update yPos
        self.yPos = float(self.ui.toMotorPositionY.text())
        # Move motor2
        self.motor2.put('VAL',self.yPos)
        while (self.motor2.get('RBV') != self.yPos):
            time.sleep(0.001)
            self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
            self.ui.MotorPositionY.repaint()
    '''
    "MotorPositionZ clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_changeMotorPositionZ_clicked(self, checked=None):
        # Update zPos
        self.zPos = float(self.ui.toMotorPositionZ.text())
        # Move motor3
        self.motor3.put('VAL',self.zPos)
        while (self.motor3.get('RBV') != self.zPos):
            time.sleep(0.001)
            self.ui.MotorPositionZ.setText(unicode(self.motor3.get('RBV')))
            self.ui.MotorPositionZ.repaint()
    
    '''
    "minusMotorPositionX clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_minusMotorPositionX_clicked(self, checked=None):
        # Update xPos
        self.xStep = int(self.ui.shiftMotorPositionX.text())
        self.xPos -= self.xStep
        # Move motor1
        self.motor1.put('VAL',self.xPos)
        while (self.motor1.get('RBV') != self.xPos):
            time.sleep(0.001)
            self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
            self.ui.MotorPositionX.repaint()
    '''
    "plusMotorPositionX clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_plusMotorPositionX_clicked(self, checked=None):
        # Update xPos
        self.xStep = int(self.ui.shiftMotorPositionX.text())
        self.xPos += self.xStep
        # Move motor1
        self.motor1.put('VAL',self.xPos)
        while (self.motor1.get('RBV') != self.xPos):
            time.sleep(0.001)
            self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
            self.ui.MotorPositionX.repaint()
    '''
    "minusMotorPositionY clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_minusMotorPositionY_clicked(self, checked=None):
        # Update yPos
        self.yStep = int(self.ui.shiftMotorPositionY.text())
        self.yPos -= self.yStep
        # Move motor2
        self.motor2.put('VAL',self.yPos)
        while (self.motor2.get('RBV') != self.yPos):
            time.sleep(0.001)
            self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
            self.ui.MotorPositionY.repaint()
    '''
    "plusMotorPositionY clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_plusMotorPositionY_clicked(self, checked=None):
        # Update yPos
        self.yStep = int(self.ui.shiftMotorPositionY.text())
        self.yPos += self.yStep
        # Move motor2
        self.motor2.put('VAL',self.yPos)
        while (self.motor2.get('RBV') != self.yPos):
            time.sleep(0.001)
            self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
            self.ui.MotorPositionY.repaint()
    '''
    "minusMotorPositionZ clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_minusMotorPositionZ_clicked(self, checked=None):
        # Update zPos
        self.zStep = int(self.ui.shiftMotorPositionZ.text())
        self.zPos -= self.zStep
        # Move motor3
        self.motor3.put('VAL',self.zPos)
        while (self.motor3.get('RBV') != self.zPos):
            time.sleep(0.001)
            self.ui.MotorPositionZ.setText(unicode(self.motor3.get('RBV')))
            self.ui.MotorPositionZ.repaint()
    '''
    "plusMotorPositionZ clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_plusMotorPositionZ_clicked(self, checked=None):
        # Update zPos
        self.zStep = int(self.ui.shiftMotorPositionZ.text())
        self.zPos += self.zStep
        # Move motor3
        self.motor3.put('VAL',self.zPos)
        while (self.motor3.get('RBV') != self.zPos):
            time.sleep(0.001)
            self.ui.MotorPositionZ.setText(unicode(self.motor3.get('RBV')))
            self.ui.MotorPositionZ.repaint()

    '''
    "ExecuteScan clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_ExecuteScan_clicked(self, checked=None):
        # Check if ROI has been selected
        if (self.selected_VL != 1 and self.selected_XR != 1):
            print "Please select ROI first!"
            QMessageBox.about(self, "Error","Please select ROI first!")
        else:
            # Check if motor has moved to top-left point
            if (self.xPos != int(self.ui.TopLeftX.text())
                    or self.yPos != int(self.ui.TopLeftY.text())):
                print "Please click MoveToStartPoint button first!"
                QMessageBox.about(self, "Error","Please click MoveToStartPoint button first!")
            else:
                # Update ScanStepSizeX
                self.scanStepX = int(self.ui.ScanStepSizeX.text())
                # Update ScanStepSizeY
                self.scanStepY = int(self.ui.ScanStepSizeY.text())
                # Update DwellTime
                self.dwellTime = float(self.ui.DwellTime.text())
                
                # If ROI is in scene_VL
                if self.selected_VL == 1:
                    ## Calculate TimeLeft
                    # self.timeLeft = self.width_VL * self.height_VL / (self.dwellTime * 1000)
                    ## Show TimeLeft
                    # self.ui.TimeLeft.setText(unicode(self.timeLeft)+"s")

                    # Open HDF5 file
                    self.hdf5File = h5py.File('2xfm_0430.h5','r+')
                    # Load data from HDF5 file
                    self.loadData_XR = self.hdf5File['MAPS/XRF_roi']
                    print "Open file 'XRF_roi'"
                    self.loadData_Plot = self.hdf5File['MAPS/mca_arr']
                    print "Open file 'mca_arr'"
                    self.calib = self.hdf5File['MAPS/energy_calib']
                    print "Open file 'energy_calib'"

                    # data in y coordinates
                    self.plotData = [0]*2000
                    # data in x coordinates
                    self.energy = [0]*2000
                    # Calculate energy
                    for i in range(2000):
                        self.energy[i] = i * self.calib[1] + self.calib[0]

                    # Retrieve data of one element (Mg in this case)
                    self.oriImageData_XR = self.loadData_XR[0]

                    # Write HDF5 file
                    myfile = unicode(self.directory + self.fileName + ".hdf5")
                    self.testFile = h5py.File(myfile, "w")
                    dset = self.testFile.create_dataset('subgroup/dataset',
                                                        (len(self.oriImageData_XR),
                                                         len(self.oriImageData_XR[0])),
                                                        dtype='d')
                    
                    self.width_VL = 25
                    self.height_VL = 23
                    # motor coordinates of ROI
                    startPosX = self.xPos
                    endPosX = self.xPos + self.width_VL
                    startPosY = self.yPos
                    endPosY = self.yPos + self.height_VL                    

                    print "Start"

                    for i in xrange(startPosY,endPosY,self.scanStepY):
                        # Show TimeLeft
                        self.ui.TimeLeft.setText(unicode(i-startPosY+1)+" / "+unicode(len(self.oriImageData_XR)))

                        '''
                        # Move motor1 to endPosX
                        self.motor1.put('VAL',endPosX)
                        while (self.motor1.get('RBV') != endPosX):
                            time.sleep(0.001)
                            self.xPos = self.motor1.get('RBV')
                            self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
                            self.ui.MotorPositionX.repaint()
                        '''
                        for j in xrange(startPosX,endPosX,self.scanStepX):
                            if (self.abort != 1):
                                # Move motor1 to next position
                                self.xPos = j
                                self.motor1.put('VAL',self.xPos)
                                while (self.motor1.get('RBV') != self.xPos):
                                    time.sleep(0.001)
                                    self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
                                    self.ui.MotorPositionX.repaint()
                                self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
                                self.ui.MotorPositionX.repaint()
                                # Acquire scan data #
                                time.sleep(0.5)

                        if (self.abort != 1): 
                            # Write data
                            dset[i-startPosY,:] = self.oriImageData_XR[i-startPosY]

                            # self.tempFile = h5py.File('mytestfile.h5','r+')
                            self.imageData_XR = self.testFile['subgroup/dataset'] 
                        
                            # Get max & min pixel value
                            self.scale_min = np.min(self.imageData_XR)
                            self.scale_max = np.max(self.imageData_XR)
                        	# Show max & min value
                            self.ui.minPixelValue.setText(unicode(self.scale_min))
                            self.ui.maxPixelValue.setText(unicode(self.scale_max))
                        
                            # Transfer newImageData_XR to Image_XR
                            myimage = unicode(self.directory+self.fileName+".tif")
                            plt.imsave(myimage, self.imageData_XR, cmap=plt.cm.gray)
                            
                            self.pixmap_XR = QtGui.QPixmap(unicode(self.directory+self.fileName+".tif"))
                        
                            # Resize pixmap_XR
                            self.sizeWidth = 200
                            self.sizeHeight = 200
                            self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,self.sizeHeight,QtCore.Qt.IgnoreAspectRatio)

                            # Update pixmapItem_XR
                            pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                            # Add pixapItem_XR
                            self.scene_XR.addItem(pixmapItem_XR)
                            # Set scene_XR in graphicsView_XR
                            self.ui.graphicsView_XR.setScene(self.scene_XR)
                            
                            # Calculate plotData
                            for k in range(2000):
                                self.plotData[k] = self.plotData[k] + np.sum(self.loadData_Plot[k,i-startPosY])
                            # Plot
                            self.paintPlot()
                            # Adjust viewport to fit scene_Plot
                            self.ui.graphicsView_XR.fitInView(self.scene_Plot.sceneRect())
                            # Adjust viewport to fit pixmapItem_XR
                            self.ui.graphicsView_XR.fitInView(pixmapItem_XR)
                            # Call repaint method to refresh graphicsView_Plot
                            self.ui.graphicsView_Plot.viewport().repaint()
                            # Call repaint method to refresh graphicsView_XR
                            self.ui.graphicsView_XR.viewport().repaint()

                            # Wait for 1 second
                            time.sleep(1)

                        	# Move motor1 back to startPosX
                            self.motor1.put('VAL',startPosX)
                            while (self.motor1.get('RBV') != startPosX):
                                time.sleep(0.001)
                                self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
                                self.ui.MotorPositionX.repaint()
                            # Move motor2 to next line
                            self.yPos = i+self.scanStepY
                            self.motor2.put('VAL',self.yPos)
                            while (self.motor2.get('RBV') != self.yPos):
                                time.sleep(0.001)
                                self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
                                self.ui.MotorPositionY.repaint()
                            self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
                            self.ui.MotorPositionY.repaint()
                        else:
							# Show warning message
                            QMessageBox.about(self, "Warning","Abort scan Progress!")
                            # Increase total scan count by 1
                            self.scanCount = self.scanCount + 1
                            # Update file name
                            self.fileName = unicode(QDate.currentDate().year()) \
                                            + unicode(format(QDate.currentDate().month(), '02d')) \
                                            + unicode(format(QDate.currentDate().day(), '02d')) \
                                            + "_" + unicode(format(self.scanCount, '03d')) \
                                            + "_Sample"
                            # Show file name
                            self.ui.FileName.setText(self.fileName)
                            # Set abort signal back to 0
                            self.abort = 0

                    print "Finished"
                    # Connect editingFinished event with event handlers
                    self.ui.minPixelValue.editingFinished.connect(self.minPixelValue_EditingFinished)
                    self.ui.maxPixelValue.editingFinished.connect(self.maxPixelValue_EditingFinished)

                    # Set selected_VL back to 0
                    self.selected_VL = 0
                    # Remove selectedRectItem_VL
                    self.scene_VL.removeItem(self.selectedRectItem_VL)
                    # Close HDF5 file
                    self.testFile.close()
                    self.hdf5File.close()
                    
                # If ROI is in scene_XR
                if self.selected_XR == 1:
                    # Calculate TimeLeft
                    self.timeLeft = self.width_XR * self.height_XR / (self.dwellTime * 1000)
                    # Show TimeLeft
                    self.ui.TimeLeft.setText(unicode(self.timeLeft)+"s")

                    # Do something # 
                    
                    # Set selected_XR back to 0
                    self.selected_XR = 0
                    # Remove selectedRectItem_XR
                    self.scene_XR.removeItem(self.selectedRectItem_XR)
                
                # Increase total scan count by 1
                self.scanCount = self.scanCount + 1
                # Update file name
                self.fileName = unicode(QDate.currentDate().year()) \
                                + unicode(format(QDate.currentDate().month(), '02d')) \
                                + unicode(format(QDate.currentDate().day(), '02d')) \
                                + "_" + unicode(format(self.scanCount, '03d')) \
                                + "_Sample"
                # Show file name
                self.ui.FileName.setText(self.fileName)
    
    '''
    "MoveToStartPoint clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_MoveToStartPoint_clicked(self, checked=None):
        # Check if ROI has been selected
        if (self.selected_VL == 1 or self.selected_XR == 1):
            # Update xPos & yPos
            self.xPos = int(self.ui.TopLeftX.text())
            self.yPos = int(self.ui.TopLeftY.text())
            # Move motor1
            self.motor1.put('VAL',self.xPos)
            while (self.motor1.get('RBV') != self.xPos):
                time.sleep(0.001)
                self.ui.MotorPositionX.setText(unicode(self.motor1.get('RBV')))
                self.ui.MotorPositionX.repaint()
            # Move motor2
            self.motor2.put('VAL',self.yPos)
            while (self.motor2.get('RBV') != self.yPos):
                time.sleep(0.001)
                self.ui.MotorPositionY.setText(unicode(self.motor2.get('RBV')))
                self.ui.MotorPositionY.repaint()
        else:
            print "Please select ROI first!"
            QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
    
    '''
    Plot in scene_Plot
    '''
    def paintPlot(self):
        # Set the size of figure
        self.figure = plt.Figure(figsize=(5.5,2.0),dpi=100, facecolor='w')
        self.canvas = FigureCanvas(self.figure)
        # Add canvas into scene_Plot
        self.scene_Plot.addWidget(self.canvas)
        # Add subplot (Only 1 subplot in this case)
        self.axes = self.figure.add_subplot(111)
        # If Energy is checked
        if (self.ui.Energy.isChecked()):
            self.axes.plot(self.energy,
                           self.plotData,
                           linestyle = 'solid',
                           marker = '',
                           color = 'green',
                           #label = 'XANES'
                           )
        # If Channel is checked
        elif (self.ui.Channel.isChecked()):
            self.axes.plot(self.plotData,
                           linestyle = 'solid',
                           marker = '',
                           color = 'green',
                           #label = 'XANES'
                           )
        # Show grid
        self.axes.grid('on')
        '''
        # self.axes.legend()
        # self.axes.set_xlim(1,2100)
        # self.axes.set_xticks([500,1000])
        # self.axes.set_ylim(0,190000)
        # self.axes.set_yticks([5000,50000,150000])
        '''
        # Show title
        self.axes.set_title('SRX',size = 10)
        '''
        self.axes.annotate('Energy (eV)', xy=(0, 0.8),
                         xycoords='axes points',
                         horizontalalignment='right',
                         verticalalignment='bottom',
                         fontsize=10)
        self.axes.annotate('Normalized ut',xy=(19.8,21.2),
                       xycoords='axes points',
                       horizontalalignment='left',
                       verticalalignment='bottom',
                       fontsize=10)
        '''
        # Draw canvas
        self.canvas.draw()
    
    '''
    "MOdifyElement clicked" event handler
    '''
    def on_ModifyElement_clicked(self, checked=None):
        if checked==None:return
        # Get result from PeriodicTable
        (tempElementsStatus,ok) = PeriodicTable.updateElementsStatus(self.currentElementsStatus)
        # Check if OK is clicked
        if ok == True:
            # Update currentElementsStatus
            self.currentElementsStatus = deepcopy(tempElementsStatus)
            # Set tableWidget to empty
            self.ui.tableWidget.setRowCount(0)
            # number of lines in tableWidget
            self.LineCount = 0
            
            for index in range(len(self.knownElements)):
                # currentElementsStatus[] = 1 means being selected
                if self.currentElementsStatus[index] == 1:
                    # index == 0 means Li, index == 1 means Be, etc.
                    if index == 0:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Li = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Li.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Li.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Li.currentIndexChanged['QString'].connect(self.comboBox_Li_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Li)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 1:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Be = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Be.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Be.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Be.currentIndexChanged['QString'].connect(self.comboBox_Be_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Be)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 2:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_B = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_B.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_B.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_B.currentIndexChanged['QString'].connect(self.comboBox_B_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_B)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 3:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_C = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_C.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_C.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_C.currentIndexChanged['QString'].connect(self.comboBox_C_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_C)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 4:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_N = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_N.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_N.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_N.currentIndexChanged['QString'].connect(self.comboBox_N_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_N)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 5:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_O = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_O.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_O.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_O.currentIndexChanged['QString'].connect(self.comboBox_O_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_O)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 6:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_F = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_F.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_F.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_F.currentIndexChanged['QString'].connect(self.comboBox_F_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_F)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 7:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ne = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ne.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ne.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ne.currentIndexChanged['QString'].connect(self.comboBox_Ne_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ne)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 8:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Na = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Na.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Na.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Na.currentIndexChanged['QString'].connect(self.comboBox_Na_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Na)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 9:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Mg = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Mg.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Mg.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Mg.currentIndexChanged['QString'].connect(self.comboBox_Mg_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Mg)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 10:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Al = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Al.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Al.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Al.currentIndexChanged['QString'].connect(self.comboBox_Al_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Al)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 11:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Si = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Si.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Si.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Si.currentIndexChanged['QString'].connect(self.comboBox_Si_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Si)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 12:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_P = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_P.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_P.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_P.currentIndexChanged['QString'].connect(self.comboBox_P_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_P)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 13:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_S = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_S.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_S.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_S.currentIndexChanged['QString'].connect(self.comboBox_S_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_S)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 14:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Cl = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Cl.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Cl.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Cl.currentIndexChanged['QString'].connect(self.comboBox_Cl_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Cl)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 15:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ar = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ar.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Ar.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ar.currentIndexChanged['QString'].connect(self.comboBox_Ar_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ar)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 16:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_K = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_K.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_K.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_K.currentIndexChanged['QString'].connect(self.comboBox_K_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_K)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 17:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ca = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ca.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Ca.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ca.currentIndexChanged['QString'].connect(self.comboBox_Ca_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ca)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 18:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Sc = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Sc.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Sc.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Sc.currentIndexChanged['QString'].connect(self.comboBox_Sc_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Sc)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 19:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ti = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ti.insertItem(temp,
                                                            self.energyLabel[i] + \
                                                            QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                            "eV")
                                temp = temp + 1
                        self.comboBox_Ti.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ti.currentIndexChanged['QString'].connect(self.comboBox_Ti_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ti)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 20:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_V = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_V.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_V.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_V.currentIndexChanged['QString'].connect(self.comboBox_V_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_V)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 21:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Cr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Cr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Cr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Cr.currentIndexChanged['QString'].connect(self.comboBox_Cr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Cr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 22:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Mn = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Mn.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Mn.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Mn.currentIndexChanged['QString'].connect(self.comboBox_Mn_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Mn)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 23:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Fe = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Fe.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Fe.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Fe.currentIndexChanged['QString'].connect(self.comboBox_Fe_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Fe)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 24:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Co = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Co.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Co.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Co.currentIndexChanged['QString'].connect(self.comboBox_Co_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Co)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 25:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ni = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ni.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ni.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ni.currentIndexChanged['QString'].connect(self.comboBox_Ni_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ni)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 26:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Cu = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Cu.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Cu.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Cu.currentIndexChanged['QString'].connect(self.comboBox_Cu_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Cu)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 27:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Zn = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Zn.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Zn.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Zn.currentIndexChanged['QString'].connect(self.comboBox_Zn_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Zn)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 28:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ga = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ga.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ga.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ga.currentIndexChanged['QString'].connect(self.comboBox_Ga_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ga)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 29:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ge = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ge.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ge.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ge.currentIndexChanged['QString'].connect(self.comboBox_Ge_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ge)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 30:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_As = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_As.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_As.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_As.currentIndexChanged['QString'].connect(self.comboBox_As_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_As)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 31:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Se = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Se.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Se.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Se.currentIndexChanged['QString'].connect(self.comboBox_Se_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Se)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 32:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Br = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Br.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Br.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Br.currentIndexChanged['QString'].connect(self.comboBox_Br_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Br)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 33:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Kr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Kr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Kr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Kr.currentIndexChanged['QString'].connect(self.comboBox_Kr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Kr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 34:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Rb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Rb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Rb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Rb.currentIndexChanged['QString'].connect(self.comboBox_Rb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Rb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 35:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Sr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Sr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Sr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Sr.currentIndexChanged['QString'].connect(self.comboBox_Sr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Sr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 36:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Y = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Y.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Y.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Y.currentIndexChanged['QString'].connect(self.comboBox_Y_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Y)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 37:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Zr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Zr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Zr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Zr.currentIndexChanged['QString'].connect(self.comboBox_Zr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Zr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 38:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Nb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Nb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Nb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Nb.currentIndexChanged['QString'].connect(self.comboBox_Nb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Nb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 39:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Mo = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Mo.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Mo.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Mo.currentIndexChanged['QString'].connect(self.comboBox_Mo_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Mo)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1   
                    elif index == 40:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Tc = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Tc.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Tc.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Tc.currentIndexChanged['QString'].connect(self.comboBox_Tc_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Tc)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 41:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ru = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ru.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ru.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ru.currentIndexChanged['QString'].connect(self.comboBox_Ru_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ru)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 42:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Rh = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Rh.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Rh.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Rh.currentIndexChanged['QString'].connect(self.comboBox_Rh_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Rh)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 43:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pd = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pd.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pd.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pd.currentIndexChanged['QString'].connect(self.comboBox_Pd_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pd)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 44:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ag = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ag.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ag.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ag.currentIndexChanged['QString'].connect(self.comboBox_Ag_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ag)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 45:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Cd = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Cd.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Cd.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Cd.currentIndexChanged['QString'].connect(self.comboBox_Cd_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Cd)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 46:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_In = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_In.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_In.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_In.currentIndexChanged['QString'].connect(self.comboBox_In_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_In)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 47:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Sn = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Sn.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Sn.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Sn.currentIndexChanged['QString'].connect(self.comboBox_Sn_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Sn)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 48:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Sb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Sb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Sb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Sb.currentIndexChanged['QString'].connect(self.comboBox_Sb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Sb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 49:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Te = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Te.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Te.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Te.currentIndexChanged['QString'].connect(self.comboBox_Te_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Te)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1     
                    elif index == 50:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_I = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_I.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_I.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_I.currentIndexChanged['QString'].connect(self.comboBox_I_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_I)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 51:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Xe = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Xe.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Xe.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Xe.currentIndexChanged['QString'].connect(self.comboBox_Xe_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Xe)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 52:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Cs = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Cs.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Cs.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Cs.currentIndexChanged['QString'].connect(self.comboBox_Cs_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Cs)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 53:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ba = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ba.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ba.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ba.currentIndexChanged['QString'].connect(self.comboBox_Ba_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ba)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 54:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Hf = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Hf.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Hf.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Hf.currentIndexChanged['QString'].connect(self.comboBox_Hf_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Hf)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 55:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ta = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ta.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ta.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ta.currentIndexChanged['QString'].connect(self.comboBox_Ta_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ta)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 56:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_W = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_W.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_W.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_W.currentIndexChanged['QString'].connect(self.comboBox_W_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_W)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 57:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Re = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Re.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Re.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Re.currentIndexChanged['QString'].connect(self.comboBox_Re_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Re)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 58:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Os = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Os.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Os.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Os.currentIndexChanged['QString'].connect(self.comboBox_Os_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Os)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 59:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ir = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ir.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ir.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ir.currentIndexChanged['QString'].connect(self.comboBox_Ir_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ir)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1                        
                    elif index == 60:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pt = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pt.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pt.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pt.currentIndexChanged['QString'].connect(self.comboBox_Pt_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pt)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 61:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Au = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Au.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Au.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Au.currentIndexChanged['QString'].connect(self.comboBox_Au_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Au)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 62:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Hg = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Hg.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Hg.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Hg.currentIndexChanged['QString'].connect(self.comboBox_Hg_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Hg)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 63:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Tl = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Tl.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Tl.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Tl.currentIndexChanged['QString'].connect(self.comboBox_Tl_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Tl)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 64:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pb.currentIndexChanged['QString'].connect(self.comboBox_Pb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 65:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Bi = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Bi.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Bi.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Bi.currentIndexChanged['QString'].connect(self.comboBox_Bi_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Bi)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 66:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Po = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Po.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Po.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Po.currentIndexChanged['QString'].connect(self.comboBox_Po_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Po)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 67:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_At = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_At.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_At.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_At.currentIndexChanged['QString'].connect(self.comboBox_At_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_At)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 68:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Rn = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Rn.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Rn.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Rn.currentIndexChanged['QString'].connect(self.comboBox_Rn_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Rn)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 69:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Fr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Fr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Fr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Fr.currentIndexChanged['QString'].connect(self.comboBox_Fr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Fr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1                        
                    elif index == 70:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ra = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ra.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ra.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ra.currentIndexChanged['QString'].connect(self.comboBox_Ra_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ra)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 71:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_La = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_La.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_La.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_La.currentIndexChanged['QString'].connect(self.comboBox_La_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_La)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 72:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ce = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ce.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ce.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ce.currentIndexChanged['QString'].connect(self.comboBox_Ce_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ce)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 73:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pr = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pr.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pr.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pr.currentIndexChanged['QString'].connect(self.comboBox_Pr_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pr)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 74:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Nd = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Nd.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Nd.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Nd.currentIndexChanged['QString'].connect(self.comboBox_Nd_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Nd)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 75:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pm = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pm.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pm.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pm.currentIndexChanged['QString'].connect(self.comboBox_Pm_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pm)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 76:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Sm = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Sm.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Sm.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Sm.currentIndexChanged['QString'].connect(self.comboBox_Sm_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Sm)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 77:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Eu = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Eu.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Eu.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Eu.currentIndexChanged['QString'].connect(self.comboBox_Eu_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Eu)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 78:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Gd = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Gd.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Gd.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Gd.currentIndexChanged['QString'].connect(self.comboBox_Gd_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Gd)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 79:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Tb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Tb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Tb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Tb.currentIndexChanged['QString'].connect(self.comboBox_Tb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Tb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1                        
                    elif index == 80:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Dy = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Dy.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Dy.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Dy.currentIndexChanged['QString'].connect(self.comboBox_Dy_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Dy)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 81:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ho = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ho.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ho.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ho.currentIndexChanged['QString'].connect(self.comboBox_Ho_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ho)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 82:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Er = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Er.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Er.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Er.currentIndexChanged['QString'].connect(self.comboBox_Er_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Er)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 83:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Tm = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Tm.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Tm.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Tm.currentIndexChanged['QString'].connect(self.comboBox_Tm_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Tm)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 84:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Yb = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Yb.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Yb.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Yb.currentIndexChanged['QString'].connect(self.comboBox_Yb_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Yb)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 85:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Lu = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Lu.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Lu.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Lu.currentIndexChanged['QString'].connect(self.comboBox_Lu_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Lu)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 86:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Ac = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Ac.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Ac.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Ac.currentIndexChanged['QString'].connect(self.comboBox_Ac_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Ac)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 87:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Th = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Th.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Th.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Th.currentIndexChanged['QString'].connect(self.comboBox_Th_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Th)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 88:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pa = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pa.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pa.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pa.currentIndexChanged['QString'].connect(self.comboBox_Pa_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pa)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 89:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_U = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_U.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_U.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_U.currentIndexChanged['QString'].connect(self.comboBox_U_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_U)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1                        
                    elif index == 90:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Np = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Np.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Np.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Np.currentIndexChanged['QString'].connect(self.comboBox_Np_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Np)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 91:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Pu = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Pu.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Pu.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Pu.currentIndexChanged['QString'].connect(self.comboBox_Pu_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Pu)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
                    elif index == 92:
                        # Add a new line in tableWidget
                        self.ui.tableWidget.insertRow(self.LineCount)
                        # Create comboBox
                        self.comboBox_Am = QtGui.QComboBox()
                        temp = 0
                        # Insert items to comboBox
                        for i in range(len(self.PhotonEnergy[0])):
                            if (self.modifiedPhotonEnergy[index][i] != 0):
                                self.comboBox_Am.insertItem(temp,
                                                           self.energyLabel[i] + \
                                                           QString(unicode(self.modifiedPhotonEnergy[index][i])) + \
                                                           "eV")
                                temp = temp + 1
                        self.comboBox_Am.insertItem(temp,"All")
                        # Connect "comboBox changed" event handler
                        self.comboBox_Am.currentIndexChanged['QString'].connect(self.comboBox_Am_Changed)
                        # Show element symbol in talbeWidget
                        self.ui.tableWidget.setItem(self.LineCount,0,
                                                    QTableWidgetItem(QString(self.knownElements[index])))
                        # Show comboBox in tableWidget
                        self.ui.tableWidget.setCellWidget(self.LineCount,1,self.comboBox_Am)
                        # Show scanEnergyRange in tableWidget
                        self.ui.tableWidget.setItem(self.LineCount,2,
                                                    QTableWidgetItem(QString(unicode(self.scanEnergyRange[index]))))
                        self.LineCount = self.LineCount + 1
    '''
    "comboBox_Li changed" event handler
    '''
    def comboBox_Li_Changed(self,event):
        print "Li:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[0][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[0][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Li.currentIndex() == temp:
            self.scanEnergyLevel[0] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[0] = level[self.comboBox_Li.currentIndex()]
        
        print self.scanEnergyLevel[0]
    '''
    "comboBox_Be changed" event handler
    '''
    def comboBox_Be_Changed(self,event):
        print "Be:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[1][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[1][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Be.currentIndex() == temp:
            self.scanEnergyLevel[1] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[1] = level[self.comboBox_Be.currentIndex()]
        
        print self.scanEnergyLevel[1]
    '''
    "comboBox_B changed" event handler
    '''
    def comboBox_B_Changed(self,event):
        print "B:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[2][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[2][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_B.currentIndex() == temp:
            self.scanEnergyLevel[2] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[2] = level[self.comboBox_B.currentIndex()]
        
        print self.scanEnergyLevel[2]
    '''
    "comboBox_C changed" event handler
    '''
    def comboBox_C_Changed(self,event):
        print "C:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[3][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[3][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_C.currentIndex() == temp:
            self.scanEnergyLevel[3] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[3] = level[self.comboBox_C.currentIndex()]
        
        print self.scanEnergyLevel[3]
    '''
    "comboBox_N changed" event handler
    '''
    def comboBox_N_Changed(self,event):
        print "N:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[4][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[4][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_N.currentIndex() == temp:
            self.scanEnergyLevel[4] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[4] = level[self.comboBox_N.currentIndex()]
        
        print self.scanEnergyLevel[4]
    '''
    "comboBox_O changed" event handler
    '''
    def comboBox_O_Changed(self,event):
        print "O:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[5][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[5][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_O.currentIndex() == temp:
            self.scanEnergyLevel[5] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[5] = level[self.comboBox_O.currentIndex()]
        
        print self.scanEnergyLevel[5]
    '''
    "comboBox_F changed" event handler
    '''
    def comboBox_F_Changed(self,event):
        print "F:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[6][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[6][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_F.currentIndex() == temp:
            self.scanEnergyLevel[6] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[6] = level[self.comboBox_F.currentIndex()]
        
        print self.scanEnergyLevel[6]
    '''
    "comboBox_Ne changed" event handler
    '''
    def comboBox_Ne_Changed(self,event):
        print "Ne:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[7][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[7][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ne.currentIndex() == temp:
            self.scanEnergyLevel[7] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[7] = level[self.comboBox_Ne.currentIndex()]
        
        print self.scanEnergyLevel[7]
    '''
    "comboBox_Na changed" event handler
    '''
    def comboBox_Na_Changed(self,event):
        print "Na:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[8][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[8][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Na.currentIndex() == temp:
            self.scanEnergyLevel[8] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[8] = level[self.comboBox_Na.currentIndex()]
        
        print self.scanEnergyLevel[8]
    '''
    "comboBox_Mg changed" event handler
    '''
    def comboBox_Mg_Changed(self,event):
        print "Mg:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[9][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[9][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Mg.currentIndex() == temp:
            self.scanEnergyLevel[9] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[9] = level[self.comboBox_Mg.currentIndex()]
        
        print self.scanEnergyLevel[9]
    '''
    "comboBox_Al changed" event handler
    '''
    def comboBox_Al_Changed(self,event):
        print "B:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[10][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[10][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Al.currentIndex() == temp:
            self.scanEnergyLevel[10] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[10] = level[self.comboBox_Al.currentIndex()]
        
        print self.scanEnergyLevel[10]
    '''
    "comboBox_Si changed" event handler
    '''
    def comboBox_Si_Changed(self,event):
        print "Si:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[11][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[11][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Si.currentIndex() == temp:
            self.scanEnergyLevel[11] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[11] = level[self.comboBox_Si.currentIndex()]
        
        print self.scanEnergyLevel[11]
    '''
    "comboBox_P changed" event handler
    '''
    def comboBox_P_Changed(self,event):
        print "P:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[12][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[12][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_P.currentIndex() == temp:
            self.scanEnergyLevel[12] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[12] = level[self.comboBox_P.currentIndex()]
        
        print self.scanEnergyLevel[12]
    '''
    "comboBox_S changed" event handler
    '''
    def comboBox_S_Changed(self,event):
        print "S:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[13][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[13][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_S.currentIndex() == temp:
            self.scanEnergyLevel[13] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[13] = level[self.comboBox_S.currentIndex()]
        
        print self.scanEnergyLevel[13]
    '''
    "comboBox_Cl changed" event handler
    '''
    def comboBox_Cl_Changed(self,event):
        print "Cl:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[14][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[14][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Cl.currentIndex() == temp:
            self.scanEnergyLevel[14] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[14] = level[self.comboBox_Cl.currentIndex()]
        
        print self.scanEnergyLevel[14]
    '''
    "comboBox_Ar changed" event handler
    '''
    def comboBox_Ar_Changed(self,event):
        print "Ar:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[15][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[15][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ar.currentIndex() == temp:
            self.scanEnergyLevel[15] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[15] = level[self.comboBox_Ar.currentIndex()]
        
        print self.scanEnergyLevel[15]
    '''
    "comboBox_K changed" event handler
    '''
    def comboBox_K_Changed(self,event):
        print "K:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[16][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[16][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_K.currentIndex() == temp:
            self.scanEnergyLevel[16] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[16] = level[self.comboBox_K.currentIndex()]
        
        print self.scanEnergyLevel[16]
    '''
    "comboBox_Ca changed" event handler
    '''
    def comboBox_Ca_Changed(self,event):
        print "Ca:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[17][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[17][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ca.currentIndex() == temp:
            self.scanEnergyLevel[17] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[17] = level[self.comboBox_Ca.currentIndex()]
        
        print self.scanEnergyLevel[17]
    '''
    "comboBox_Sc changed" event handler
    '''
    def comboBox_Sc_Changed(self,event):
        print "Sc:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[18][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[18][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Sc.currentIndex() == temp:
            self.scanEnergyLevel[18] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[18] = level[self.comboBox_Sc.currentIndex()]
        
        print self.scanEnergyLevel[18]
    '''
    "comboBox_Ti changed" event handler
    '''
    def comboBox_Ti_Changed(self,event):
        print "Ti:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[19][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[19][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ti.currentIndex() == temp:
            self.scanEnergyLevel[19] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[19] = level[self.comboBox_Ti.currentIndex()]
        
        print self.scanEnergyLevel[19]
    '''
    "comboBox_V changed" event handler
    '''
    def comboBox_V_Changed(self,event):
        print "V:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[20][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[20][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_V.currentIndex() == temp:
            self.scanEnergyLevel[20] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[20] = level[self.comboBox_V.currentIndex()]
        
        print self.scanEnergyLevel[20]
    '''
    "comboBox_Cr changed" event handler
    '''
    def comboBox_Cr_Changed(self,event):
        print "Cr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[21][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[21][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Cr.currentIndex() == temp:
            self.scanEnergyLevel[21] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[21] = level[self.comboBox_Cr.currentIndex()]
        
        print self.scanEnergyLevel[21]
    '''
    "comboBox_Mn changed" event handler
    '''
    def comboBox_Mn_Changed(self,event):
        print "Mn:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[22][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[22][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Mn.currentIndex() == temp:
            self.scanEnergyLevel[22] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[22] = level[self.comboBox_Mn.currentIndex()]
        
        print self.scanEnergyLevel[22]
    '''
    "comboBox_Fe changed" event handler
    '''
    def comboBox_Fe_Changed(self,event):
        print "Fe:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[23][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[23][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Fe.currentIndex() == temp:
            self.scanEnergyLevel[23] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[23] = level[self.comboBox_Fe.currentIndex()]
        
        print self.scanEnergyLevel[23]
    '''
    "comboBox_Co changed" event handler
    '''
    def comboBox_Co_Changed(self,event):
        print "Co:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[24][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[24][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Co.currentIndex() == temp:
            self.scanEnergyLevel[24] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[24] = level[self.comboBox_Co.currentIndex()]
        
        print self.scanEnergyLevel[24]
    '''
    "comboBox_Ni changed" event handler
    '''
    def comboBox_Ni_Changed(self,event):
        print "Ni:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[25][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[25][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ni.currentIndex() == temp:
            self.scanEnergyLevel[25] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[25] = level[self.comboBox_Ni.currentIndex()]
        
        print self.scanEnergyLevel[25]
    '''
    "comboBox_Cu changed" event handler
    '''
    def comboBox_Cu_Changed(self,event):
        print "Cu:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[26][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[26][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Cu.currentIndex() == temp:
            self.scanEnergyLevel[26] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[26] = level[self.comboBox_Cu.currentIndex()]
        
        print self.scanEnergyLevel[26]
    '''
    "comboBox_Zn changed" event handler
    '''
    def comboBox_Zn_Changed(self,event):
        print "Zn:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[27][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[27][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Zn.currentIndex() == temp:
            self.scanEnergyLevel[27] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[27] = level[self.comboBox_Zn.currentIndex()]
        
        print self.scanEnergyLevel[27]
    '''
    "comboBox_Ga changed" event handler
    '''
    def comboBox_Ga_Changed(self,event):
        print "Ga:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[28][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[28][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ga.currentIndex() == temp:
            self.scanEnergyLevel[28] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[28] = level[self.comboBox_Ga.currentIndex()]
        
        print self.scanEnergyLevel[28]
    '''
    "comboBox_Ge changed" event handler
    '''
    def comboBox_Ge_Changed(self,event):
        print "Ge:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[29][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[29][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ge.currentIndex() == temp:
            self.scanEnergyLevel[29] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[29] = level[self.comboBox_Ge.currentIndex()]
        
        print self.scanEnergyLevel[29]
    '''
    "comboBox_As changed" event handler
    '''
    def comboBox_As_Changed(self,event):
        print "As:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[30][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[30][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_As.currentIndex() == temp:
            self.scanEnergyLevel[30] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[30] = level[self.comboBox_As.currentIndex()]
        
        print self.scanEnergyLevel[30]
    '''
    "comboBox_Se changed" event handler
    '''
    def comboBox_Se_Changed(self,event):
        print "Se:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[31][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[31][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Se.currentIndex() == temp:
            self.scanEnergyLevel[31] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[31] = level[self.comboBox_Se.currentIndex()]
        
        print self.scanEnergyLevel[31]
    '''
    "comboBox_Br changed" event handler
    '''
    def comboBox_Br_Changed(self,event):
        print "Br:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[32][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[32][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Br.currentIndex() == temp:
            self.scanEnergyLevel[32] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[32] = level[self.comboBox_Br.currentIndex()]
        
        print self.scanEnergyLevel[32]
    '''
    "comboBox_Kr changed" event handler
    '''
    def comboBox_Kr_Changed(self,event):
        print "Kr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[33][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[33][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Kr.currentIndex() == temp:
            self.scanEnergyLevel[33] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[33] = level[self.comboBox_Kr.currentIndex()]
        
        print self.scanEnergyLevel[33]
    '''
    "comboBox_Rb changed" event handler
    '''
    def comboBox_Rb_Changed(self,event):
        print "Rb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[34][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[34][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Rb.currentIndex() == temp:
            self.scanEnergyLevel[34] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[34] = level[self.comboBox_Rb.currentIndex()]
        
        print self.scanEnergyLevel[34]
    '''
    "comboBox_Sr changed" event handler
    '''
    def comboBox_Sr_Changed(self,event):
        print "Sr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[35][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[35][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Sr.currentIndex() == temp:
            self.scanEnergyLevel[35] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[35] = level[self.comboBox_Sr.currentIndex()]
        
        print self.scanEnergyLevel[35]
    '''
    "comboBox_Y changed" event handler
    '''
    def comboBox_Y_Changed(self,event):
        print "Y:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[36][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[36][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Y.currentIndex() == temp:
            self.scanEnergyLevel[36] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[36] = level[self.comboBox_Y.currentIndex()]
        
        print self.scanEnergyLevel[36]
    '''
    "comboBox_Zr changed" event handler
    '''
    def comboBox_Zr_Changed(self,event):
        print "Zr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[37][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[37][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Zr.currentIndex() == temp:
            self.scanEnergyLevel[37] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[37] = level[self.comboBox_Zr.currentIndex()]
        
        print self.scanEnergyLevel[37]
    '''
    "comboBox_Nb changed" event handler
    '''
    def comboBox_Nb_Changed(self,event):
        print "Nb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[38][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[38][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Nb.currentIndex() == temp:
            self.scanEnergyLevel[38] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[38] = level[self.comboBox_Nb.currentIndex()]
        
        print self.scanEnergyLevel[38]
    '''
    "comboBox_Mo changed" event handler
    '''
    def comboBox_Mo_Changed(self,event):
        print "Mo:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[39][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[39][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Mo.currentIndex() == temp:
            self.scanEnergyLevel[39] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[39] = level[self.comboBox_Mo.currentIndex()]
        
        print self.scanEnergyLevel[39]
    '''
    "comboBox_Tc changed" event handler
    '''
    def comboBox_Tc_Changed(self,event):
        print "Tc:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[40][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[40][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Tc.currentIndex() == temp:
            self.scanEnergyLevel[40] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[40] = level[self.comboBox_Tc.currentIndex()]
        
        print self.scanEnergyLevel[40]
    '''
    "comboBox_Ru changed" event handler
    '''
    def comboBox_Ru_Changed(self,event):
        print "Ru:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[41][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[41][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ru.currentIndex() == temp:
            self.scanEnergyLevel[41] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[41] = level[self.comboBox_Ru.currentIndex()]
        
        print self.scanEnergyLevel[41]
    '''
    "comboBox_Rh changed" event handler
    '''
    def comboBox_Rh_Changed(self,event):
        print "Rh:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[42][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[42][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Rh.currentIndex() == temp:
            self.scanEnergyLevel[42] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[42] = level[self.comboBox_Rh.currentIndex()]
        
        print self.scanEnergyLevel[42]
    '''
    "comboBox_Pd changed" event handler
    '''
    def comboBox_Pd_Changed(self,event):
        print "Pd:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[43][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[43][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pd.currentIndex() == temp:
            self.scanEnergyLevel[43] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[43] = level[self.comboBox_Pd.currentIndex()]
        
        print self.scanEnergyLevel[43]
    '''
    "comboBox_Ag changed" event handler
    '''
    def comboBox_Ag_Changed(self,event):
        print "Ag:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[44][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[44][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ag.currentIndex() == temp:
            self.scanEnergyLevel[44] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[44] = level[self.comboBox_Ag.currentIndex()]
        
        print self.scanEnergyLevel[44]
    '''
    "comboBox_Cd changed" event handler
    '''
    def comboBox_Cd_Changed(self,event):
        print "Cd:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[45][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[45][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Cd.currentIndex() == temp:
            self.scanEnergyLevel[45] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[45] = level[self.comboBox_Cd.currentIndex()]
        
        print self.scanEnergyLevel[45]
    '''
    "comboBox_In changed" event handler
    '''
    def comboBox_In_Changed(self,event):
        print "In:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[46][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[46][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_In.currentIndex() == temp:
            self.scanEnergyLevel[46] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[46] = level[self.comboBox_In.currentIndex()]
        
        print self.scanEnergyLevel[46]
    '''
    "comboBox_Sn changed" event handler
    '''
    def comboBox_Sn_Changed(self,event):
        print "Sn:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[47][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[47][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Sn.currentIndex() == temp:
            self.scanEnergyLevel[47] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[47] = level[self.comboBox_Sn.currentIndex()]
        
        print self.scanEnergyLevel[47]
    '''
    "comboBox_Sb changed" event handler
    '''
    def comboBox_Sb_Changed(self,event):
        print "Sb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[48][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[48][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Sb.currentIndex() == temp:
            self.scanEnergyLevel[48] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[48] = level[self.comboBox_Sb.currentIndex()]
        
        print self.scanEnergyLevel[48]
    '''
    "comboBox_Te changed" event handler
    '''
    def comboBox_Te_Changed(self,event):
        print "Te:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[49][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[49][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Te.currentIndex() == temp:
            self.scanEnergyLevel[49] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[49] = level[self.comboBox_Te.currentIndex()]
        
        print self.scanEnergyLevel[49]
    '''
    "comboBox_I changed" event handler
    '''
    def comboBox_I_Changed(self,event):
        print "I:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[50][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[50][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_I.currentIndex() == temp:
            self.scanEnergyLevel[50] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[50] = level[self.comboBox_I.currentIndex()]
        
        print self.scanEnergyLevel[50]
    '''
    "comboBox_Xe changed" event handler
    '''
    def comboBox_Xe_Changed(self,event):
        print "Xe:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[51][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[51][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Xe.currentIndex() == temp:
            self.scanEnergyLevel[51] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[51] = level[self.comboBox_Xe.currentIndex()]
        
        print self.scanEnergyLevel[51]
    '''
    "comboBox_Cs changed" event handler
    '''
    def comboBox_Cs_Changed(self,event):
        print "Cs:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[52][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[52][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Cs.currentIndex() == temp:
            self.scanEnergyLevel[52] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[52] = level[self.comboBox_Cs.currentIndex()]
        
        print self.scanEnergyLevel[52]
    '''
    "comboBox_Ba changed" event handler
    '''
    def comboBox_Ba_Changed(self,event):
        print "Ba:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[53][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[53][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ba.currentIndex() == temp:
            self.scanEnergyLevel[53] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[53] = level[self.comboBox_Ba.currentIndex()]
        
        print self.scanEnergyLevel[53]
    '''
    "comboBox_Hf changed" event handler
    '''
    def comboBox_Hf_Changed(self,event):
        print "Hf:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[54][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[54][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Hf.currentIndex() == temp:
            self.scanEnergyLevel[54] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[54] = level[self.comboBox_Hf.currentIndex()]
        
        print self.scanEnergyLevel[54]
    '''
    "comboBox_Ta changed" event handler
    '''
    def comboBox_Ta_Changed(self,event):
        print "Ta:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[55][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[55][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ta.currentIndex() == temp:
            self.scanEnergyLevel[55] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[55] = level[self.comboBox_Ta.currentIndex()]
        
        print self.scanEnergyLevel[55]
    '''
    "comboBox_W changed" event handler
    '''
    def comboBox_W_Changed(self,event):
        print "W:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[56][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[56][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_W.currentIndex() == temp:
            self.scanEnergyLevel[56] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[56] = level[self.comboBox_W.currentIndex()]
        
        print self.scanEnergyLevel[56]
    '''
    "comboBox_Re changed" event handler
    '''
    def comboBox_Re_Changed(self,event):
        print "Re:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[57][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[57][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Re.currentIndex() == temp:
            self.scanEnergyLevel[57] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[57] = level[self.comboBox_Re.currentIndex()]
        
        print self.scanEnergyLevel[57]
    '''
    "comboBox_Os changed" event handler
    '''
    def comboBox_Os_Changed(self,event):
        print "Os:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[58][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[58][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Os.currentIndex() == temp:
            self.scanEnergyLevel[58] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[58] = level[self.comboBox_Os.currentIndex()]
        
        print self.scanEnergyLevel[58]
    '''
    "comboBox_Ir changed" event handler
    '''
    def comboBox_Ir_Changed(self,event):
        print "Ir:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[59][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[59][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ir.currentIndex() == temp:
            self.scanEnergyLevel[59] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[59] = level[self.comboBox_Ir.currentIndex()]
        
        print self.scanEnergyLevel[59]
    '''
    "comboBox_Pt changed" event handler
    '''
    def comboBox_Pt_Changed(self,event):
        print "Pt:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[60][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[60][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pt.currentIndex() == temp:
            self.scanEnergyLevel[60] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[60] = level[self.comboBox_Pt.currentIndex()]
        
        print self.scanEnergyLevel[60]
    '''
    "comboBox_Au changed" event handler
    '''
    def comboBox_Au_Changed(self,event):
        print "Au:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[61][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[61][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Au.currentIndex() == temp:
            self.scanEnergyLevel[61] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[61] = level[self.comboBox_Au.currentIndex()]
        
        print self.scanEnergyLevel[61]
    '''
    "comboBox_Hg changed" event handler
    '''
    def comboBox_Hg_Changed(self,event):
        print "Hg:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[62][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[62][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Hg.currentIndex() == temp:
            self.scanEnergyLevel[62] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[62] = level[self.comboBox_Hg.currentIndex()]
        
        print self.scanEnergyLevel[62]
    '''
    "comboBox_Tl changed" event handler
    '''
    def comboBox_Tl_Changed(self,event):
        print "Tl:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[63][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[63][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Tl.currentIndex() == temp:
            self.scanEnergyLevel[63] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[63] = level[self.comboBox_Tl.currentIndex()]
        
        print self.scanEnergyLevel[63]
    '''
    "comboBox_Pb changed" event handler
    '''
    def comboBox_Pb_Changed(self,event):
        print "Pb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[64][i] != 0):
                level[temp] = self.modifiedPhtonEnergy[64][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pb.currentIndex() == temp:
            self.scanEnergyLevel[64] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[64] = level[self.comboBox_Pb.currentIndex()]
        
        print self.scanEnergyLevel[64]
    '''
    "comboBox_Bi changed" event handler
    '''
    def comboBox_Bi_Changed(self,event):
        print "Bi:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[65][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[65][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Bi.currentIndex() == temp:
            self.scanEnergyLevel[65] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[65] = level[self.comboBox_Bi.currentIndex()]
        
        print self.scanEnergyLevel[65]
    '''
    "comboBox_Po changed" event handler
    '''
    def comboBox_Po_Changed(self,event):
        print "Po:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[66][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[66][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Po.currentIndex() == temp:
            self.scanEnergyLevel[66] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[66] = level[self.comboBox_Po.currentIndex()]
        
        print self.scanEnergyLevel[66]
    '''
    "comboBox_At changed" event handler
    '''
    def comboBox_At_Changed(self,event):
        print "At:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[67][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[67][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_At.currentIndex() == temp:
            self.scanEnergyLevel[67] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[67] = level[self.comboBox_At.currentIndex()]
        
        print self.scanEnergyLevel[67]
    '''
    "comboBox_Rn changed" event handler
    '''
    def comboBox_Rn_Changed(self,event):
        print "Rn:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[68][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[68][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Rn.currentIndex() == temp:
            self.scanEnergyLevel[68] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[68] = level[self.comboBox_Rn.currentIndex()]
        
        print self.scanEnergyLevel[68]
    '''
    "comboBox_Fr changed" event handler
    '''
    def comboBox_Fr_Changed(self,event):
        print "Fr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[69][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[69][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Fr.currentIndex() == temp:
            self.scanEnergyLevel[69] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[69] = level[self.comboBox_Fr.currentIndex()]
        
        print self.scanEnergyLevel[69]
    '''
    "comboBox_Ra changed" event handler
    '''
    def comboBox_Ra_Changed(self,event):
        print "Ra:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[70][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[70][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ra.currentIndex() == temp:
            self.scanEnergyLevel[70] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[70] = level[self.comboBox_Ra.currentIndex()]
        
        print self.scanEnergyLevel[70]
    '''
    "comboBox_La changed" event handler
    '''
    def comboBox_La_Changed(self,event):
        print "La:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[71][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[71][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_La.currentIndex() == temp:
            self.scanEnergyLevel[71] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[71] = level[self.comboBox_La.currentIndex()]
        
        print self.scanEnergyLevel[71]
    '''
    "comboBox_Ce changed" event handler
    '''
    def comboBox_Ce_Changed(self,event):
        print "Ce:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[72][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[72][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ce.currentIndex() == temp:
            self.scanEnergyLevel[72] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[72] = level[self.comboBox_Ce.currentIndex()]
        
        print self.scanEnergyLevel[72]
    '''
    "comboBox_Pr changed" event handler
    '''
    def comboBox_Pr_Changed(self,event):
        print "Pr:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[73][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[73][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pr.currentIndex() == temp:
            self.scanEnergyLevel[73] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[73] = level[self.comboBox_Pr.currentIndex()]
        
        print self.scanEnergyLevel[73]
    '''
    "comboBox_Nd changed" event handler
    '''
    def comboBox_Nd_Changed(self,event):
        print "Nd:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[74][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[74][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Nd.currentIndex() == temp:
            self.scanEnergyLevel[74] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[74] = level[self.comboBox_Nd.currentIndex()]
        
        print self.scanEnergyLevel[74]
    '''
    "comboBox_Pm changed" event handler
    '''
    def comboBox_Pm_Changed(self,event):
        print "Pm:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[75][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[75][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pm.currentIndex() == temp:
            self.scanEnergyLevel[75] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[75] = level[self.comboBox_Pm.currentIndex()]
        
        print self.scanEnergyLevel[75]
    '''
    "comboBox_Sm changed" event handler
    '''
    def comboBox_Sm_Changed(self,event):
        print "Sm:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[76][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[76][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Sm.currentIndex() == temp:
            self.scanEnergyLevel[76] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[76] = level[self.comboBox_Sm.currentIndex()]
        
        print self.scanEnergyLevel[76]
    '''
    "comboBox_Eu changed" event handler
    '''
    def comboBox_Eu_Changed(self,event):
        print "Eu:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[77][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[77][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Eu.currentIndex() == temp:
            self.scanEnergyLevel[77] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[77] = level[self.comboBox_Eu.currentIndex()]
        
        print self.scanEnergyLevel[77]
    '''
    "comboBox_Gd changed" event handler
    '''
    def comboBox_Gd_Changed(self,event):
        print "Gd:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[78][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[78][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Gd.currentIndex() == temp:
            self.scanEnergyLevel[78] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[78] = level[self.comboBox_Gd.currentIndex()]
        
        print self.scanEnergyLevel[78]
    '''
    "comboBox_Tb changed" event handler
    '''
    def comboBox_Tb_Changed(self,event):
        print "Tb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[79][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[79][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Tb.currentIndex() == temp:
            self.scanEnergyLevel[79] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[79] = level[self.comboBox_Tb.currentIndex()]
        
        print self.scanEnergyLevel[79]
    '''
    "comboBox_Dy changed" event handler
    '''
    def comboBox_Dy_Changed(self,event):
        print "Dy:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[80][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[80][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Dy.currentIndex() == temp:
            self.scanEnergyLevel[80] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[80] = level[self.comboBox_Dy.currentIndex()]
        
        print self.scanEnergyLevel[80]
    '''
    "comboBox_Ho changed" event handler
    '''
    def comboBox_Ho_Changed(self,event):
        print "Ho:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[81][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[81][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ho.currentIndex() == temp:
            self.scanEnergyLevel[81] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[81] = level[self.comboBox_Ho.currentIndex()]
        
        print self.scanEnergyLevel[81]
    '''
    "comboBox_Er changed" event handler
    '''
    def comboBox_Er_Changed(self,event):
        print "Er:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[82][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[82][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Er.currentIndex() == temp:
            self.scanEnergyLevel[82] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[82] = level[self.comboBox_Er.currentIndex()]
        
        print self.scanEnergyLevel[82]
    '''
    "comboBox_Tm changed" event handler
    '''
    def comboBox_Tm_Changed(self,event):
        print "Tm:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[83][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[83][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Tm.currentIndex() == temp:
            self.scanEnergyLevel[83] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[83] = level[self.comboBox_Tm.currentIndex()]
        
        print self.scanEnergyLevel[83]
    '''
    "comboBox_Yb changed" event handler
    '''
    def comboBox_Yb_Changed(self,event):
        print "Yb:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[84][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[84][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Yb.currentIndex() == temp:
            self.scanEnergyLevel[84] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[84] = level[self.comboBox_Yb.currentIndex()]
        
        print self.scanEnergyLevel[84]
    '''
    "comboBox_Lu changed" event handler
    '''
    def comboBox_Lu_Changed(self,event):
        print "Lu:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[85][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[85][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Lu.currentIndex() == temp:
            self.scanEnergyLevel[85] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[85] = level[self.comboBox_Lu.currentIndex()]
        
        print self.scanEnergyLevel[85]
    '''
    "comboBox_Ac changed" event handler
    '''
    def comboBox_Ac_Changed(self,event):
        print "Ac:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[86][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[86][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Ac.currentIndex() == temp:
            self.scanEnergyLevel[86] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[86] = level[self.comboBox_Ac.currentIndex()]
        
        print self.scanEnergyLevel[86]
    '''
    "comboBox_Th changed" event handler
    '''
    def comboBox_Th_Changed(self,event):
        print "Th:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[87][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[87][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Th.currentIndex() == temp:
            self.scanEnergyLevel[87] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[87] = level[self.comboBox_Th.currentIndex()]
        
        print self.scanEnergyLevel[87]
    '''
    "comboBox_Pa changed" event handler
    '''
    def comboBox_Pa_Changed(self,event):
        print "Pa:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[88][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[88][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pa.currentIndex() == temp:
            self.scanEnergyLevel[88] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[88] = level[self.comboBox_Pa.currentIndex()]
        
        print self.scanEnergyLevel[88]
    '''
    "comboBox_U changed" event handler
    '''
    def comboBox_U_Changed(self,event):
        print "U:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[89][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[89][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_U.currentIndex() == temp:
            self.scanEnergyLevel[89] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[89] = level[self.comboBox_U.currentIndex()]
        
        print self.scanEnergyLevel[89]
    '''
    "comboBox_Np changed" event handler
    '''
    def comboBox_Np_Changed(self,event):
        print "Np:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[90][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[90][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Np.currentIndex() == temp:
            self.scanEnergyLevel[90] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[90] = level[self.comboBox_Np.currentIndex()]
        
        print self.scanEnergyLevel[90]
    '''
    "comboBox_Pu changed" event handler
    '''
    def comboBox_Pu_Changed(self,event):
        print "Pu:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[91][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[91][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Pu.currentIndex() == temp:
            self.scanEnergyLevel[91] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[91] = level[self.comboBox_Pu.currentIndex()]
        
        print self.scanEnergyLevel[91]
    '''
    "comboBox_Am changed" event handler
    '''
    def comboBox_Am_Changed(self,event):
        print "Am:"
        temp = 0
        level = [0]*len(self.PhotonEnergy[0])
        # Get all energy levels in range
        for i in range(len(self.PhotonEnergy[0])):
            if (self.modifiedPhotonEnergy[92][i] != 0):
                level[temp] = self.modifiedPhotonEnergy[92][i]
                temp = temp + 1
        # Check if "All" is selected
        if self.comboBox_Am.currentIndex() == temp:
            self.scanEnergyLevel[92] = -1
        else:
            # Update scanEnergyLevel
            self.scanEnergyLevel[92] = level[self.comboBox_Am.currentIndex()]
        
        print self.scanEnergyLevel[92]
    
    '''
    "CellDoubleClicked" event handler
    '''
    def handleCellDoubleClicked(self,row,column):
        # Check if column == 2 & line is not empty
        if column == 2 and (row < self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.editItem(self.ui.tableWidget.item(row,column))
    '''
    "CellChanged" event handler
    '''
    def handleCellChanged(self,row,column):
        # Check if column == 2
        if column == 2:
            # If element == Li
            if (self.ui.tableWidget.item(row,0).text() == "Li") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[0] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Be
            elif (self.ui.tableWidget.item(row,0).text() == "Be") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[1] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == B
            elif (self.ui.tableWidget.item(row,0).text() == "B") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[2] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == C
            elif (self.ui.tableWidget.item(row,0).text() == "C") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[3] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == N
            elif (self.ui.tableWidget.item(row,0).text() == "N") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[4] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == O
            elif (self.ui.tableWidget.item(row,0).text() == "O") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[5] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == F
            elif (self.ui.tableWidget.item(row,0).text() == "F") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[6] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ne
            elif (self.ui.tableWidget.item(row,0).text() == "Ne") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[7] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Na
            elif (self.ui.tableWidget.item(row,0).text() == "Na") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[8] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Mg
            elif (self.ui.tableWidget.item(row,0).text() == "Mg") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[9] = self.ui.tableWidget.item(row,column).text().toInt()[0]       
            # If element == Al
            elif (self.ui.tableWidget.item(row,0).text() == "Al") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[10] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Si
            elif (self.ui.tableWidget.item(row,0).text() == "Si") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[11] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == P
            elif (self.ui.tableWidget.item(row,0).text() == "P") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[12] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == S
            elif (self.ui.tableWidget.item(row,0).text() == "S") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[13] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Cl
            elif (self.ui.tableWidget.item(row,0).text() == "Cl") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[14] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ar
            elif (self.ui.tableWidget.item(row,0).text() == "Ar") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[15] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == K
            elif (self.ui.tableWidget.item(row,0).text() == "K") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[16] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ca
            elif (self.ui.tableWidget.item(row,0).text() == "Ca") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[17] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Sc
            elif (self.ui.tableWidget.item(row,0).text() == "Sc") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[18] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ti
            elif (self.ui.tableWidget.item(row,0).text() == "Ti") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[19] = self.ui.tableWidget.item(row,column).text().toInt()[0]  
            # If element == V
            elif (self.ui.tableWidget.item(row,0).text() == "V") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[20] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Cr
            elif (self.ui.tableWidget.item(row,0).text() == "Cr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[21] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Mn
            elif (self.ui.tableWidget.item(row,0).text() == "Mn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[22] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Fe
            elif (self.ui.tableWidget.item(row,0).text() == "Fe") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[23] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Co
            elif (self.ui.tableWidget.item(row,0).text() == "Co") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[24] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ni
            elif (self.ui.tableWidget.item(row,0).text() == "Ni") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[25] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Cu
            elif (self.ui.tableWidget.item(row,0).text() == "Cu") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[26] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Zn
            elif (self.ui.tableWidget.item(row,0).text() == "Zn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[27] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ga
            elif (self.ui.tableWidget.item(row,0).text() == "Ga") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[28] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ge 
            elif (self.ui.tableWidget.item(row,0).text() == "Ge") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[29] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == As
            elif (self.ui.tableWidget.item(row,0).text() == "As") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[30] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Se
            elif (self.ui.tableWidget.item(row,0).text() == "Se") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[31] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Br
            elif (self.ui.tableWidget.item(row,0).text() == "Br") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[32] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Kr
            elif (self.ui.tableWidget.item(row,0).text() == "Kr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[33] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Rb
            elif (self.ui.tableWidget.item(row,0).text() == "Rb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[34] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Sr
            elif (self.ui.tableWidget.item(row,0).text() == "Sr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[35] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Y
            elif (self.ui.tableWidget.item(row,0).text() == "Y") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[36] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Zr
            elif (self.ui.tableWidget.item(row,0).text() == "Zr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[37] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Nb
            elif (self.ui.tableWidget.item(row,0).text() == "Nb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[38] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Mo
            elif (self.ui.tableWidget.item(row,0).text() == "Mo") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[39] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Tc
            elif (self.ui.tableWidget.item(row,0).text() == "Tc") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[40] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ru
            elif (self.ui.tableWidget.item(row,0).text() == "Ru") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[41] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Rh
            elif (self.ui.tableWidget.item(row,0).text() == "Rh") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[42] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pd
            elif (self.ui.tableWidget.item(row,0).text() == "Pd") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[43] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ag
            elif (self.ui.tableWidget.item(row,0).text() == "Ag") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[44] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Cd
            elif (self.ui.tableWidget.item(row,0).text() == "Cd") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[45] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == In
            elif (self.ui.tableWidget.item(row,0).text() == "In") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[46] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Sn
            elif (self.ui.tableWidget.item(row,0).text() == "Sn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[47] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Sb
            elif (self.ui.tableWidget.item(row,0).text() == "Sb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[48] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Te
            elif (self.ui.tableWidget.item(row,0).text() == "Te") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                # Update scanEnergyRange
                self.scanEnergyRange[49] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == I
            elif (self.ui.tableWidget.item(row,0).text() == "I") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[50] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Xe
            elif (self.ui.tableWidget.item(row,0).text() == "Xe") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[51] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Cs
            elif (self.ui.tableWidget.item(row,0).text() == "Cs") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[52] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ba
            elif (self.ui.tableWidget.item(row,0).text() == "Ba") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[53] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Hf
            elif (self.ui.tableWidget.item(row,0).text() == "Hf") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[54] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ta
            elif (self.ui.tableWidget.item(row,0).text() == "Ta") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[55] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == W
            elif (self.ui.tableWidget.item(row,0).text() == "W") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[56] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Re
            elif (self.ui.tableWidget.item(row,0).text() == "Re") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[57] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Os
            elif (self.ui.tableWidget.item(row,0).text() == "Os") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[58] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ir
            elif (self.ui.tableWidget.item(row,0).text() == "Ir") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[59] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pt
            elif (self.ui.tableWidget.item(row,0).text() == "Pt") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[60] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Au
            elif (self.ui.tableWidget.item(row,0).text() == "Au") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[61] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Hg
            elif (self.ui.tableWidget.item(row,0).text() == "Hg") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[62] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Tl
            elif (self.ui.tableWidget.item(row,0).text() == "Tl") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[63] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pb
            elif (self.ui.tableWidget.item(row,0).text() == "Pb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[64] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Bi
            elif (self.ui.tableWidget.item(row,0).text() == "Bi") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[65] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Po
            elif (self.ui.tableWidget.item(row,0).text() == "Po") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[66] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == At
            elif (self.ui.tableWidget.item(row,0).text() == "At") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[67] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Rn
            elif (self.ui.tableWidget.item(row,0).text() == "Rn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[68] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Fr
            elif (self.ui.tableWidget.item(row,0).text() == "Fr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[69] = self.ui.tableWidget.item(row,column).text().toInt()[0]            
            # If element == Ra
            elif (self.ui.tableWidget.item(row,0).text() == "Ra") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[70] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == La
            elif (self.ui.tableWidget.item(row,0).text() == "La") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[71] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ce
            elif (self.ui.tableWidget.item(row,0).text() == "Ce") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[72] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pr
            elif (self.ui.tableWidget.item(row,0).text() == "Pr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[73] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Nd
            elif (self.ui.tableWidget.item(row,0).text() == "Nd") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[74] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pm
            elif (self.ui.tableWidget.item(row,0).text() == "Pm") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[75] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Sm
            elif (self.ui.tableWidget.item(row,0).text() == "Sm") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[76] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Eu
            elif (self.ui.tableWidget.item(row,0).text() == "Eu") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[77] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Gd
            elif (self.ui.tableWidget.item(row,0).text() == "Gd") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[78] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Tb
            elif (self.ui.tableWidget.item(row,0).text() == "Tb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[79] = self.ui.tableWidget.item(row,column).text().toInt()[0]            
            # If element == Dy
            elif (self.ui.tableWidget.item(row,0).text() == "Dy") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[80] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ho
            elif (self.ui.tableWidget.item(row,0).text() == "Ho") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[81] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Er
            elif (self.ui.tableWidget.item(row,0).text() == "Er") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[82] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Tm
            elif (self.ui.tableWidget.item(row,0).text() == "Tm") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[83] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Yb
            elif (self.ui.tableWidget.item(row,0).text() == "Yb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[84] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Lu
            elif (self.ui.tableWidget.item(row,0).text() == "Lu") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[85] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Ac
            elif (self.ui.tableWidget.item(row,0).text() == "Ac") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[86] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Th
            elif (self.ui.tableWidget.item(row,0).text() == "Th") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[87] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pa
            elif (self.ui.tableWidget.item(row,0).text() == "Pa") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[88] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == U
            elif (self.ui.tableWidget.item(row,0).text() == "U") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[89] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Np
            elif (self.ui.tableWidget.item(row,0).text() == "Np") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[90] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Pu
            elif (self.ui.tableWidget.item(row,0).text() == "U") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[91] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            # If element == Am
            elif (self.ui.tableWidget.item(row,0).text() == "U") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[92] = self.ui.tableWidget.item(row,column).text().toInt()[0]
    
    '''
    "MinPhotonEnergy editingFinished" event handler
    '''
    def MinPhotonEnergy_EditingFinished(self):
        if self.ui.MinPhotonEnergy.isModified():
            # Update minEnergy
            self.minEnergy = self.ui.MinPhotonEnergy.text().toDouble()[0]
            # Set tableWidget to empty
            self.ui.tableWidget.setRowCount(0)
            # Set LineCount = 0
            self.LineCount = 0
            # Reset modifiedPhotonEnergy
            self.modifiedPhotonEnergy = deepcopy(self.PhotonEnergy)
            
            # Update availableEnergyCount, modifiedPhotonEnergy & currentElementsStatus
            for i in range(len(self.PhotonEnergy)):
                # Clear availableEnergyCount
                self.availableEnergyCount[i] = 0
                for j in range(len(self.PhotonEnergy[0])):
                    # If PhotonEnergy[i][j] is in range, availableEnergyCount[i] ++
                    if (self.PhotonEnergy[i][j] >= self.minEnergy) and (self.PhotonEnergy[i][j] <= self.maxEnergy):
                        self.availableEnergyCount[i] = self.availableEnergyCount[i] + 1
                    # Otherwise, modifiedEnergyCount[i][j] = 0
                    else:
                        self.modifiedPhotonEnergy[i][j] = 0
                # If no energy level is in range, currentElementsStatus = -1
                if (self.availableEnergyCount[i] == 0):
                    self.currentElementsStatus[i] = -1
                else:
                    # If element is available now, set currentElementsStatus = 0
                    if (self.currentElementsStatus[i] == -1):
                        self.currentElementsStatus[i] = 0
        
        self.ui.MinPhotonEnergy.setModified(False)
    '''
    "MaxPhotonEnergy editingFinished" event handler
    '''
    def MaxPhotonEnergy_EditingFinished(self):
        if self.ui.MaxPhotonEnergy.isModified():
            # Update minEnergy
            self.maxEnergy = self.ui.MaxPhotonEnergy.text().toDouble()[0]
            # Set tableWidget to empty
            self.ui.tableWidget.setRowCount(0)
            # Set LineCount = 0
            self.LineCount = 0
            # Reset modifiedPhotonEnergy
            self.modifiedPhotonEnergy = deepcopy(self.PhotonEnergy)
            
            # Update availableEnergyCount, modifiedPhotonEnergy & currentElementsStatus
            for i in range(len(self.PhotonEnergy)):
                # Clear availableEnergyCount
                self.availableEnergyCount[i] = 0
                for j in range(len(self.PhotonEnergy[0])):
                    # If PhotonEnergy[i][j] is in range, availableEnergyCount[i] ++
                    if (self.PhotonEnergy[i][j] >= self.minEnergy) and (self.PhotonEnergy[i][j] <= self.maxEnergy):
                        self.availableEnergyCount[i] = self.availableEnergyCount[i] + 1
                    # Otherwise, modifiedEnergyCount[i][j] = 0
                    else:
                        self.modifiedPhotonEnergy[i][j] = 0
                # If no energy level is in range, currentElementsStatus = -1
                if (self.availableEnergyCount[i] == 0):
                    self.currentElementsStatus[i] = -1
                else:
                    # If element is available now, set currentElementsStatus = 0
                    if (self.currentElementsStatus[i] == -1):
                        self.currentElementsStatus[i] = 0
        
        self.ui.MaxPhotonEnergy.setModified(False)
    
    '''
    "TopLeftX editingFinished" event handler
    '''
    def TopLeftX_EditingFinished(self):
        if self.ui.TopLeftX.isModified():
            # Clear scene_VL, Reload pixmap_VL
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            # Clear scene_XR
            self.scene_XR.clear()
            # If ROI is in scene_VL
            if (self.selected_VL == 1):
                # Update startPos_VL
                self.startPos_VL.setX(self.ui.TopLeftX.text().toInt()[0])
                # Draw a red rectangle to show new ROI
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            # If ROI is in scene_XR
            elif (self.selected_XR == 1):
                # Update startPos_XR
                self.startPos_XR.setX(self.ui.TopLeftX.text().toInt()[0])
                # Draw a red rectangle to show new ROI
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            # If no ROI has been selected
            else:
                self.ui.TopLeftX.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.TopLeftX.setModified(False)
    '''
    "TopLeftY editingFinished" event handler
    '''
    def TopLeftY_EditingFinished(self):
        if self.ui.TopLeftY.isModified():
            # Clear scene_VL, Reload pixmap_VL
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            # Clear scene_XR
            self.scene_XR.clear()
            # If ROI is in scene_VL
            if (self.selected_VL == 1):
                # Update startPos_VL
                self.startPos_VL.setY(self.ui.TopLeftY.text().toInt()[0])
                # Draw a red rectangle to show new ROI
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            # If ROI is in scene_XR
            elif (self.selected_XR == 1):
                # Update startPos_XR
                self.startPos_XR.setY(self.ui.TopLeftY.text().toInt()[0])
                # Draw a red rectangle to show new ROI
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            # If no ROI has been selected
            else:
                self.ui.TopLeftY.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.TopLeftY.setModified(False)
    '''
    "ScanAreaWidth editingFinished" event handler
    '''
    def ScanAreaWidth_EditingFinished(self):
        if self.ui.ScanAreaWidth.isModified():
            # Clear scene_VL, Reload pixmap_VL
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            # Clear scene_XR
            self.scene_XR.clear()
            # If ROI is in scene_VL
            if (self.selected_VL == 1):
                # Update startPos_VL
                self.width_VL = self.ui.ScanAreaWidth.text().toInt()[0]
                # Draw a red rectangle to show new ROI
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            # If ROI is in scene_XR
            elif (self.selected_XR == 1):
                # Update startPos_XR
                self.width_XR = self.ui.ScanAreaWidth.text().toInt()[0]
                # Draw a red rectangle to show new ROI
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            # If no ROI has been selected
            else:
                self.ui.ScanAreaWidth.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.ScanAreaWidth.setModified(False)
    '''
    "ScanAreaHeight editingFinished" event handler
    '''
    def ScanAreaHeight_EditingFinished(self):
        if self.ui.ScanAreaHeight.isModified():
            # Clear scene_VL, Reload pixmap_VL
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            # Clear scene_XR
            self.scene_XR.clear()
            # If ROI is in scene_VL
            if (self.selected_VL == 1):
                # Update startPos_VL
                self.height_VL = self.ui.ScanAreaHeight.text().toInt()[0]
                # Draw a red rectangle to show new ROI
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            # If ROI is in scene_XR
            elif (self.selected_XR == 1):
                # Update startPos_XR
                self.height_XR = self.ui.ScanAreaHeight.text().toInt()[0]
                # Draw a red rectangle to show new ROI
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            # If no ROI has been selected
            else:
                self.ui.ScanAreaHeight.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.ScanAreaHeight.setModified(False)

    '''
    "Energy clicked" event handler
    '''
    def Energy_clicked(self, enabled):
        if enabled:
            # Call paintPlot
            self.paintPlot()
    '''
    "Channel clicked" event handler
    '''
    def Channel_clicked(self, enabled):
        if enabled:
            # Call paintPlot
            self.paintPlot()
    
    '''
    "minPixelValue editingFinished" event handler
    '''
    def minPixelValue_EditingFinished(self):
        if self.ui.minPixelValue.isModified():
            # Update scale_min
            self.scale_min = self.ui.minPixelValue.text().toDouble()[0]
            # Check if the max == min
            if (self.scale_max == self.scale_min):
                # Change value back
                self.scale_min = np.min(self.imageData_XR)
                self.ui.minPixelValue.setText(unicode(self.scale_min))
                
                print "Min value cannot be equal to Max value!"
                QMessageBox.about(self, "Error",
                                  "Min value cannot be equal to Max value!")
            else:
                # Clear scene_XR
                self.scene_XR.clear()
                # Update newImageData_XR
                self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
                self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
                self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
                # Transfer newImageData_XR to Image_XR
                self.Image_XR = self.numpy2qimage(np.array(255*self.newImageData_XR,
                                                            dtype=int))
                # Transfer Image_XR to pixmap_XR
                self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
                # Resize pixmap_XR
                self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,
                                                       self.sizeHeight,
                                                       QtCore.Qt.IgnoreAspectRatio)
                # Create pixmapItem_XR
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                # Add pixmapItem_XR in scene_XR
                self.scene_XR.addItem(self.pixmapItem_XR)
        
        self.ui.minPixelValue.setModified(False)
    '''
    "maxPixelValue editingFinished" event handler
    '''
    def maxPixelValue_EditingFinished(self):
        if self.ui.maxPixelValue.isModified():
            # Update scale_max
            self.scale_max = self.ui.maxPixelValue.text().toDouble()[0]
            # Check if the max == min
            if (self.scale_max == self.scale_min):
                # Change value back
                self.scale_max = np.max(self.imageData_XR)
                self.ui.maxPixelValue.setText(unicode(self.scale_max))
                
                print "Max value cannot be equal to Min value!"
                QMessageBox.about(self, "Error",
                                  "Max value cannot be equal to Min value!")
            else:
                # Clear scene_XR
                self.scene_XR.clear()
                # Update newImageData_XR
                self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
                self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
                self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
                # Transfer newImageData_XR to Image_XR
                self.Image_XR = self.numpy2qimage(np.array(255*self.newImageData_XR,
                                                            dtype=int))
                # Transfer Image_XR to pixmap_XR
                self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
                # Resize pixmap_XR
                self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,
                                                       self.sizeHeight,
                                                       QtCore.Qt.IgnoreAspectRatio)
                # Create pixmapItem_XR
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                # Add pixmapItem_XR in scene_XR
                self.scene_XR.addItem(self.pixmapItem_XR)
        
        self.ui.maxPixelValue.setModified(False)

    '''
    "FileName editingFinished" event handler
    '''
    def FileName_EditingFinished(self):
        if self.ui.FileName.isModified():
            # Update self.fileName
            self.fileName = self.ui.FileName.text()
        
        self.ui.FileName.setModified(False)

    '''
    "ChangeDirectory clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_ChangeDirectory_clicked(self, checked=None):
        # Open QFileDialog
        dir = QFileDialog.getExistingDirectory(self,
                                               "Open Directory",
                                               self.directory,
                                               QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks);
        # Update self.directory
        self.directory = dir + "/"
        # Show self.directory
        self.ui.Directory.setText(self.directory)

    '''
    "AbortScan clicked" event handler
    '''
    @QtCore.pyqtSlot()
    def on_AbortScan_clicked(self, checked=None):
        print "Abort"
        self.abort = 1

'''
main method
'''
def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MyForm()
    mainWindow.show()
    # Show mainWindow on top
    mainWindow.raise_()
    # Install event filter
    app.installEventFilter(mainWindow)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
