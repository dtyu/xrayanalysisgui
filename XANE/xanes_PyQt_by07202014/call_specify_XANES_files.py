from __future__ import division
import sys
import os
from specify_XANES_files import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QCoreApplication
import scipy
import data_struct
import data_stack
import analyze
import nnma
import henke
import matplotlib 
import qimage2ndarray
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

class common:
    def __init__(self):
        self.stack_loaded = 0

class MyForm(QtGui.QDialog):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)
    #'Browse Data' callback
    QtCore.QObject.connect(self.ui.button_load_XANES, QtCore.SIGNAL('clicked()'), self.GetSamFile)
    #'Background' callback
    QtCore.QObject.connect(self.ui.button_load_BKG, QtCore.SIGNAL('clicked()'), self.GetBkgFile)
    #'Load Reference 1' callback
    QtCore.QObject.connect(self.ui.load_ref1, QtCore.SIGNAL('clicked()'), self.GetRef1File)
    #'Load Reference 2' callback
    QtCore.QObject.connect(self.ui.load_ref2, QtCore.SIGNAL('clicked()'), self.GetRef2File)
    #'Load Reference 3' callback
    QtCore.QObject.connect(self.ui.load_ref3, QtCore.SIGNAL('clicked()'), self.GetRef3File)
    #'Load and Show Image' callback
    QtCore.QObject.connect(self.ui.back_normal, QtCore.SIGNAL('clicked()'), self.LoadShowImage)
    #'slider_img_maxscale' callback
    self.ui.slider_img_maxscale.valueChanged.connect(self.MaxscaleShowImage)
    #'slider_img_minscale' callback
    self.ui.slider_img_minscale.valueChanged.connect(self.MinscaleShowImage)
    #'slider_img' callback
    self.ui.slider_img.valueChanged.connect(self.SliderShowImage)
    #'current_img' callback
    self.ui.current_img.textChanged.connect(self.SelectShowImage)

    #'Select Point' callback
    QtCore.QObject.connect(self.ui.select_point, QtCore.SIGNAL('clicked()'), self.SelectPoint)
    #'X_cord' callback
    self.ui.x_cord.textChanged.connect(self.GetXCord)
    #'Y_cord' callback
    self.ui.y_cord.textChanged.connect(self.GetYCord)
    #'Binning' callback
    self.ui.bin.textChanged.connect(self.GetBin)
    #'Edge Jump :' callback
    self.ui.edit_edge_jump.textChanged.connect(self.EdgeJumpShowImage)
    #'Plot Spectrum (selected)' callback
    QtCore.QObject.connect(self.ui.update_spectrum, QtCore.SIGNAL('clicked()'), self.PlotSpectrum)

    #'Select Method:' callback
    self.ui.select_method.activated.connect(self.SelectMethod)
    #'Set as Raw Bkg' callback
    QtCore.QObject.connect(self.ui.set_raw_bkg, QtCore.SIGNAL('clicked()'), self.SetRawBkg)
    #'Fit Base Line' callback
    QtCore.QObject.connect(self.ui.fit_base_line, QtCore.SIGNAL('clicked()'), self.FitBaseLine)
    #'Base Line = 0' callback
    QtCore.QObject.connect(self.ui.base_line_zero, QtCore.SIGNAL('clicked()'), self.BaseLineZero)

    #'use default scaling (first/last 5 points)' callback
    self.ui.default_scaling.stateChanged.connect(self.DefaultScaling)
    #'pre_start' callback
    self.ui.pre_start.valueChanged.connect(self.PreStart)
    #'pre_end' callback
    self.ui.pre_end.valueChanged.connect(self.PreEnd)
    #'post_start' callback
    self.ui.post_start.valueChanged.connect(self.PostStart)
    #'post_end' callback
    self.ui.post_end.valueChanged.connect(self.PostEnd)
    #'edge_start' callback
    self.ui.edge_start.valueChanged.connect(self.EdgeStart)
    #'edge_end' callback
    self.ui.edge_end.valueChanged.connect(self.EdgeEnd)
 
    #'pre_plot' callback
    QtCore.QObject.connect(self.ui.pre_plot, QtCore.SIGNAL('clicked()'), self.PrePlot)
    #'post_plot' callback
    QtCore.QObject.connect(self.ui.post_plot, QtCore.SIGNAL('clicked()'), self.PostPlot)
    #'edge_plot' callback
    QtCore.QObject.connect(self.ui.edge_plot, QtCore.SIGNAL('clicked()'), self.EdgePlot)


    self.ui.listWidget.addItem('Raw Spectrum (ROI) "*"')
    self.ui.listWidget.addItem('Normalized Spectrum (ROI)')
    self.ui.listWidget.addItem('Raw Bulk Spectrum "o"')
    self.ui.listWidget.addItem('Normalized Bulk Spectrum')
    self.ui.listWidget.addItem('Fitted Results (ROI)')
    self.ui.listWidget.addItem('Reference 1 "red -"')
    self.ui.listWidget.addItem('Reference 2 "green -"')
    self.ui.listWidget.addItem('Reference 3 "blue -"')

    self.ui.select_method.addItems(['select one from below :','base line norm','raw background norm','pre/post edge norm'])
    ############################
    self.scale_max = 1.00
    self.scale_min = 0.00
    self.currentSliderStep = 0
    self.selectpointPress = False
    self.bin = 1
    self.rawImagePosX = None
    self.rawImagePosY = None
    #self.ref1 = None
    #self.ref2 = None
    #self.ref3 = None
    self.edgeJump = -100

  def GetSamFile(self):
    if self.ui.samTxrm.isChecked() == True:
        wildcard =  "TXRM (*.txrm)" 
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
        filepath = str(filepath)
        if filepath == '':
          QtGui.QMessageBox.information(self, "Empty File","Please select a txrm file.")
          return      
        self.directory =  os.path.dirname(str(filepath))
        self.filename =  os.path.basename(str(filepath))
        self.filepath = filepath
        self.ui.text_XANES_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:    " +self.filename)
        self.sam_directory = self.directory
        self.sam_filename = self.filename
        self.sam_filepath = self.filepath 
        self.ui.button_load_BKG.setEnabled(True) 
    if self.ui.samXrm.isChecked() == True:
        wildcard =  "XRM (*.xrm)" 
        filepaths = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', '', wildcard)
        if filepaths == '':
          QtGui.QMessageBox.information(self, "Empty File","Please select multiple xrm files.")
          return      
        self.directory = os.path.dirname(str(filepaths[0]))
        self.filename_first = os.path.basename(str(filepaths[0]))
        self.filename_last = os.path.basename(str(filepaths[-1]))
        self.filepaths = filepaths
        self.ui.text_XANES_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:    " +self.filename_first+ "\n" +self.filename_last)
        self.sam_directory = self.directory
        self.sam_filepaths = self.filepaths
	self.ui.button_load_BKG.setEnabled(True) 

  def GetBkgFile(self):
    if self.ui.bkgTxrm.isChecked() == True:
        wildcard =  "TXRM (*.txrm)" 
        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
        filepath = str(filepath)
        if filepath == '':
          QtGui.QMessageBox.information(self, "Empty File","Please select a txrm file.")
          return      
        self.directory =  os.path.dirname(str(filepath))
        self.filename =  os.path.basename(str(filepath))
        self.filepath = filepath
        self.ui.text_BKG_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:     " +self.filename)
        self.bkg_directory = self.directory
        self.bkg_filename = self.filename
        self.bkg_filepath = self.filepath 
        self.ui.back_normal.setEnabled(True) 
    if self.ui.bkgXrm.isChecked() == True:
        wildcard =  "XRM (*.xrm)" 
	filepaths = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', '', wildcard)
        if filepaths == '':
          QtGui.QMessageBox.information(self, "Empty File","Please select multiple xrm files.")
          return      
        self.directory = os.path.dirname(str(filepaths[0]))
        self.filename_first = os.path.basename(str(filepaths[0]))
        self.filename_last = os.path.basename(str(filepaths[-1]))
        self.filepaths = filepaths
        self.ui.text_BKG_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:     " +self.filename_first+ "\n" +self.filename_last)
        self.bkg_directory = self.directory
        self.bkg_filepaths = self.filepaths
	self.ui.back_normal.setEnabled(True) 

  def GetRef1File(self, wildcard = ''):
    wildcard =  "TXT (*.txt)" 
    filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
    filepath = str(filepath)
    if filepath == '':
      QtGui.QMessageBox.information(self, "Empty File","Please select a txt file.")
      return      
    self.filepath = filepath
    self.ref1 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref1.append(float(line.split()[1]))
    #print(ref1)
    self.filename =  os.path.basename(str(filepath))
    self.ui.ref1name.setText(self.filename)

  def GetRef2File(self, wildcard = ''):
    wildcard = "TXT (*.txt)" 
    filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
    filepath = str(filepath)
    if filepath == '':
      QtGui.QMessageBox.information(self, "Empty File","Please select a txt file.")
      return      
    self.filepath = filepath
    self.ref2 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref2.append(float(line.split()[1]))
    self.filename =  os.path.basename(str(filepath))
    self.ui.ref2name.setText(self.filename)

  def GetRef3File(self, wildcard = ''):
    wildcard = "TXT (*.txt)" 
    filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
    filepath = str(filepath)
    if filepath == '':
      QtGui.QMessageBox.information(self, "Empty File","Please select a txt file.")
      return      
    self.filepath = filepath
    self.ref3 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref3.append(float(line.split()[1]))
    self.filename =  os.path.basename(str(filepath))
    self.ui.ref3name.setText(self.filename)

  def LoadShowImage(self):
    self.ui.status_bkgnorm.setText('status: running')
    QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    #initialization
    self.data_struct = data_struct.h5()
    self.stk_sam = data_stack.data(self.data_struct)
    self.stk_bkg = data_stack.data(self.data_struct)
    self.anlz_sam = analyze.analyze(self.stk_sam)
    self.anlz_bkg = analyze.analyze(self.stk_bkg)
    self.common = common()
    #load sample and background
    if self.ui.samTxrm.isChecked() == True:            
        #self.new_stack_refresh()  
        self.stk_sam.new_data()
        #self.stk.data_struct.delete_data()
        self.anlz_sam.delete_data()  
        self.stk_sam.read_txrm(self.sam_filepath, self.data_struct)                 
    if self.ui.samXrm.isChecked() == True:              
        self.stk_sam.new_data()
        self.anlz_sam.delete_data()
        #self.sam_filelist = os.path.basename(str(self.sam_filepaths))
        self.stk_sam.read_xrm_list(self.sam_filepaths) 
    if self.ui.bkgTxrm.isChecked() == True:
        self.stk_bkg.new_data()
        self.anlz_bkg.delete_data() 
        self.stk_bkg.read_txrm(self.bkg_filepath, self.data_struct)
    if self.ui.bkgXrm.isChecked() == True:
        self.stk_bkg.new_data()
        self.anlz_bkg.delete_data()
        #self.bkg_filelist = os.path.basename(str(self.bkg_filepaths))
        self.stk_bkg.read_xrm_list(self.bkg_filepaths)
    self.common.stack_loaded == 1
    #update image information
    self.iev = int(self.stk_sam.n_ev)
    self.currentSliderStep = self.iev - 1
    self.ev = self.data_struct.exchange.energy
    #calculate scaleimg
    sam_image_stack = self.stk_sam.absdata.copy() 
    bkg_image_stack = self.stk_bkg.absdata.copy()
    self.scale_image_stack = np.true_divide(sam_image_stack,bkg_image_stack)  
    #show image
    self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
    QtGui.QApplication.restoreOverrideCursor()
    #refresh_widgets
    self.ui.slider_img_maxscale.setEnabled(True)
    self.ui.slider_img_minscale.setEnabled(True)
    self.ui.slider_img.setEnabled(True)
    self.ui.current_img.setEnabled(True)
    self.ui.current_img.setText(str(self.iev))
    self.ui.slider_img.setMinimum(1)
    self.ui.slider_img.setMaximum(self.iev)
    self.ui.total_img.setText(str(self.iev))
    self.ui.status_bkgnorm.setText('status: complete')
    self.ui.text_minscale.setText("Min   0   %")
    self.ui.text_maxscale.setText("Max  100  %")
    self.ui.select_point.setEnabled(True)
    self.ui.update_spectrum.setEnabled(True)
    self.ui.x_cord.setEnabled(True)
    self.ui.y_cord.setEnabled(True)
    self.ui.edit_edge_jump.setEnabled(True)

    self.ui.pre_start.setMinimum(1)
    self.ui.pre_start.setMaximum(self.iev)
    self.ui.pre_end.setMinimum(1)
    self.ui.pre_end.setMaximum(self.iev)
    self.ui.post_start.setMinimum(1)
    self.ui.post_start.setMaximum(self.iev)
    self.ui.post_end.setMinimum(1)
    self.ui.post_end.setMaximum(self.iev)
    self.ui.edge_start.setMinimum(1)
    self.ui.edge_start.setMaximum(self.iev)
    self.ui.edge_end.setMinimum(1)
    self.ui.edge_end.setMaximum(self.iev)

    self.ui.text_pre_start.setText('PreEstart')
    self.ui.text_pre_end.setText('PreEend')
    self.ui.text_post_start.setText('PostEstart')
    self.ui.text_post_end.setText('PostEend')
    self.ui.text_edge_start.setText('EdgeStart')
    self.ui.text_edge_end.setText('EdgeEnd')

  def EdgeEnd(self,value):
      self.edgeEnd = int(value)
      self.ui.text_edge_end.setText(str(self.edgeEnd))

  def ShowImage(self,currentSliderStep,scale_min,scale_max,rawImagePosX = None,rawImagePosY = None,bin = None,edgeJump = None):
      self.orgImage = self.scale_image_stack[:,:,int(currentSliderStep)]
      self.currentImage = (self.orgImage - scale_min) / (scale_max - scale_min)
      self.currentImage[self.orgImage >= (scale_max)] = 1
      self.currentImage[self.orgImage <= (scale_min)] = 0

      self.edgeJump = edgeJump
      self.edgeDiff = np.array((255*self.scale_image_stack[:,:,0]), dtype=int) - np.array((255*self.scale_image_stack[:,:,int(self.iev - 1)]), dtype=int)
      self.filter_image = np.ones((self.stk_sam.n_rows, self.stk_sam.n_cols), dtype=np.int)
      self.filter_image[self.edgeDiff < self.edgeJump] = 0
      self.currentImage[self.filter_image == 0] = 0

      image = qimage2ndarray.numpy2qimage(np.array(255*self.currentImage, dtype=int))
      pixmap = QtGui.QPixmap.fromImage(image)
      pixmap = pixmap.scaled(379, 379,QtCore.Qt.IgnoreAspectRatio)
      self.rotated_pixmap = pixmap.transformed(QtGui.QMatrix().rotate(-90),Qt.SmoothTransformation)
      #pixmap = QtGui.QPixmap.fromImage(ImageQt(scipy.misc.toimage(image)))
      self.scene = QGraphicsScene(self)
      item = QGraphicsPixmapItem(self.rotated_pixmap)
      self.scene.addItem(item)
      pen   = QtGui.QPen(QtGui.QColor(QtCore.Qt.yellow))
      if ((rawImagePosX is not None) & (rawImagePosY is not None) & (bin != 1)): 
          self.scene.addRect(self.rawImagePosX-self.bin,self.rawImagePosY-self.bin,self.bin*2,self.bin*2,pen)
          self.scene.addLine(self.rawImagePosX-10,self.rawImagePosY,self.rawImagePosX+10,self.rawImagePosY,pen)
	  self.scene.addLine(self.rawImagePosX,self.rawImagePosY-10,self.rawImagePosX,self.rawImagePosY+10,pen)
      elif ((rawImagePosX is not None) & (rawImagePosY is not None) & (bin == 1)):
	  self.scene.addLine(self.rawImagePosX-10,self.rawImagePosY,self.rawImagePosX+10,self.rawImagePosY,pen)
	  self.scene.addLine(self.rawImagePosX,self.rawImagePosY-10,self.rawImagePosX,self.rawImagePosY+10,pen)
          
      self.ui.orgView.setScene(self.scene)
  
  def EdgeJumpShowImage(self,value):
      self.edgeJump = int(value)
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def MaxscaleShowImage(self,value):
      self.scale_max = (value+1)/100
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
      self.ui.text_maxscale.setText("Max  "+str(value+1)+"  %")

  def MinscaleShowImage(self,value):
      self.scale_min = (value)/100
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
      self.ui.text_minscale.setText("Min  "+str(value)+"  %")

  def SliderShowImage(self,value):
      self.currentSliderStep = value - 1
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
      self.ui.current_img.setText(str(value))

  def SelectShowImage(self):
      self.currentSliderStep = int(self.ui.current_img.text()) - 1
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def SelectPoint(self):
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
      self.selectpointPress = True
      self.ui.bin.setEnabled(True)

  def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.ui.orgView and self.selectpointPress == True):
            self.rawImagePos = event.pos()
            self.rawImagePosX = self.rawImagePos.x()
	    self.rawImagePosY = self.rawImagePos.y()
            print('rawImagePos: (%d, %d)' % (self.rawImagePosX/379*1024, self.rawImagePosY/379*1024))
	    self.ui.x_cord.setText(str(int(self.rawImagePosX/379*1024)))
            self.ui.y_cord.setText(str(int(self.rawImagePosY/379*1024)))
            self.selectpointPress = False
	    QtGui.QApplication.restoreOverrideCursor()
            self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
        return QtGui.QWidget.eventFilter(self, source, event)
  
  def GetXCord(self):
      self.rawImagePosX = int(self.ui.x_cord.text())/1024*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def GetYCord(self):
      self.rawImagePosY = int(self.ui.y_cord.text())/1024*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def GetBin(self):
      self.bin = int(self.ui.bin.text())/1024*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def PlotSpectrum(self):
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
      items = self.ui.listWidget.selectedItems()
      x=[]
      for i in range(len(items)):
          x.append(str(self.ui.listWidget.selectedItems()[i].text()))
      print x
      self.figure = plt.figure(num=None, figsize=(5, 2), dpi=100, facecolor='w', edgecolor='k')
      self.canvas = FigureCanvas(self.figure)
      self.scene2 = QGraphicsScene(self)
      self.scene2.addWidget(self.canvas)
      self.ui.plotView.setScene(self.scene2)
      self.ax = self.figure.add_subplot(111)
      X = self.rawImagePosX
      Y = self.rawImagePosY
      print(self.scale_image_stack.shape)
      if 'Raw Spectrum (ROI) "*"' in x:
          if self.scale_image_stack == '':
              QtGui.QMessageBox.information(self, "Empty File","Please load and show file.")
              return
          if (self.rawImagePosX == '') or (self.rawImagePosY == ''):
              QtGui.QMessageBox.information(self, "No ROI","Please select a point.")
              return
          
          if self.bin > 1 :
              data = -np.log(self.scale_image_stack[(X-self.bin/2):(X+self.bin/2+1),(Y-self.bin/2):(Y+self.bin/2+1),0:self.iev])
	      self.mean_data = np.mean(np.mean(data, axis=0), axis=0)
              #print(data.shape,self.mean_data.shape)
              self.ax.plot(self.ev,self.mean_data, '*-', color="c")
          else:
              self.mean_data = -np.log(self.scale_image_stack[X,Y,0:self.iev])
              #print(self.ev,mean_data)
	      self.ax.plot(self.ev, self.mean_data, '*-', color="c")
              #print(self.ev,mean_data.shape)
      if 'Raw Bulk Spectrum "o"' in x:
          if self.scale_image_stack == '':
              QtGui.QMessageBox.information(self, "Empty File","Please load and show file.")
              return
	  data = -np.log(self.scale_image_stack[:,:,0:self.iev])
	  self.raw_bulk_data = np.mean(np.mean(data, axis=0), axis=0)
          #print(data.shape,mean_data.shape)
          self.ax.plot(self.ev,self.raw_bulk_data, 'o-', color="m")
      if 'Reference 1 "red -"' in x:
          if self.ref1 == '':
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 1.")
              return
          self.ax.plot(self.ev,self.ref1, '-', color="r")
      if 'Reference 2 "green -"' in x:
          if self.ref2 == '':
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 2.")
              return
          self.ax.plot(self.ev,self.ref2, '-', color="g")
      if 'Reference 3 "blue -"' in x:
          if self.ref3 == '':
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 3.")
              return
          self.ax.plot(self.ev,self.ref3, '-', color="blue")
      self.ax.annotate('Energy (eV)', xy=(-1, 0.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',
                fontsize=10)
      self.ax.annotate('Normalized ut', xy=(-325, 120), xycoords='axes points',horizontalalignment='left', verticalalignment='bottom',fontsize=10)
      self.canvas.draw()
      QtGui.QApplication.restoreOverrideCursor()
      self.ui.select_method.setEnabled(True)
      self.ui.smooth_pts.setEnabled(True)

  def SelectMethod(self):
      if str(self.ui.select_method.currentText()) == 'base line norm':
          self.ui.set_raw_bkg.setEnabled(False)
          self.ui.fit_base_line.setEnabled(True)
	  self.ui.base_line_zero.setEnabled(True)
          self.ui.check_select_zero.setEnabled(True)
          self.ui.smooth_pts.setEnabled(True)
	  self.ui.default_scaling.setEnabled(True)
	  self.ui.default_scaling.setChecked(True)
          self.ui.pre_start.setEnabled(False)
          self.ui.pre_end.setEnabled(False)
	  self.ui.post_start.setEnabled(False)
          self.ui.post_end.setEnabled(False)
          self.ui.edge_start.setEnabled(False)
	  self.ui.edge_end.setEnabled(False)
          
      elif str(self.ui.select_method.currentText()) == 'raw background norm':
          self.ui.set_raw_bkg.setEnabled(True)
          self.ui.fit_base_line.setEnabled(False)
	  self.ui.base_line_zero.setEnabled(False)
          self.ui.check_select_zero.setEnabled(False)
          self.ui.smooth_pts.setEnabled(True)
	  self.ui.default_scaling.setEnabled(True)
	  self.ui.default_scaling.setChecked(True)
          self.ui.pre_start.setEnabled(False)
          self.ui.pre_end.setEnabled(False)
	  self.ui.post_start.setEnabled(False)
          self.ui.post_end.setEnabled(False)
          self.ui.edge_start.setEnabled(False)
	  self.ui.edge_end.setEnabled(False)
          
      elif str(self.ui.select_method.currentText()) == 'pre/post edge norm':
	  self.ui.set_raw_bkg.setEnabled(False)
          self.ui.fit_base_line.setEnabled(False)
	  self.ui.base_line_zero.setEnabled(False)
          self.ui.check_select_zero.setEnabled(False)
          self.ui.smooth_pts.setEnabled(True)
	  self.ui.default_scaling.setEnabled(True)
	  self.ui.default_scaling.setChecked(False)
          self.ui.pre_start.setEnabled(True)
          self.ui.pre_end.setEnabled(True)
	  self.ui.post_start.setEnabled(True)
          self.ui.post_end.setEnabled(True)
          self.ui.edge_start.setEnabled(True)
	  self.ui.edge_end.setEnabled(True)
          
      else:
	  self.ui.set_raw_bkg.setEnabled(False)
          self.ui.fit_base_line.setEnabled(False)
	  self.ui.base_line_zero.setEnabled(False)
          self.ui.check_select_zero.setEnabled(False)
          self.ui.smooth_pts.setEnabled(False)
	  self.ui.default_scaling.setEnabled(False)
          self.ui.default_scaling.setChecked(False)
          self.ui.pre_start.setEnabled(False)
          self.ui.pre_end.setEnabled(False)
	  self.ui.post_start.setEnabled(False)
          self.ui.post_end.setEnabled(False)
          self.ui.edge_start.setEnabled(False)
	  self.ui.edge_end.setEnabled(False)

  def SetRawBkg(self):
      if self.mean_data == '':
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Spectrum of ROI First!")
          return
      self.RawBkg = self.mean_data
      QtGui.QMessageBox.information(self, "Notice","Current Raw Spectrum (ROI) was set as Baseline!")

  def FitBaseLine(self):
      if self.mean_data == '':
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Spectrum of ROI First!")
          return
      base = []
      base = np.polyfit(self.ev, self.mean_data, 1)
      print(base)
      self.baseline = base[0]*self.ev + base[1]
      print(self.baseline)
      self.ax.plot(self.ev,self.baseline, '-', color="c")
      self.canvas.draw()
      QtGui.QMessageBox.information(self, "Notice","Current Fittend Raw Spectrum (ROI) was set as Baseline!")

  def BaseLineZero(self):
      self.baseline = np.zeros(self.iev, dtype=np.int)
      self.ax.set_ylim([-0.1,1.5])
      self.ax.plot(self.ev,self.baseline, '-', color="black")
      self.canvas.draw()
  
  def DefaultScaling(self, state):
      if state == QtCore.Qt.Checked:
          self.ui.pre_start.setEnabled(False)
          self.ui.pre_end.setEnabled(False)
	  self.ui.post_start.setEnabled(False)
          self.ui.post_end.setEnabled(False)
          self.ui.edge_start.setEnabled(False)
	  self.ui.edge_end.setEnabled(False)
	  self.ui.pre_plot.setEnabled(False)
	  self.ui.post_plot.setEnabled(False)
	  self.ui.edge_plot.setEnabled(False)

      else:
          if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
	      self.ui.pre_start.setEnabled(True)
              self.ui.pre_end.setEnabled(True)
	      self.ui.post_start.setEnabled(True)
              self.ui.post_end.setEnabled(True)
              self.ui.edge_start.setEnabled(True)
	      self.ui.edge_end.setEnabled(True)
	  elif (str(self.ui.select_method.currentText()) == 'base line norm') or (str(self.ui.select_method.currentText()) == 'raw background norm'):
	      self.ui.pre_start.setEnabled(True)
              self.ui.pre_end.setEnabled(True)
	      self.ui.post_start.setEnabled(True)
              self.ui.post_end.setEnabled(True)
              self.ui.edge_start.setEnabled(False)
	      self.ui.edge_end.setEnabled(False)
	   
  def PreStart(self,value):
      self.preStart = int(value)
      self.ui.text_pre_start.setText(str(self.preStart))

  def PreEnd(self,value):
      self.preEnd = int(value)
      self.ui.text_pre_end.setText(str(self.preEnd))
      if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
          self.ui.pre_plot.setEnabled(True)

  def PostStart(self,value):
      self.postStart = int(value)
      self.ui.text_post_start.setText(str(self.postStart))

  def PostEnd(self,value):
      self.postEnd = int(value)
      self.ui.text_post_end.setText(str(self.postEnd))
      if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
          self.ui.post_plot.setEnabled(True)

  def EdgeStart(self,value):
      self.edgeStart = int(value)
      self.ui.text_edge_start.setText(str(self.edgeStart))

  def EdgeEnd(self,value):
      self.edgeEnd = int(value)
      self.ui.text_edge_end.setText(str(self.edgeEnd))
      if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
          self.ui.edge_plot.setEnabled(True)

  def PrePlot(self):
  def PostPlot(self):
  def EdgePlot(self):

      #if self.ui.check_select_zero.isChecked:
      #QtGui.QMessageBox.information(self, "Notice","Zero was set as Baseline!")


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  app.installEventFilter(myapp)
  sys.exit(app.exec_())

        
            
            
