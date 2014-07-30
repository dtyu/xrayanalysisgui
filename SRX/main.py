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
        
##        # Set up graphics scene and graphics view for plot
##        self.scene_Plot = QGraphicsScene()
##        self.ui.graphicsView_Plot.setScene(self.scene_Plot)
##        # Open HDF5 file
##        self.hdf5File = h5py.File('C:/Users/robinliheyi/Desktop/dataForHeyi/2xfm_0430.h5','r+')
##        # Load data from HDF5 file
##        self.loadData_XR = self.hdf5File['MAPS/XRF_roi']
##        print "Open file 'XRF_roi'"
##        self.loadData_Plot = self.hdf5File['MAPS/mca_arr']
##        print "Open file 'mca_arr'"
##        self.calib = self.hdf5File['MAPS/energy_calib']
##        print "Open file 'energy_calib'"
##        # Store data from hdf5 file
##        self.plotData = [0]*2000
##        self.energy = [0]*2000
##        # Calculate
##        for i in range(2000):
##            self.plotData[i] = np.sum(self.loadData_Plot[i])
##            self.energy[i] = i * self.calib[1] + self.calib[0]
##        # Call plot method
##        self.paintPlot()
##        # Retrieve data for one element
##        self.imageData_XR = self.loadData_XR[0]
##        # Get max and min pixel value
##        self.scale_min = np.min(self.imageData_XR)
##        self.scale_max = np.max(self.imageData_XR)
##        # Show max and min pixel value
##        self.ui.minPixelValue.setText(unicode(self.scale_min))
##        self.ui.minPixelValue.editingFinished.connect(self.minPixelValue_EditingFinished)
##        self.ui.maxPixelValue.setText(unicode(self.scale_max))
##        self.ui.maxPixelValue.editingFinished.connect(self.maxPixelValue_EditingFinished)
##        # Transfer pixel value into 0-255
##        self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
##        self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
##        self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
##        # Transfer numpy array to QImage
##        self.Image_XR = self.gray2qimage(np.array(255*self.newImageData_XR,
##                                                    dtype=int))
##        # Transfer QImage to QPixmap
##        self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
##        # Resize the QPixmap
##        self.sizeWidth = 200
##        self.sizeHeight = 200
##        self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,self.sizeHeight,QtCore.Qt.IgnoreAspectRatio)
##        # Create pixmapItem
##        self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
##        # Create graphics scene and graphics view
##        self.scene_XR = QGraphicsScene()
##        self.scene_XR.addItem(self.pixmapItem_XR)
##        self.ui.graphicsView_XR.setScene(self.scene_XR) 
        '''
        # Load the first image
        # Create the first GraphicsPixmapItem
        # Add the item to the first GraphicsScene
        # Set the scene in the first GraphicsView
        '''
        self.pixmap_VL = QtGui.QPixmap("image1.jpg")
        self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
        self.scene_VL = QGraphicsScene()
        self.scene_VL.addItem(self.pixmapItem_VL)
        self.ui.graphicsView_VL.setScene(self.scene_VL)
        '''
        # Load the second image
        # Create the second GraphicsPixmapItem
        # Add the item to the second GraphicsScene
        # Set the scene in the second GraphicsView
        '''
        # self.pixmap_XR = QtGui.QPixmap("image2.jpg")
        # self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
        # self.scene_XR = QGraphicsScene()
        # self.scene_XR.addItem(self.pixmapItem_XR)
        # self.ui.graphicsView_XR.setScene(self.scene_XR)
        
        # Create the first RubberBand in the first GraphicsView
        self.rubberBand_VL = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                             self.ui.graphicsView_VL)
        # Create the second RubberBand in the second GraphicsView
        self.rubberBand_XR = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                             self.ui.graphicsView_XR)
        
        # Load Photo Energy from .txt file
        self.PhotonEnergy = np.loadtxt('PhotonEnergy.txt')
        # Energy Range(KeV)
        self.minEnergy = 100
        self.maxEnergy = 26000
        # Elements which user can select
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
        # 0 means not selected, 1 means selected
        self.SelectElements = [0]*93
        # Store selection results temporarily
        self.tempSelectElements = self.SelectElements
        self.count = 0
        # Store user's selection
        self.energySelection = [0]*93
        self.energyCount = [0]*93
        self.scanRange = [300]*93
        self.knownElements = ["Li","B","Be","C","N",
                              "O","F","Ne","Na","Mg",
                              "Al","Si","P","S","Cl",
                              "Ar","K","Ca","Sc","Ti",
                              "V","Cr","Mn","Fe","Co",
                              "Ni","Cu","Zn","Ga","Ge",
                              "As","Se","Br","Kr","Rb",
                              "Sr","Y","Zr","Nb","Mo",
                              "Tc","Ru","Rh","Pd","Ag",
                              "Cd","In","Sn","Sb","Te",
                              "I","Xe","Cs","Ba","Hf",
                              "Ta","W","Re","Os","Ir",
                              "Pt","Au","Hg","Tl","Pb",
                              "Bi","Po","At","Rn","Fr",
                              "Ra","La","Ce","Pr","Nd",
                              "Pm","Sm","Eu","Gd","Tb",
                              "Dy","Ho","Er","Tm","Yb",
                              "Lu","Ac","Th","Pa","U",
                              "Np","Pu","Am"]
        
        '''
        # Initialize variables
        '''
        # Motor Position
        self.xPos = 353
        self.yPos = 252
        self.zPos = 305
        # shift Motor Position
        self.xStep = 0
        self.yStep = 0
        self.zStep = 0
        # Scan Step Size
        self.scanStepX = 1
        self.scanStepY = 1
        # Dwell Time
        self.dwellTime = 0.1
        # Scan Area
        self.width_VL = 0
        self.height_VL = 0
        self.width_XR = 0
        self.height_XR = 0
        '''
        # If user have selected a ROI in VL, then selected_VL = 1
        # Similar with selected_XR
        '''
        self.selected_VL = 0
        self.selected_XR = 0
        '''
        # Initialize starting point, width and height for selected area
        '''
        # XR
        self.startPos_XR = QPoint(0,0)
        self.width_XR = 0
        self.height_XR = 0
        # VL
        self.startPos_VL = QPoint(0,0)
        self.width_VL = 0
        self.height_VL = 0
        
        '''
        # Show the initialized values
        '''
        self.ui.TopLeftX.setText(unicode(self.startPos_XR.x()))
        self.ui.TopLeftX.editingFinished.connect(self.TopLeftX_EditingFinished)
        self.ui.TopLeftY.setText(unicode(self.startPos_XR.y()))
        self.ui.TopLeftY.editingFinished.connect(self.TopLeftY_EditingFinished)
        self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
        self.ui.ScanAreaWidth.editingFinished.connect(self.ScanAreaWidth_EditingFinished)
        self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
        self.ui.ScanAreaHeight.editingFinished.connect(self.ScanAreaHeight_EditingFinished)
        # Initialized as 353,252,305
        # Show Motor Position
        self.ui.MotorPositionX.setText(unicode(self.xPos))
        self.ui.MotorPositionY.setText(unicode(self.yPos))
        self.ui.MotorPositionZ.setText(unicode(self.zPos))
        # Initialized as Motor Position
        # User can enter desired Motor Position and click GO
        self.ui.toMotorPositionX.setText(unicode(self.xPos))
        self.ui.toMotorPositionY.setText(unicode(self.yPos))
        self.ui.toMotorPositionZ.setText(unicode(self.zPos))
        # Initialized as 0
        # User can enter values and click + for increasing, - for decreasing
        self.ui.shiftMotorPositionX.setText(unicode(self.xStep))
        self.ui.shiftMotorPositionY.setText(unicode(self.yStep))
        self.ui.shiftMotorPositionZ.setText(unicode(self.zStep))
        # Initialized as 1
        self.ui.ScanStepSizeX.setText(unicode(self.scanStepX))
        self.ui.ScanStepSizeY.setText(unicode(self.scanStepY))
        # Initialized as 0.1
        self.ui.DwellTime.setText(unicode(self.dwellTime))
        # Set titles for the table widget
        self.ui.tableWidget.setHorizontalHeaderLabels([QString("Element"),
                                                       QString("Energy"),
                                                       QString("Range"),
                                                       QString("Count")])
        # Connect table widget event handlers with events
        self.ui.tableWidget.cellDoubleClicked.connect(self.handleCellDoubleClicked)
        self.ui.tableWidget.cellChanged.connect(self.handleCellChanged)
        # Connect radio button event handlers with events
        self.ui.Energy.toggled.connect(self.Energy_clicked)
        self.ui.Channel.toggled.connect(self.Channel_clicked)
        # Set width of each column in the table widget
        self.ui.tableWidget.setColumnWidth(0,100)
        self.ui.tableWidget.setColumnWidth(1,150)
        self.ui.tableWidget.setColumnWidth(2,100)
        self.ui.tableWidget.setColumnWidth(3,100)

        # Handler for closing the main window
        self.connect(self, QtCore.SIGNAL('triggered()'),self.closeEvent)
    
    # When the main window is closed, clear three graphics scenes
    def closeEvent(self, event):
        print "Closing"
        self.scene_Plot.clear()
        self.scene_XR.clear()
        self.scene_VL.clear()
        
    '''
    # Handles mouse events in graphicsView_VL and graphicsView_XR
    '''
    def eventFilter(self, source, event):
        # mouse press event in graphicsView_VL
        if (event.type() == QtCore.QEvent.GraphicsSceneMousePress
                and source is self.scene_VL):
            if event.button() == QtCore.Qt.LeftButton:
                # Clear graphicsScene_VL and graphicsScene_XR
                self.scene_VL.clear()
                self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
                self.scene_VL.addItem(self.pixmapItem_VL)
                self.scene_XR.clear()
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                self.scene_XR.addItem(self.pixmapItem_XR)
                # Set selected_VL = 0 and selected_XR = 0
                self.selected_VL = 0
                self.selected_XR = 0
                # Set the width and the height of the scan area to 0
                self.width_VL = 0
                self.height_VL = 0
                self.ui.ScanAreaWidth.setText(unicode(self.width_VL))
                self.ui.ScanAreaHeight.setText(unicode(self.height_VL))
                
                # Get mouse coordinates
                self.startPos_VL = self.ui.graphicsView_VL.mapFromScene(event.scenePos())
                # Show start point coordinates
                self.ui.TopLeftX.setText(unicode(self.startPos_VL.x()))
                self.ui.TopLeftY.setText(unicode(self.startPos_VL.y()))
                # Start rubberBnad
                self.rubberBand_VL.setGeometry(QtCore.QRect(self.startPos_VL,
                                                            QtCore.QSize()))
                self.rubberBand_VL.show()
                
                return super(MyForm, self).eventFilter(source, event)
        # mouse move event in graphicsView_VL
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
        # mouse release event in graphicsView_VL
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseRelease
                and source is self.scene_VL):
            if event.button() == QtCore.Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_VL = self.ui.graphicsView_VL.mapFromScene(event.scenePos())
                # Calculate scan area
                self.width_VL = self.currentPos_VL.x() - self.startPos_VL.x()
                self.height_VL = self.currentPos_VL.y() - self.startPos_VL.y()
                # Set selected_VL = 1
                self.selected_VL = 1
                # Hide the rubberBand_VL
                self.rubberBand_VL.hide()
                # Draw a red rectangle to show the selected area
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
                # Show the width and the height of the scan area
                self.ui.ScanAreaWidth.setText(unicode(self.width_VL))
                self.ui.ScanAreaHeight.setText(unicode(self.height_VL))
                
                return super(MyForm, self).eventFilter(source, event)

        # mouse press event in graphicsView_XR
        if (event.type() == QtCore.QEvent.GraphicsSceneMousePress
                and source is self.scene_XR):
            if event.button() == QtCore.Qt.LeftButton:
                # Clear graphicsScene_VL and graphicsScene_XR
                self.scene_VL.clear()
                self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
                self.scene_VL.addItem(self.pixmapItem_VL)
                self.scene_XR.clear()
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                self.scene_XR.addItem(self.pixmapItem_XR)
                # Set selected_XR = 0 and selected_VL = 0
                self.selected_XR = 0
                self.selected_VL = 0
                # Set the width and the height of the scan area to 0
                self.width_XR = 0
                self.height_XR = 0
                self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
                self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
                
                # Get mouse coordinates
                self.startPos_XR = self.ui.graphicsView_XR.mapFromScene(event.scenePos())
                # Show start point coordinates
                self.ui.TopLeftX.setText(unicode(self.startPos_XR.x()))
                self.ui.TopLeftY.setText(unicode(self.startPos_XR.y()))
                # Start rubberBnad
                self.rubberBand_XR.setGeometry(QtCore.QRect(self.startPos_XR, QtCore.QSize()))
                self.rubberBand_XR.show()
                
                return super(MyForm, self).eventFilter(source, event)
        # mouse move event in graphicsView_XR
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
        # mouse release event in graphicsView_XR
        if (event.type() == QtCore.QEvent.GraphicsSceneMouseRelease
                and source is self.scene_XR):
            if event.button() == QtCore.Qt.LeftButton:
                # Get mouse coordinates
                self.currentPos_XR = self.ui.graphicsView_XR.mapFromScene(event.scenePos())
                # Calculate scan area
                self.width_XR = self.currentPos_XR.x() - self.startPos_XR.x()
                self.height_XR = self.currentPos_XR.y() - self.startPos_XR.y()
                # Set selected_XR = 1
                self.selected_XR = 1
                # Hide the rubberBand_XR
                self.rubberBand_XR.hide()
                # Draw a red rectangle to show the selected area
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
                # Show the width and the height of the scan area
                self.ui.ScanAreaWidth.setText(unicode(self.width_XR))
                self.ui.ScanAreaHeight.setText(unicode(self.height_XR))
                
                return super(MyForm, self).eventFilter(source, event)
        
        return False
    
    '''
    Handles button click events
    '''
    # Click 1st Go, change Motor Position X
    @QtCore.pyqtSlot()
    def on_changeMotorPositionX_clicked(self, checked=None):
        self.xPos = int(self.ui.toMotorPositionX.text())
        self.ui.MotorPositionX.setText(unicode(self.xPos))
    # Click 2nd Go, change Motor Position Y
    @QtCore.pyqtSlot()
    def on_changeMotorPositionY_clicked(self, checked=None):
        self.yPos = int(self.ui.toMotorPositionY.text())
        self.ui.MotorPositionY.setText(unicode(self.yPos))
    # Click 3rd Go, change Motor Position Z
    @QtCore.pyqtSlot()
    def on_changeMotorPositionZ_clicked(self, checked=None):
        self.zPos = int(self.ui.toMotorPositionZ.text())
        self.ui.MotorPositionZ.setText(unicode(self.zPos))
    
    # Click 1st -, decrease Motor Position X
    @QtCore.pyqtSlot()
    def on_minusMotorPositionX_clicked(self, checked=None):
        self.xStep = int(self.ui.shiftMotorPositionX.text())
        self.xPos -= self.xStep
        self.ui.MotorPositionX.setText(unicode(self.xPos))
    # Click 1st +, increase Motor Position X
    @QtCore.pyqtSlot()
    def on_plusMotorPositionX_clicked(self, checked=None):
        self.xStep = int(self.ui.shiftMotorPositionX.text())
        self.xPos += self.xStep
        self.ui.MotorPositionX.setText(unicode(self.xPos))
    
    # Click 2nd -, decrease Motor Position Y
    @QtCore.pyqtSlot()
    def on_minusMotorPositionY_clicked(self, checked=None):
        self.yStep = int(self.ui.shiftMotorPositionY.text())
        self.yPos -= self.yStep
        self.ui.MotorPositionY.setText(unicode(self.yPos))
    # Click 2nd +, increase Motor Position Y
    @QtCore.pyqtSlot()
    def on_plusMotorPositionY_clicked(self, checked=None):
        self.yStep = int(self.ui.shiftMotorPositionY.text())
        self.yPos += self.yStep
        self.ui.MotorPositionY.setText(unicode(self.yPos))
    
    # Click 3rd -, decrease Motor Position Z
    @QtCore.pyqtSlot()
    def on_minusMotorPositionZ_clicked(self, checked=None):
        self.zStep = int(self.ui.shiftMotorPositionZ.text())
        self.zPos -= self.zStep
        self.ui.MotorPositionZ.setText(unicode(self.zPos))
    # Click 3rd +, increase Motor Position Z
    @QtCore.pyqtSlot()
    def on_plusMotorPositionZ_clicked(self, checked=None):
        self.zStep = int(self.ui.shiftMotorPositionZ.text())
        self.zPos += self.zStep
        self.ui.MotorPositionZ.setText(unicode(self.zPos))

    # Start scanning process
    @QtCore.pyqtSlot()
    def on_ExecuteScan_clicked(self, checked=None):
        '''
        # If user has not selected a ROI
        # Print out a warning message
        '''
        if (self.selected_VL != 1 and self.selected_XR != 1):
            print "Please select ROI first!"
            QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        '''
        # If user has selected a ROI
        # Calculate TimeLeft
        # Start scanning process
        '''
        
        if (self.selected_VL == 1 or self.selected_XR == 1):
            # Get ScanStepSizeX
            self.scanStepX = int(self.ui.ScanStepSizeX.text())
            # Get ScanStepSizeY
            self.scanStepY = int(self.ui.ScanStepSizeY.text())
            # Get DwellTime
            self.dwellTime = float(self.ui.DwellTime.text())
            # Check if user has clicked MoveToStartPoint
            if (self.xPos != int(self.ui.TopLeftX.text())
                    or self.yPos != int(self.ui.TopLeftY.text())):
                print "Please click MoveToStartPoint button first!"
                QMessageBox.about(self, "Error",
                                  "Please click MoveToStartPoint button first!")
            else:
                '''
                # If user has selected a ROI in VL
                '''
                if self.selected_VL == 1:
                    # Calculate TimeLeft
                    self.timeLeft = self.width_VL * self.height_VL / (self.dwellTime * 1000)
                    # Show TimeLeft
                    self.ui.TimeLeft.setText(unicode(self.timeLeft)+"s")
                    # Print out coordinates of X and Y
                    print "Y Position Change:"
                    for j in range(0,self.height_VL,self.scanStepY):
                        self.yPos += self.scanStepY
                        print self.yPos
                        self.ui.MotorPositionY.setText(unicode(self.yPos))
                    print "X Position Change:"  
                    for i in range(0,self.width_VL,self.scanStepX):
                        self.xPos += self.scanStepX
                        print self.xPos
                        self.ui.MotorPositionX.setText(unicode(self.xPos))
                    # Set selected_VL = 0
                    self.selected_VL = 0
                '''
                # If user has selected a ROI in XR
                '''
                if self.selected_XR == 1:
                    # Calculate TimeLeft
                    self.timeLeft = self.width_XR * self.height_XR / (self.dwellTime * 1000)
                    # Show TimeLeft
                    self.ui.TimeLeft.setText(unicode(self.timeLeft)+"s")
                    # Print out coordinates of X and Y
                    print "Y Position Change:"
                    for j in range(0,self.height_XR,self.scanStepY):
                        self.yPos += self.scanStepY
                        print self.yPos
                        self.ui.MotorPositionY.setText(unicode(self.yPos))
                    print "X Position Change:"  
                    for i in range(0,self.width_XR,self.scanStepX):
                        self.xPos += self.scanStepX
                        print self.xPos
                        self.ui.MotorPositionX.setText(unicode(self.xPos))
                    # Set selected_XR = 0
                    self.selected_XR = 0
    
    # Move the motor to selected start point
    @QtCore.pyqtSlot()
    def on_MoveToStartPoint_clicked(self, checked=None):
        if (self.selected_VL == 1 or self.selected_XR == 1):
            self.xPos = int(self.ui.TopLeftX.text())
            self.yPos = int(self.ui.TopLeftY.text())

            self.ui.MotorPositionX.setText(unicode(self.xPos))
            self.ui.MotorPositionY.setText(unicode(self.yPos))
        else:
            print "Please select ROI first!"
            QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
    
    # Transfer numpy array to QImage
    def gray2qimage(self,gray):
        if (len(gray.shape) != 2):
            raise ValueError("gray2QImage can only convert 2D arrays")    
        gray = np.require(gray, np.uint8, 'C')
        
        (h, w) = gray.shape
        
        result = QImage(gray.data, w, h, QImage.Format_Indexed8)
        result.ndarray = gray
        for i in range(256):
                result.setColor(i, QColor(i, i, i).rgb())
        return result
    # Paint the plot in graphics scene_Plot
    def paintPlot(self):
        # Set the size of the whole figure
        self.figure = plt.Figure(figsize=(5.5,2.0),dpi=100, facecolor='w')
        self.canvas = FigureCanvas(self.figure)
        # Add the canvas into he graphics scene
        self.scene_Plot.addWidget(self.canvas)
        # Draw the plot
        self.axes = self.figure.add_subplot(111)

        if (self.ui.Energy.isChecked()):
            self.axes.plot(self.energy,
                           self.plotData,
                           linestyle = 'solid',
                           marker = '',
                           color = 'green',
                           #label = 'XANES'
                           )
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
        # Show a title
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
        # Draw the canvas
        self.canvas.draw()
    
    # Open a new Dialog
    # Allow user to select elements
    def on_ModifyElement_clicked(self, checked=None):
        if checked==None:return
        
        # Open a periodic table for user to select elements
        # Get user's selection
        (self.tempSelectElements,ok) = PeriodicTable.getSelectedElements(self.SelectElements)
        # If user click OK, store the selection results
        # Else, discard the selection results
        if ok == True:
            self.SelectElements = self.tempSelectElements
            # Show selection results in the table view
            self.ui.tableWidget.setRowCount(0)
            self.count = 0
            for index in range(len(self.SelectElements)):
                if self.SelectElements[index] == 1:
                    self.label = [u"K\u03b11: ",u"K\u03b12: ",u"K\u03b21: ",
                                  u"L\u03b11: ",u"L\u03b12: ",u"L\u03b21: ",
                                  u"L\u03b22: ",u"L\u03b31: ",u"M\u03b11: "]
                    if index == 0:
                        self.energyCount[0] = 0
                        if (self.ui.tableWidget.rowCount() < self.count + 1):
                            self.ui.tableWidget.insertRow(self.count)
                        self.comboBox_Li = QtGui.QComboBox()
                        self.energyAvailable_Li = [0]*9
                        for i in range(9):
                            if (self.PhotonEnergy[index][i] > self.minEnergy) \
                               and (self.PhotonEnergy[index][i] < self.maxEnergy):
                                self.comboBox_Li.insertItem(self.energyCount[0], self.label[i]+ \
                                                           QString(unicode(self.PhotonEnergy[index][i])) + "eV")
                                self.energyAvailable_Li[self.energyCount[0]] = self.PhotonEnergy[index][i]
                                self.energyCount[0] = self.energyCount[0] + 1
                        self.comboBox_Li.insertItem(self.energyCount[0],"All")
                        self.comboBox_Li.currentIndexChanged['QString'].connect(self.comboBox_Li_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBox_Li)
                        if self.energyCount[0] == 0:
                            self.SelectElements[index] = 0
                            self.ui.tableWidget.removeCellWidget(self.count,1)
                            if self.ui.tableWidget.rowCount() != 1:
                                self.ui.tableWidget.removeRow(self.count)
                            print "Li is not available!"
                        else:
                            self.energySelection[0] = self.energyAvailable_Li[0]
                            self.ui.tableWidget.setItem(self.count,0,
                                                        QTableWidgetItem(QString(self.knownElements[index])))
                            self.ui.tableWidget.setItem(self.count,2,
                                                        QTableWidgetItem(QString(unicode(self.scanRange[index]))))
                            self.count = self.count + 1
                    
                    elif index == 1:
                        self.energyCount[1] = 0
                        if (self.ui.tableWidget.rowCount() < self.count + 1):
                            self.ui.tableWidget.insertRow(self.count)
                        self.comboBox_Be = QtGui.QComboBox()
                        self.energyAvailable_Be = [0]*9
                        for i in range(9):
                            if (self.PhotonEnergy[index][i] > self.minEnergy) \
                               and (self.PhotonEnergy[index][i] < self.maxEnergy):
                                self.comboBox_Be.insertItem(self.energyCount[1], self.label[i]+ \
                                                           QString(unicode(self.PhotonEnergy[index][i])) + "eV")
                                self.energyAvailable_Be[self.energyCount[1]] = self.PhotonEnergy[index][i]
                                self.energyCount[1] = self.energyCount[1] + 1
                        self.comboBox_Be.insertItem(self.energyCount[1],"All")
                        self.comboBox_Be.currentIndexChanged['QString'].connect(self.comboBox_Be_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBox_Be)
                        if self.energyCount[1] == 0:
                            self.SelectElements[index] = 0
                            self.ui.tableWidget.removeCellWidget(self.count,1)
                            if self.ui.tableWidget.rowCount() != 1:
                                self.ui.tableWidget.removeRow(self.count)
                            print "Be is not available!"
                        else:
                            self.energySelection[1] = self.energyAvailable_Be[0]
                            self.ui.tableWidget.setItem(self.count,0,
                                                        QTableWidgetItem(QString(self.knownElements[index])))
                            self.ui.tableWidget.setItem(self.count,2,
                                                        QTableWidgetItem(QString(unicode(self.scanRange[index]))))
                            self.count = self.count + 1

    def comboBox_Li_Changed(self,event):
        print "Li:"
        for i in range(self.energyCount[0]):
            if self.comboBox_Li.currentIndex() == i:
                self.energySelection[0] = self.energyAvailable_Li[i]
        if self.comboBox_Li.currentIndex() == self.energyCount[0]:
            self.energySelection[0] = -1
        print self.energySelection[0]

    def comboBox_Be_Changed(self,event):
        print "Be:"
        for i in range(self.energyCount[1]):
            if self.comboBox_Be.currentIndex() == i:
                self.energySelection[1] = self.energyAvailable_Be[i]
        if self.comboBox_Be.currentIndex() == self.energyCount[1]:
            self.energySelection[1] = -1
        print self.energySelection[1]
    
    # Handle double clicked event in the table widget
    def handleCellDoubleClicked(self,row,column):
        if column == 2 and (row < self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.editItem(self.ui.tableWidget.item(row,column))
    # Handle cell content change event in the table widget
    def handleCellChanged(self,row,column):
        if column == 2:
            if (self.ui.tableWidget.item(row,0).text() == "Ti") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[0] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "V") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[1] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Cr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[2] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Mn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[3] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Fe") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[4] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Co") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[5] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Ni") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[6] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Cu") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[7] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Zn") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[8] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Ga") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[4] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Ge") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[5] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "As") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[6] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Se") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[7] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Br") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[8] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Kr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[4] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Rb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[5] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Sr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[6] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Y") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[7] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Zr") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[8] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Nb") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[4] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Mo") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[5] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Tc") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[6] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Ru") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[7] = self.ui.tableWidget.item(row,column).text().toInt()[0]
            elif (self.ui.tableWidget.item(row,0).text() == "Rh") and \
               (self.ui.tableWidget.item(row,column).text().toInt()[0] != 0):
                self.scanRange[8] = self.ui.tableWidget.item(row,column).text().toInt()[0]
    # If user change the TopLeft X coordinate of the ROI
    def TopLeftX_EditingFinished(self):
        if self.ui.TopLeftX.isModified():
            # Clear graphicsScene_VL and graphicsScene_XR
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
            # Draw a red rectangle to show the selected area
            if (self.selected_VL == 1):
                self.startPos_VL.setX(self.ui.TopLeftX.text().toInt()[0])
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            elif (self.selected_XR == 1):
                self.startPos_XR.setX(self.ui.TopLeftX.text().toInt()[0])
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            else:
                self.ui.TopLeftX.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.TopLeftX.setModified(False)
    
    # If user change the TopLeft Y coordinate of the ROI
    def TopLeftY_EditingFinished(self):
        if self.ui.TopLeftY.isModified():
            # Clear graphicsScene_VL and graphicsScene_XR
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
            # Draw a red rectangle to show the selected area
            if (self.selected_VL == 1):
                self.startPos_VL.setY(self.ui.TopLeftY.text().toInt()[0])
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            elif (self.selected_XR == 1):
                self.startPos_XR.setY(self.ui.TopLeftY.text().toInt()[0])
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            else:
                self.ui.TopLeftY.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.TopLeftY.setModified(False)
    # If user change the width of the ROI
    def ScanAreaWidth_EditingFinished(self):
        if self.ui.ScanAreaWidth.isModified():
            # Clear graphicsScene_VL and graphicsScene_XR
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
            # Draw a red rectangle to show the selected area
            if (self.selected_VL == 1):
                self.width_VL = self.ui.ScanAreaWidth.text().toInt()[0]
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            elif (self.selected_XR == 1):
                self.width_XR = self.ui.ScanAreaWidth.text().toInt()[0]
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            else:
                self.ui.ScanAreaWidth.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.ScanAreaWidth.setModified(False)
    
    # If user change the height of the ROI
    def ScanAreaHeight_EditingFinished(self):
        if self.ui.ScanAreaHeight.isModified():
            # Clear graphicsScene_VL and graphicsScene_XR
            self.scene_VL.clear()
            self.pixmapItem_VL = QtGui.QGraphicsPixmapItem(self.pixmap_VL)
            self.scene_VL.addItem(self.pixmapItem_VL)
            self.scene_XR.clear()
            self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
            self.scene_XR.addItem(self.pixmapItem_XR)
            # Draw a red rectangle to show the selected area
            if (self.selected_VL == 1):
                self.height_VL = self.ui.ScanAreaHeight.text().toInt()[0]
                self.selectedRect_VL = QRectF(self.ui.graphicsView_VL.mapToScene(self.startPos_VL.x(),
                                                                                 self.startPos_VL.y()),
                                              QSizeF(self.width_VL,self.height_VL))
                self.scene_VL.addRect(self.selectedRect_VL,QtCore.Qt.red)
            elif (self.selected_XR == 1):
                self.height_XR = self.ui.ScanAreaHeight.text().toInt()[0]
                self.selectedRect_XR = QRectF(self.ui.graphicsView_XR.mapToScene(self.startPos_XR.x(),
                                                                                 self.startPos_XR.y()),
                                              QSizeF(self.width_XR,self.height_XR))
                self.scene_XR.addRect(self.selectedRect_XR,QtCore.Qt.red)
            else:
                self.ui.ScanAreaHeight.setText("0")
                print "Please select ROI first!"
                QMessageBox.about(self, "Error",
                                  "Please select ROI first!")
        self.ui.ScanAreaHeight.setModified(False)
    # If user click radio button "Energy"
    def Energy_clicked(self, enabled):
        if enabled:
            # Call plot method
            self.paintPlot()

    # If user click radio button "Channel"
    def Channel_clicked(self, enabled):
        if enabled:
            # Call plot method
            self.paintPlot()
    
    # If user change min pixel value
    def minPixelValue_EditingFinished(self):
        if self.ui.minPixelValue.isModified():
            # Get the value enterd by the user
            self.scale_min = self.ui.minPixelValue.text().toDouble()[0]
            # Check if the max == min
            if (self.scale_max == self.scale_min):
                self.scale_min = np.min(self.imageData_XR)
                self.ui.minPixelValue.setText(unicode(self.scale_min))
                
                print "Min value cannot be equal to Max value!"
                QMessageBox.about(self, "Error",
                                  "Min value cannot be equal to Max value!")
            else:
                self.scene_XR.clear()
                # Recalculate the data matrix
                self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
                self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
                self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
                # Transfer numpy array to QImage
                self.Image_XR = self.numpy2qimage(np.array(255*self.newImageData_XR,
                                                            dtype=int))
                # Transfer QImage to QPixmap
                self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
                self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,
                                                       self.sizeHeight,
                                                       QtCore.Qt.IgnoreAspectRatio)
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                self.scene_XR.addItem(self.pixmapItem_XR)
        
        self.ui.minPixelValue.setModified(False)
    
    # If user change max pixel value
    def maxPixelValue_EditingFinished(self):
        if self.ui.maxPixelValue.isModified():
            # Get the value enterd by the user
            self.scale_max = self.ui.maxPixelValue.text().toDouble()[0]
            # Check if the max == min
            if (self.scale_max == self.scale_min):
                self.scale_max = np.max(self.imageData_XR)
                self.ui.maxPixelValue.setText(unicode(self.scale_max))
                
                print "Max value cannot be equal to Min value!"
                QMessageBox.about(self, "Error",
                                  "Max value cannot be equal to Min value!")
            else:
                self.scene_XR.clear()
                # Recalculate the data matrix
                self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
                self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
                self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
                # Transfer numpy array to QImage
                self.Image_XR = self.numpy2qimage(np.array(255*self.newImageData_XR,
                                                            dtype=int))
                # Transfer QImage to QPixmap
                self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
                self.pixmap_XR = self.pixmap_XR.scaled(self.sizeWidth,
                                                       self.sizeHeight,
                                                       QtCore.Qt.IgnoreAspectRatio)
                self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
                self.scene_XR.addItem(self.pixmapItem_XR)
        
        self.ui.maxPixelValue.setModified(False)

'''
# main method
'''
def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MyForm()
    mainWindow.show()
    mainWindow.raise_()
    app.installEventFilter(mainWindow)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
