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
                # Start rubberBnad
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
            if (self.xPos == int(self.ui.TopLeftX.text())
                    or self.yPos == int(self.ui.TopLeftY.text())):
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
##                    # data in y coordinates
##                    self.plotData = [0]*2000
##                    # data in x coordinates
##                    self.energy = [0]*2000
##                    # Calculate plotData & energy
##                    for i in range(2000):
##                        self.plotData[i] = np.sum(self.loadData_Plot[i])
##                        self.energy[i] = i * self.calib[1] + self.calib[0]
##                    # Plot
##                    self.paintPlot()
                    # Retrieve data of one element (Mg in this case)
                    self.oriImageData_XR = self.loadData_XR[0]

                    # Write HDF5 file
                    myfile = unicode(self.directory + self.fileName + ".hdf5")
                    self.testFile = h5py.File(myfile, "w")
                    dset = self.testFile.create_dataset('subgroup/dataset',
                                                        (len(self.oriImageData_XR),
                                                         len(self.oriImageData_XR[0])),
                                                        dtype='d')
                    
                    print "Start"
                    # len(self.oriImageData_XR)
                    for i in range(len(self.oriImageData_XR)):
                        # Show TimeLeft
                        self.ui.TimeLeft.setText(unicode(i+1)+" / "+unicode(len(self.oriImageData_XR)))
                        
                        # Write data
                        dset[i,:] = self.oriImageData_XR[i]

                        # self.tempFile = h5py.File('mytestfile.h5','r+')
                        self.imageData_XR = self.testFile['subgroup/dataset'] 
                        
                        # Get max & min pixel value
                        self.scale_min = np.min(self.imageData_XR)
                        self.scale_max = np.max(self.imageData_XR)
                        # Show max & min value
                        self.ui.minPixelValue.setText(unicode(self.scale_min))
                        self.ui.maxPixelValue.setText(unicode(self.scale_max))
                        
                        # Scale value into 0-255
                        # self.newImageData_XR = 255 * (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
                        # self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
                        # self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
                        
                        # Transfer newImageData_XR to Image_XR
                        myimage = unicode(self.directory+self.fileName+".png")
                        plt.imsave(myimage, self.imageData_XR, cmap=plt.cm.gray)
                        
                        # self.Image_XR = qimage2ndarray.array2qimage(np.array(self.imageData_XR,dtype = float),normalize=True)
                        ## Transfer Image_XR to pixmap_XR
                        # self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
                        self.pixmap_XR = QtGui.QPixmap(unicode(self.directory+self.fileName+".png"))
                        
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
                        
                        # Call repaint method to refresh GUI
                        self.ui.graphicsView_XR.viewport().repaint()
                        # Wait for 1 second
                        time.sleep(1)

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
            if (self.ui.tableWidget.item(row,0).text() == "Be") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 300):
                # Update scanEnergyRange
                self.scanEnergyRange[1] = self.ui.tableWidget.item(row,column).text().toInt()[0]
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
            # Clear scene_XR, Reload pixmap_XR
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
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
            # Clear scene_XR, Reload pixmap_XR
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
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
            # Clear scene_XR, Reload pixmap_XR
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
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
            # Clear scene_XR, Reload pixmap_XR
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
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
        self.directory = dir + "\\"
        # Show self.directory
        self.ui.Directory.setText(self.directory)

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
