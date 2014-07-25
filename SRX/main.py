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
        # Set up graphics scene and graphics view for plot
        self.scene_Plot = QGraphicsScene()
        self.ui.graphicsView_Plot.setScene(self.scene_Plot)
        # Open HDF5 file
        self.hdf5File = h5py.File('C:/Users/robinliheyi/Desktop/dataForHeyi/2xfm_0430.h5','r+')
        # Load data from HDF5 file
        self.loadData_XR = self.hdf5File['MAPS/XRF_roi']
        print "Open file 'XRF_roi'"
        self.loadData_Plot = self.hdf5File['MAPS/mca_arr']
        print "Open file 'mca_arr'"
        self.calib = self.hdf5File['MAPS/energy_calib']
        print "Open file 'energy_calib'"
        # Store data from hdf5 file
        self.plotData = [0]*2000
        self.channel = [0]*2000
        # Calculate
        for i in range(2000):
            self.plotData[i] = np.sum(self.loadData_Plot[i])
            self.channel[i] = i * self.calib[1] + self.calib[0]
        # Call plot method
        self.paintPlot()
        # Retrieve data for one element
        self.imageData_XR = self.loadData_XR[0]
        # Get max and min pixel value
        self.scale_min = np.min(self.imageData_XR)
        self.scale_max = np.max(self.imageData_XR)
        # Show max and min pixel value
        self.ui.minPixelValue.setText(unicode(self.scale_min))
        self.ui.minPixelValue.editingFinished.connect(self.minPixelValue_EditingFinished)
        self.ui.maxPixelValue.setText(unicode(self.scale_max))
        self.ui.maxPixelValue.editingFinished.connect(self.maxPixelValue_EditingFinished)
        # Transfer pixel value into 0-255
        self.newImageData_XR = (self.imageData_XR - self.scale_min) / (self.scale_max - self.scale_min)
        self.newImageData_XR[self.imageData_XR >= (self.scale_max)] = 1
        self.newImageData_XR[self.imageData_XR <= (self.scale_min)] = 0
        # Transfer numpy array to QImage
        self.Image_XR = self.gray2qimage(np.array(255*self.newImageData_XR,
                                                    dtype=int))
        # Transfer QImage to QPixmap
        self.pixmap_XR = QtGui.QPixmap.fromImage(self.Image_XR)
        self.pixmap_XR = self.pixmap_XR.scaled(200,200,QtCore.Qt.IgnoreAspectRatio)
        self.pixmapItem_XR = QtGui.QGraphicsPixmapItem(self.pixmap_XR)
        # Create graphics scene and graphics view
        self.scene_XR = QGraphicsScene()
        self.scene_XR.addItem(self.pixmapItem_XR)
        self.ui.graphicsView_XR.setScene(self.scene_XR) 
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
        # Elements which user can select
        '''
        # [0] represents Ti, [1] represents V, [2] represents Cr, [3] represents Mn,
        # [4] represents Fe, [5] represents Co, [6] represents Ni, [7] represents Cu,
        # [8] represents Zn, [9] represents Ga, [10] represents Ge, [11] represents As
        # [12] represents Se, [13] represents Br, [14] represents Kr, [15] represents Rb,
        # [16] represents Sr, [17] represents Y, [18] represents Zr, [19] represents Nb,
        # [20] represents Mo, [21] represents Tc, [22] represents Ru, [23] represents Rh,
        # [24] represents Pd, [25] represents Ag, [26] represents Cd, [27] represents In,
        # [28] represents Sn, [29] represents Sb, [30] represents Te, [31] represents I,
        # [32] represents Xe, [33] represents Cs, [34] represents Ba, [35] represents Hf,
        # [36] represents Ta, [37] represents W, [38] represents Re, [39] represents Os,
        # [40] represents Ir, [41] represents Pt, [42] represents Au, [43] represents Hg,
        # [44] represents Tl, [45] represents Pb, [46] represents Bi, [47] represents Po,
        # [48] represents At, [49] represents Rn, [50] represents Fr, [51] represents Ra,
        # [52] represents La, [53] represents Ce, [54] represents Pr, [55] represents Nd,
        # [56] represents Pm, [57] represents Sm, [58] represents Eu, [59] represents Gd,
        # [60] represents Tb, [61] represents Dy, [62] represents Ho, [63] represents Er,
        # [64] represents Tm, [65] represents Yb, [66] represents Lu, [67] represents Ac,
        # [68] represents Th, [69] represents Pa, [70] represents U, [71] represents Np,
        # [72] represents Pu, [73] represents Am,
        '''
        # 0 means not selected, 1 means selected
        self.SelectElements = [0]*74
        # Store selection results temporarily
        self.tempSelectElements = self.SelectElements
        # Data stored in advance
        self.knownElements = [["Ti",8],["V",9],["Cr",10],["Mn",11],["Fe",12],
                              ["Co",13],["Ni",14],["Cu",15],["Zn",16],["Ga",17],
                              ["Ge",18],["As",19],["Se",20],["Br",21],["Kr",22],
                              ["Rb",23],["Sr",24],["Y",25],["Zr",26],["Nb",27],
                              ["Mo",28],["Tc",29],["Ru",30],["Rh",31],["Pd",32],
                              ["Ag",33],["Cd",34],["In",35],["Sn",36],["Sb",37],
                              ["Te",38],["I",39],["Xe",40],["Cs",41],["Ba",42],
                              ["Hf",43],["Ta",44],["W",45],["Re",46],["Os",47],
                              ["Ir",48],["Pt",49],["Au",50],["Hg",51],["Tl",52],
                              ["Pb",53],["Bi",54],["Po",55],["At",56],["Rn",57],
                              ["Fr",58],["Ra",59],["La",60],["Ce",61],["Pr",62],
                              ["Nd",63],["Pm",64],["Sm",65],["Eu",66],["Gd",67],
                              ["Tb",68],["Dy",69],["Ho",70],["Er",71],["Tm",72],
                              ["Yb",73],["Lu",74],["Ac",75],["Th",76],["Pa",77],
                              ["U",78],["Np",79],["Pu",80],["Am",81]]
        self.count = 0
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
        # Connect event handlers with events
        self.ui.tableWidget.cellDoubleClicked.connect(self.handleCellDoubleClicked)
        self.ui.tableWidget.cellChanged.connect(self.handleCellChanged)
        # Set width of each column in the table widget
        self.ui.tableWidget.setColumnWidth(0,100)
        self.ui.tableWidget.setColumnWidth(1,150)
        self.ui.tableWidget.setColumnWidth(2,100)
        self.ui.tableWidget.setColumnWidth(3,100)
        # Store user's selection
        self.energySelection = [""]*74
        self.scanRange = [300]*74
        
        # Ti
        self.energySelection[0] = "4,510.84"
        # V
        self.energySelection[1] = "4,952.20"
        # Cr
        self.energySelection[2] = "5,414.72"
        # Mn
        self.energySelection[3] = "5,898.75"
        # Fe
        self.energySelection[4] = "6,403.84"
        # Co
        self.energySelection[5] = "6,930.32"
        # Ni
        self.energySelection[6] = "7,478.15"
        # Cu
        self.energySelection[7] = "8,047.78"
        # Zn
        self.energySelection[8] = "8,638.86"
        # Ga
        self.energySelection[9] = "9,251.74"
        # Ge
        self.energySelection[10] = "9,886.42"
        # As
        self.energySelection[11] = "10,543.72"
        # Se
        self.energySelection[12] = "11,222.4"
        # Br
        self.energySelection[13] = "11,924.2"
        # Kr
        self.energySelection[14] = "12,649"
        # Rb
        self.energySelection[15] = "13,395.3"
        # Sr
        self.energySelection[16] = "14,165"
        # Y
        self.energySelection[17] = "14,958.4"
        # Zr
        self.energySelection[18] = "15,775.1"
        # Nb
        self.energySelection[19] = "16,615.1"
        # Mo
        self.energySelection[20] = "17,479.34"
        # Tc
        self.energySelection[21] = "18,367.1"
        # Ru
        self.energySelection[22] = "19,279.2"
        # Rh
        self.energySelection[23] = "20,216.1"

        # Handler for closing the main window
        self.connect(self, QtCore.SIGNAL('triggered()'),self.closeEvent)
    
    # When the main window is closed, clear three graphics scenes
    def closeEvent(self, event):
        print "Closing"
        self.scene_Plot.clear()
        self.scene_XR.clear()
        self.scene_VL.clear()
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
    
    # Paint the plot in graphics scene_Plot
    def paintPlot(self):
        # Set the size of the whole figure
        self.figure = plt.Figure(figsize=(7.0,2.0),dpi=100, facecolor='w')
        self.canvas = FigureCanvas(self.figure)
        # Add the canvas into he graphics scene
        self.scene_Plot.addWidget(self.canvas)
        # Draw the plot
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(self.channel,
                       self.plotData,
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
    
    '''
    # Open a new Dialog
    # Allow user to select elements
    '''
    def on_ModifyElement_clicked(self, checked=None):
        if checked==None:return
        '''
        # Open a periodic table for user to select elements
        # Get user's selection
        '''
        (self.tempSelectElements,ok) = PeriodicTable.getSelectedElements(self.SelectElements)
        '''
        # If user click OK, store the selection results
        # Else, discard the selection results
        '''
        if ok == True:
            self.SelectElements = self.tempSelectElements
            # Show selection results in the table view
            self.ui.tableWidget.setRowCount(0)
            self.count = 0
            for index in range(len(self.SelectElements)):
                if self.SelectElements[index] == 1:
                    self.ui.tableWidget.insertRow(self.count)
                    self.ui.tableWidget.setItem(self.count,0,
                                                QTableWidgetItem(QString(self.knownElements[index][0])))
                    self.ui.tableWidget.setItem(self.count,2,
                                                QTableWidgetItem(QString(unicode(self.scanRange[index]))))
                    if index == 0:
                        self.comboBoxTi = QtGui.QComboBox()
                        self.comboBoxTi.insertItem(0,u"K\u03b11: 4,510.84eV")
                        self.comboBoxTi.insertItem(1,u"K\u03b11: 4,510.84eV")
                        self.comboBoxTi.insertItem(2,u"K\u03b21: 4,931.81eV")
                        self.comboBoxTi.insertItem(3,"All")
                        self.comboBoxTi.currentIndexChanged['QString'].connect(self.comboBoxTi_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxTi)
                    elif index == 1:
                        self.comboBoxV = QtGui.QComboBox()
                        self.comboBoxV.insertItem(0,u"K\u03b11: 4,952.2eV")
                        self.comboBoxV.insertItem(1,u"K\u03b12: 4,944.64eV")
                        self.comboBoxV.insertItem(2,u"K\u03b21: 5,427.29eV")
                        self.comboBoxV.insertItem(3,"All")
                        self.comboBoxV.currentIndexChanged['QString'].connect(self.comboBoxV_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxV)
                    elif index == 2:
                        self.comboBoxCr = QtGui.QComboBox()
                        self.comboBoxCr.insertItem(0,u"K\u03b11: 5,414.72eV")
                        self.comboBoxCr.insertItem(1,u"K\u03b12: 5,405.509eV")
                        self.comboBoxCr.insertItem(2,u"K\u03b21: 5,946.71eV")
                        self.comboBoxCr.insertItem(3,"All")
                        self.comboBoxCr.currentIndexChanged['QString'].connect(self.comboBoxCr_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxCr)
                    elif index == 3:
                        self.comboBoxMn = QtGui.QComboBox()
                        self.comboBoxMn.insertItem(0,u"K\u03b11: 5,898.75eV")
                        self.comboBoxMn.insertItem(1,u"K\u03b12: 5,887.65eV")
                        self.comboBoxMn.insertItem(2,u"K\u03b21: 6,490.45eV")
                        self.comboBoxMn.insertItem(3,"All")
                        self.comboBoxMn.currentIndexChanged['QString'].connect(self.comboBoxMn_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxMn)
                    elif index == 4:
                        self.comboBoxFe = QtGui.QComboBox()
                        self.comboBoxFe.insertItem(0,u"K\u03b11: 6,403.84eV")
                        self.comboBoxFe.insertItem(1,u"K\u03b12: 6,390.84eV")
                        self.comboBoxFe.insertItem(2,u"K\u03b21: 7,057.98eV")
                        self.comboBoxFe.insertItem(3,"All")
                        self.comboBoxFe.currentIndexChanged['QString'].connect(self.comboBoxFe_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxFe)
                    elif index == 5:
                        self.comboBoxCo = QtGui.QComboBox()
                        self.comboBoxCo.insertItem(0,u"K\u03b11: 6,930.32eV")
                        self.comboBoxCo.insertItem(1,u"K\u03b12: 6,915.30eV")
                        self.comboBoxCo.insertItem(2,u"K\u03b21: 7,649.43eV")
                        self.comboBoxCo.insertItem(3,"All")
                        self.comboBoxCo.currentIndexChanged['QString'].connect(self.comboBoxCo_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxCo)
                    elif index == 6:
                        self.comboBoxNi = QtGui.QComboBox()
                        self.comboBoxNi.insertItem(0,u"K\u03b11: 7,478.15eV")
                        self.comboBoxNi.insertItem(1,u"K\u03b12: 7,460.89eV")
                        self.comboBoxNi.insertItem(2,u"K\u03b21: 8,264.66eV")
                        self.comboBoxNi.insertItem(3,"All")
                        self.comboBoxNi.currentIndexChanged['QString'].connect(self.comboBoxNi_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxNi)
                    elif index == 7:
                        self.comboBoxCu = QtGui.QComboBox()
                        self.comboBoxCu.insertItem(0,u"K\u03b11: 8,047.78eV")
                        self.comboBoxCu.insertItem(1,u"K\u03b12: 8,027.83eV")
                        self.comboBoxCu.insertItem(2,u"K\u03b21: 8,905.29eV")
                        self.comboBoxCu.insertItem(3,"All")
                        self.comboBoxCu.currentIndexChanged['QString'].connect(self.comboBoxCu_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxCu)
                    elif index == 8:
                        self.comboBoxZn = QtGui.QComboBox()
                        self.comboBoxZn.insertItem(0,u"K\u03b11: 8,638.86eV")
                        self.comboBoxZn.insertItem(1,u"K\u03b12: 8,615.78eV")
                        self.comboBoxZn.insertItem(2,u"K\u03b21: 9,572.0eV")
                        self.comboBoxZn.insertItem(3,"All")
                        self.comboBoxZn.currentIndexChanged['QString'].connect(self.comboBoxZn_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxZn)
                    elif index == 9:
                        self.comboBoxGa = QtGui.QComboBox()
                        self.comboBoxGa.insertItem(0,u"K\u03b11: 9,251.74eV")
                        self.comboBoxGa.insertItem(1,u"K\u03b12: 9,224.82eV")
                        self.comboBoxGa.insertItem(2,u"K\u03b21: 10,264.2eV")
                        self.comboBoxGa.insertItem(3,"All")
                        self.comboBoxGa.currentIndexChanged['QString'].connect(self.comboBoxGa_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxGa)
                    elif index == 10:
                        self.comboBoxGe = QtGui.QComboBox()
                        self.comboBoxGe.insertItem(0,u"K\u03b11: 9,886.42eV")
                        self.comboBoxGe.insertItem(1,u"K\u03b12: 9,855.32eV")
                        self.comboBoxGe.insertItem(2,u"K\u03b21: 10,982.1eV")
                        self.comboBoxGe.insertItem(3,"All")
                        self.comboBoxGe.currentIndexChanged['QString'].connect(self.comboBoxGe_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxGe)
                    elif index == 11:
                        self.comboBoxAs = QtGui.QComboBox()
                        self.comboBoxAs.insertItem(0,u"K\u03b11: 10,543.72eV")
                        self.comboBoxAs.insertItem(1,u"K\u03b12: 10,507.99eV")
                        self.comboBoxAs.insertItem(2,u"K\u03b21: 11,726.2eV")
                        self.comboBoxAs.insertItem(3,"All")
                        self.comboBoxAs.currentIndexChanged['QString'].connect(self.comboBoxAs_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxAs)
                    elif index == 12:
                        self.comboBoxSe = QtGui.QComboBox()
                        self.comboBoxSe.insertItem(0,u"K\u03b11: 11,222.4eV")
                        self.comboBoxSe.insertItem(1,u"K\u03b12: 11,181.4eV")
                        self.comboBoxSe.insertItem(2,u"K\u03b21: 12,495.9eV")
                        self.comboBoxSe.insertItem(3,"All")
                        self.comboBoxSe.currentIndexChanged['QString'].connect(self.comboBoxSe_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxSe)
                    elif index == 13:
                        self.comboBoxBr = QtGui.QComboBox()
                        self.comboBoxBr.insertItem(0,u"K\u03b11: 11,924.2eV")
                        self.comboBoxBr.insertItem(1,u"K\u03b12: 11,877.6eV")
                        self.comboBoxBr.insertItem(2,u"K\u03b21: 13,291.4eV")
                        self.comboBoxBr.insertItem(3,"All")
                        self.comboBoxBr.currentIndexChanged['QString'].connect(self.comboBoxBr_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxBr)
                    elif index == 14:
                        self.comboBoxKr = QtGui.QComboBox()
                        self.comboBoxKr.insertItem(0,u"K\u03b11: 12,649eV")
                        self.comboBoxKr.insertItem(1,u"K\u03b12: 12,598eV")
                        self.comboBoxKr.insertItem(2,u"K\u03b21: 14,112eV")
                        self.comboBoxKr.insertItem(3,"All")
                        self.comboBoxKr.currentIndexChanged['QString'].connect(self.comboBoxKr_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxKr)
                    elif index == 15:
                        self.comboBoxRb = QtGui.QComboBox()
                        self.comboBoxRb.insertItem(0,u"K\u03b11: 13,395.3eV")
                        self.comboBoxRb.insertItem(1,u"K\u03b12: 13,335.8eV")
                        self.comboBoxRb.insertItem(2,u"K\u03b21: 14,961.3eV")
                        self.comboBoxRb.insertItem(3,"All")
                        self.comboBoxRb.currentIndexChanged['QString'].connect(self.comboBoxRb_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxRb)
                    elif index == 16:
                        self.comboBoxSr = QtGui.QComboBox()
                        self.comboBoxSr.insertItem(0,u"K\u03b11: 14,165eV")
                        self.comboBoxSr.insertItem(1,u"K\u03b12: 14,097.9eV")
                        self.comboBoxSr.insertItem(2,u"K\u03b21: 15,835.7eV")
                        self.comboBoxSr.insertItem(3,"All")
                        self.comboBoxSr.currentIndexChanged['QString'].connect(self.comboBoxSr_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxSr)
                    elif index == 17:
                        self.comboBoxY = QtGui.QComboBox()
                        self.comboBoxY.insertItem(0,u"K\u03b11: 14,958.4eV")
                        self.comboBoxY.insertItem(1,u"K\u03b12: 14,882.9eV")
                        self.comboBoxY.insertItem(2,u"K\u03b21: 16,737.8eV")
                        self.comboBoxY.insertItem(3,"All")
                        self.comboBoxY.currentIndexChanged['QString'].connect(self.comboBoxY_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxY)
                    elif index == 18:
                        self.comboBoxZr = QtGui.QComboBox()
                        self.comboBoxZr.insertItem(0,u"K\u03b11: 15,775.1eV")
                        self.comboBoxZr.insertItem(1,u"K\u03b12: 15,690.9eV")
                        self.comboBoxZr.insertItem(2,u"K\u03b21: 17,667.8eV")
                        self.comboBoxZr.insertItem(3,"All")
                        self.comboBoxZr.currentIndexChanged['QString'].connect(self.comboBoxZr_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxZr)
                    elif index == 19:
                        self.comboBoxNb = QtGui.QComboBox()
                        self.comboBoxNb.insertItem(0,u"K\u03b11: 16,615.1eV")
                        self.comboBoxNb.insertItem(1,u"K\u03b12: 16,521.0eV")
                        self.comboBoxNb.insertItem(2,u"K\u03b21: 18,622.5eV")
                        self.comboBoxNb.insertItem(3,"All")
                        self.comboBoxNb.currentIndexChanged['QString'].connect(self.comboBoxNb_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxNb)
                    elif index == 20:
                        self.comboBoxMo = QtGui.QComboBox()
                        self.comboBoxMo.insertItem(0,u"K\u03b11: 17,479.34eV")
                        self.comboBoxMo.insertItem(1,u"K\u03b12: 17,374.3eV")
                        self.comboBoxMo.insertItem(2,u"K\u03b21: 19,608.3eV")
                        self.comboBoxMo.insertItem(3,"All")
                        self.comboBoxMo.currentIndexChanged['QString'].connect(self.comboBoxMo_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxMo)
                    elif index == 21:
                        self.comboBoxTc = QtGui.QComboBox()
                        self.comboBoxTc.insertItem(0,u"K\u03b11: 18,367.1eV")
                        self.comboBoxTc.insertItem(1,u"K\u03b12: 18,250.8eV")
                        self.comboBoxTc.insertItem(2,u"K\u03b21: 20,619eV")
                        self.comboBoxTc.insertItem(3,"All")
                        self.comboBoxTc.currentIndexChanged['QString'].connect(self.comboBoxTc_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxTc)
                    elif index == 22:
                        self.comboBoxRu = QtGui.QComboBox()
                        self.comboBoxRu.insertItem(0,u"K\u03b11: 19,279.2eV")
                        self.comboBoxRu.insertItem(1,u"K\u03b12: 19,150.4eV")
                        self.comboBoxRu.insertItem(2,u"K\u03b21: 21,656.8eV")
                        self.comboBoxRu.insertItem(3,"All")
                        self.comboBoxRu.currentIndexChanged['QString'].connect(self.comboBoxRu_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxRu)
                    elif index == 23:
                        self.comboBoxRh = QtGui.QComboBox()
                        self.comboBoxRh.insertItem(0,u"K\u03b11: 20,216.1eV")
                        self.comboBoxRh.insertItem(1,u"K\u03b12: 20,073.7eV")
                        self.comboBoxRh.insertItem(2,u"K\u03b21: 22,723.6eV")
                        self.comboBoxRh.insertItem(3,"All")
                        self.comboBoxRh.currentIndexChanged['QString'].connect(self.comboBoxRh_Changed)
                        self.ui.tableWidget.setCellWidget(self.count,1,
                                                          self.comboBoxRh)
                        
                    
                    print QString(self.knownElements[index][0]) + ":"
                    print self.energySelection[index]
                    
                    self.count = self.count + 1

    def comboBoxTi_Changed(self,event):
        if unicode(self.comboBoxTi.currentText()) == u"K\u03b11: 4,510.84eV":
            self.energySelection[0] = "4,510.84"
        elif unicode(self.comboBoxTi.currentText()) == u"K\u03b12: 4,504.86eV":
            self.energySelection[0] = "4,504.86"
        elif unicode(self.comboBoxTi.currentText()) == u"K\u03b21: 4,931.81eV":
            self.energySelection[0] = "4,931.81"
        elif unicode(self.comboBoxTi.currentText()) == "All":
            self.energySelection[0] = "4,510.84; 4,504.86; 4,931.81"
        print "Ti:"
        print self.energySelection[0]

    def comboBoxV_Changed(self,event):
        if unicode(self.comboBoxV.currentText()) == u"K\u03b11: 4,952.20eV":
            self.energySelection[1] = "4,952.20"
        elif unicode(self.comboBoxV.currentText()) == u"K\u03b12: 4,944.64eV":
            self.energySelection[1] = "4,944.64"
        elif unicode(self.comboBoxV.currentText()) == u"K\u03b21: 5,427.29eV":
            self.energySelection[1] = "5,427.29"
        elif unicode(self.comboBoxV.currentText()) == "All":
            self.energySelection[1] = "4,952.20; 4,944.64; 5,427.29"
        print "V:"
        print self.energySelection[1]
    def comboBoxCr_Changed(self,event):
        if unicode(self.comboBoxCr.currentText()) == u"K\u03b11: 5,414.72eV":
            self.energySelection[2] = "5,414.72"
        elif unicode(self.comboBoxCr.currentText()) == u"K\u03b12: 5,405.509eV":
            self.energySelection[2] = "5,405.509"
        elif unicode(self.comboBoxCr.currentText()) == u"K\u03b21: 5,946.71eV":
            self.energySelection[2] = "5,946.71"
        elif unicode(self.comboBoxCr.currentText()) == "All":
            self.energySelection[2] = "5,414.72; 5,405.509; 5,946.71"
        print "Cr:"
        print self.energySelection[2]
    def comboBoxMn_Changed(self,event):
        if unicode(self.comboBoxMn.currentText()) == u"K\u03b11: 5,898.75eV":
            self.energySelection[3] = "5,898.75"
        elif unicode(self.comboBoxMn.currentText()) == u"K\u03b12: 5,887.65eV":
            self.energySelection[3] = "5,887.65"
        elif unicode(self.comboBoxMn.currentText()) == u"K\u03b21: 6,490.45eV":
            self.energySelection[3] = "6,490.45"
        elif unicode(self.comboBoxMn.currentText()) == "All":
            self.energySelection[3] = "5,898.75; 5,887.65; 6,490.45"
        print "Mn:"
        print self.energySelection[3]
    def comboBoxFe_Changed(self,event):
        if unicode(self.comboBoxFe.currentText()) == u"K\u03b11: 6,403.84eV":
            self.energySelection[4] = "6,403.84"
        elif unicode(self.comboBoxFe.currentText()) == u"K\u03b12: 6,390.84eV":
            self.energySelection[4] = "6,390.84"
        elif unicode(self.comboBoxFe.currentText()) == u"K\u03b21: 7,057.98eV":
            self.energySelection[4] = "7,057.98"
        elif unicode(self.comboBoxFe.currentText()) == "All":
            self.energySelection[4] = "6,403.84; 6,390.84; 7,057.98"
        print "Fe:"
        print self.energySelection[4]
    def comboBoxCo_Changed(self,event):
        if unicode(self.comboBoxCo.currentText()) == u"K\u03b11: 6,930.32eV":
            self.energySelection[5] = "6,930.32"
        elif unicode(self.comboBoxCo.currentText()) == u"K\u03b12: 6,915.30eV":
            self.energySelection[5] = "6,915.30"
        elif unicode(self.comboBoxCo.currentText()) == u"K\u03b21: 7,649.43eV":
            self.energySelection[5] = "7,649.43"
        elif unicode(self.comboBoxCo.currentText()) == "All":
            self.energySelection[5] = "6,930.32; 6,915.30; 7,649.43"
        print "Co:"
        print self.energySelection[5]
    def comboBoxNi_Changed(self,event):
        if unicode(self.comboBoxNi.currentText()) == u"K\u03b11: 7,478.15eV":
            self.energySelection[6] = "7,478.15"
        elif unicode(self.comboBoxNi.currentText()) == u"K\u03b12: 7,460.89eV":
            self.energySelection[6] = "7,460.89"
        elif unicode(self.comboBoxNi.currentText()) == u"K\u03b21: 8,264.66eV":
            self.energySelection[6] = "8,264.66"
        elif unicode(self.comboBoxNi.currentText()) == "All":
            self.energySelection[6] = "7,478.15; 7,460.89; 8,264.66"
        print "Ni:"
        print self.energySelection[6]
    def comboBoxCu_Changed(self,event):
        if unicode(self.comboBoxCu.currentText()) == u"K\u03b11: 8,047.78eV":
            self.energySelection[7] = "8,047.78"
        elif unicode(self.comboBoxCu.currentText()) == u"K\u03b12: 8,027.83eV":
            self.energySelection[7] = "8,027.83"
        elif unicode(self.comboBoxCu.currentText()) == u"K\u03b21: 8,905.29eV":
            self.energySelection[7] = "8,905.29"
        elif unicode(self.comboBoxCu.currentText()) == "All":
            self.energySelection[7] = "8,047.78; 8,027.83; 8,905.29"
        print "Cu:"
        print self.energySelection[7]
    def comboBoxZn_Changed(self,event):
        if unicode(self.comboBoxZn.currentText()) == u"K\u03b11: 8,638.86eV":
            self.energySelection[8] = "8,638.86"
        elif unicode(self.comboBoxZn.currentText()) == u"K\u03b12: 8,615.78eV":
            self.energySelection[8] = "8,615.78"
        elif unicode(self.comboBoxZn.currentText()) == u"K\u03b21: 9,572.0eV":
            self.energySelection[8] = "9,572.0"
        elif unicode(self.comboBoxZn.currentText()) == "All":
            self.energySelection[8] = "8,638.86; 8,615.78; 9,572.0"
        print "Zn:"
        print self.energySelection[8]
    def comboBoxGa_Changed(self,event):
        if unicode(self.comboBoxGa.currentText()) == u"K\u03b11: 9,251.74eV":
            self.energySelection[9] = "9,251.74"
        elif unicode(self.comboBoxGa.currentText()) == u"K\u03b12: 9,224.82eV":
            self.energySelection[9] = "9,224.82"
        elif unicode(self.comboBoxGa.currentText()) == u"K\u03b21: 10,264.2eV":
            self.energySelection[9] = "10,264.2"
        elif unicode(self.comboBoxGa.currentText()) == "All":
            self.energySelection[9] = "9,251.74; 9,224.82; 10,264.2"
        print "Ga:"
        print self.energySelection[9]
    def comboBoxGe_Changed(self,event):
        if unicode(self.comboBoxGe.currentText()) == u"K\u03b11: 9,886.42eV":
            self.energySelection[10] = "9,886.42"
        elif unicode(self.comboBoxGe.currentText()) == u"K\u03b12: 9,855.32eV":
            self.energySelection[10] = "9,855.32"
        elif unicode(self.comboBoxGe.currentText()) == u"K\u03b21: 10,982.1eV":
            self.energySelection[10] = "10,982.1"
        elif unicode(self.comboBoxGe.currentText()) == "All":
            self.energySelection[10] = "9,886.42; 9,855.32; 10,982.1"
        print "Ge:"
        print self.energySelection[10]
    def comboBoxAs_Changed(self,event):
        if unicode(self.comboBoxAs.currentText()) == u"K\u03b11: 10,543.72eV":
            self.energySelection[11] = "10,543.72"
        elif unicode(self.comboBoxAs.currentText()) == u"K\u03b12: 10,507.99eV":
            self.energySelection[11] = "10,507.99"
        elif unicode(self.comboBoxAs.currentText()) == u"K\u03b21: 11,726.2eV":
            self.energySelection[11] = "11,726.2"
        elif unicode(self.comboBoxAs.currentText()) == "All":
            self.energySelection[11] = "10,543.72; 10,507.99; 11,726.2"
        print "As:"
        print self.energySelection[11]
    def comboBoxSe_Changed(self,event):
        if unicode(self.comboBoxSe.currentText()) == u"K\u03b11: 11,222.4eV":
            self.energySelection[12] = "11,222.4"
        elif unicode(self.comboBoxSe.currentText()) == u"K\u03b12: 11,181.4eV":
            self.energySelection[12] = "11,181.4"
        elif unicode(self.comboBoxSe.currentText()) == u"K\u03b21: 12,495.9eV":
            self.energySelection[12] = "12,495.9"
        elif unicode(self.comboBoxSe.currentText()) == "All":
            self.energySelection[12] = "11,222.4; 11,181.4; 12,495.9"
        print "Se:"
        print self.energySelection[12]
    def comboBoxBr_Changed(self,event):
        if unicode(self.comboBoxBr.currentText()) == u"K\u03b11: 11,924.2eV":
            self.energySelection[13] = "11,924.2"
        elif unicode(self.comboBoxBr.currentText()) == u"K\u03b12: 11,877.6eV":
            self.energySelection[13] = "11,877.6"
        elif unicode(self.comboBoxBr.currentText()) == u"K\u03b21: 13,291.4eV":
            self.energySelection[13] = "13,291.4"
        elif unicode(self.comboBoxBr.currentText()) == "All":
            self.energySelection[13] = "11,924.2 11,877.6 13,291.4"
        print "Br:"
        print self.energySelection[13]
    def comboBoxKr_Changed(self,event):
        if unicode(self.comboBoxKr.currentText()) == u"K\u03b11: 12,649eV":
            self.energySelection[14] = "12,649"
        elif unicode(self.comboBoxKr.currentText()) == u"K\u03b12: 12,598eV":
            self.energySelection[14] = "12,598"
        elif unicode(self.comboBoxKr.currentText()) == u"K\u03b21: 14,112eV":
            self.energySelection[14] = "14,112"
        elif unicode(self.comboBoxKr.currentText()) == "All":
            self.energySelection[14] = "12,649; 12,598; 14,112"
        print "Kr:"
        print self.energySelection[14]
    def comboBoxRb_Changed(self,event):
        if unicode(self.comboBoxRb.currentText()) == u"K\u03b11: 13,395.3eV":
            self.energySelection[15] = "13,395.3"
        elif unicode(self.comboBoxRb.currentText()) == u"K\u03b12: 13,335.8eV":
            self.energySelection[15] = "13,335.8"
        elif unicode(self.comboBoxRb.currentText()) == u"K\u03b21: 14,961.3eV":
            self.energySelection[15] = "14,961.3"
        elif unicode(self.comboBoxRb.currentText()) == "All":
            self.energySelection[15] = "13,395.3; 13,335.8; 14,961.3"
        print "Rb:"
        print self.energySelection[15]
    def comboBoxSr_Changed(self,event):
        if unicode(self.comboBoxSr.currentText()) == u"K\u03b11: 14,165eV":
            self.energySelection[16] = "14,165"
        elif unicode(self.comboBoxSr.currentText()) == u"K\u03b12: 14,097.9eV":
            self.energySelection[16] = "14,097.9"
        elif unicode(self.comboBoxSr.currentText()) == u"K\u03b21: 15,835.7eV":
            self.energySelection[16] = "15,835.7"
        elif unicode(self.comboBoxSr.currentText()) == "All":
            self.energySelection[16] = "14,165; 14,097.9; 15,835.7"
        print "Sr:"
        print self.energySelection[16]
    def comboBoxY_Changed(self,event):
        if unicode(self.comboBoxY.currentText()) == u"K\u03b11: 14,958.4eV":
            self.energySelection[17] = "14,958.4"
        elif unicode(self.comboBoxY.currentText()) == u"K\u03b12: 14,882.9eV":
            self.energySelection[17] = "14,882.9"
        elif unicode(self.comboBoxY.currentText()) == u"K\u03b21: 16,737.8eV":
            self.energySelection[17] = "16,737.8"
        elif unicode(self.comboBoxY.currentText()) == "All":
            self.energySelection[17] = "14,958.4; 14,882.9; 16,737.8"
        print "Y:"
        print self.energySelection[17]
    def comboBoxZr_Changed(self,event):
        if unicode(self.comboBoxZr.currentText()) == u"K\u03b11: 15,775.1eV":
            self.energySelection[18] = "15,775.1"
        elif unicode(self.comboBoxZr.currentText()) == u"K\u03b12: 15,690.9eV":
            self.energySelection[18] = "15,690.9"
        elif unicode(self.comboBoxZr.currentText()) == u"K\u03b21: 17,667.8eV":
            self.energySelection[18] = "17,667.8"
        elif unicode(self.comboBoxZr.currentText()) == "All":
            self.energySelection[18] = "15,775.1; 15,690.9; 17,667.8"
        print "Zr:"
        print self.energySelection[18]
    def comboBoxNb_Changed(self,event):
        if unicode(self.comboBoxNb.currentText()) == u"K\u03b11: 16,615.1eV":
            self.energySelection[19] = "16,615.1"
        elif unicode(self.comboBoxNb.currentText()) == u"K\u03b12: 16,521.0eV":
            self.energySelection[19] = "16,521.0"
        elif unicode(self.comboBoxNb.currentText()) == u"K\u03b21: 18,622.5eV":
            self.energySelection[19] = "18,622.5"
        elif unicode(self.comboBoxNb.currentText()) == "All":
            self.energySelection[19] = "16,615.1; 16,521.0; 18,622.5"
        print "Nb:"
        print self.energySelection[19]
    def comboBoxMo_Changed(self,event):
        if unicode(self.comboBoxMo.currentText()) == u"K\u03b11: 17,479.34eV":
            self.energySelection[20] = "17,479.34"
        elif unicode(self.comboBoxMo.currentText()) == u"K\u03b12: 17,374.3eV":
            self.energySelection[20] = "17,374.3"
        elif unicode(self.comboBoxMo.currentText()) == u"K\u03b21: 19,608.3eV":
            self.energySelection[20] = "19,608.3"
        elif unicode(self.comboBoxMo.currentText()) == "All":
            self.energySelection[20] = "17,479.34; 17,374.3; 19,608.3"
        print "Mo:"
        print self.energySelection[20]
    def comboBoxTc_Changed(self,event):
        if unicode(self.comboBoxTc.currentText()) == u"K\u03b11: 18,367.1eV":
            self.energySelection[21] = "18,367.1"
        elif unicode(self.comboBoxTc.currentText()) == u"K\u03b12: 18,250.8eV":
            self.energySelection[21] = "18,250.8"
        elif unicode(self.comboBoxTc.currentText()) == u"K\u03b21: 20,619eV":
            self.energySelection[21] = "20,619"
        elif unicode(self.comboBoxTc.currentText()) == "All":
            self.energySelection[21] = "18,367.1; 18,250.8; 20,619"
        print "Tc:"
        print self.energySelection[21]
    def comboBoxRu_Changed(self,event):
        if unicode(self.comboBoxRu.currentText()) == u"K\u03b11: 19,279.2eV":
            self.energySelection[22] = "19,279.2"
        elif unicode(self.comboBoxRu.currentText()) == u"K\u03b12: 19,150.4eV":
            self.energySelection[22] = "19,150.4"
        elif unicode(self.comboBoxRu.currentText()) == u"K\u03b21: 21,656.8eV":
            self.energySelection[22] = "21,656.8"
        elif unicode(self.comboBoxRu.currentText()) == "All":
            self.energySelection[22] = "19,279.2; 19,150.4; 21,656.8"
        print "Ru:"
        print self.energySelection[22]
    def comboBoxRh_Changed(self,event):
        if unicode(self.comboBoxRh.currentText()) == u"K\u03b11: 20,216.1eV":
            self.energySelection[23] = "20,216.1"
        elif unicode(self.comboBoxRh.currentText()) == u"K\u03b12: 20,073.7eV":
            self.energySelection[23] = "20,073.7"
        elif unicode(self.comboBoxRh.currentText()) == u"K\u03b21: 22,723.6eV":
            self.energySelection[23] = "22,723.6"
        elif unicode(self.comboBoxRh.currentText()) == "All":
            self.energySelection[23] = "20,216.1; 20,073.7; 22,723.6"
        print "Rh:"
        print self.energySelection[23]
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
                self.pixmap_XR = self.pixmap_XR.scaled(200,200,QtCore.Qt.IgnoreAspectRatio)
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
                self.pixmap_XR = self.pixmap_XR.scaled(200,200,QtCore.Qt.IgnoreAspectRatio)
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
    app.installEventFilter(mainWindow)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
