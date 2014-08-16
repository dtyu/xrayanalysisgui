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
import subprocess
from fitting import brute_force_2ref, brute_force_3ref, least_square_3ref, least_square_2ref, NNLS_3ref, NNLS_2ref
from time import time

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
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
    #'Binning' callback
    self.ui.smooth_pts.textChanged.connect(self.GetSmooth)

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

    #'Start Normalize' callback
    QtCore.QObject.connect(self.ui.norm_spec, QtCore.SIGNAL('clicked()'), self.StartNormalize)
    #'Export Spectrum' callback
    QtCore.QObject.connect(self.ui.save_spectrum, QtCore.SIGNAL('clicked()'), self.SaveSpectrum)
    #'Save Spectrum Figure' callback
    QtCore.QObject.connect(self.ui.save_spectrum_fig, QtCore.SIGNAL('clicked()'), self.SaveSpecFig)
    #'Export to Athena' callback
    QtCore.QObject.connect(self.ui.athena, QtCore.SIGNAL('clicked()'), self.ExportAthena)

    #'Fitting_start' callback
    self.ui.fit_start.valueChanged.connect(self.FitStart)
    #'Fitting_end' callback
    self.ui.fit_end.valueChanged.connect(self.FitEnd)
    #'Resolution' callback
    self.ui.resolution.textChanged.connect(self.GetResolution)
    #'Restart' callback
    QtCore.QObject.connect(self.ui.restart, QtCore.SIGNAL('clicked()'), self.Restart)
    #'Start Fit' callback
    QtCore.QObject.connect(self.ui.fitting, QtCore.SIGNAL('clicked()'), self.StartFit)
    #'R-value Max' callback
    self.ui.Rmax.textChanged.connect(self.GetRmax)
    #'update image' callback
    QtCore.QObject.connect(self.ui.update_image, QtCore.SIGNAL('clicked()'), self.UpdateImage)
    #'Save fitting result' callback
    QtCore.QObject.connect(self.ui.save_fitted, QtCore.SIGNAL('clicked()'), self.SaveFitted)
    #'Fitting Method:' callback
    self.ui.fitting_method.activated.connect(self.FittingMethod)

    self.ui.listWidget.addItem("Raw Spectrum (ROI) 'cyan *'")
    self.ui.listWidget.addItem("Normalized Spectrum (ROI) 'magenta *'")
    self.ui.listWidget.addItem("Raw Bulk Spectrum 'cyan o'")
    self.ui.listWidget.addItem("Normalized Bulk Spectrum 'magenta o'")
    self.ui.listWidget.addItem("Fitted Results (ROI)")
    self.ui.listWidget.addItem("Reference 1 'red -'")
    self.ui.listWidget.addItem("Reference 2 'green -'")
    self.ui.listWidget.addItem("Reference 3 'blue -'")

    self.ui.select_method.addItems(['select one from below :','base line norm','raw background norm','pre/post edge norm'])
    self.ui.fitting_method.addItems(['select one:','brute force','Least Square','NNLS'])
    ############################
    self.scale_max = 1.00
    self.scale_min = 0.00
    self.currentSliderStep = 0
    self.selectpointPress = False
    self.bin = 1
    self.smooth = 1
    self.rawImagePosX = None
    self.rawImagePosY = None
    self.ref1 = None
    self.ref2 = None
    self.ref3 = None
    self.edgeJump = -100
    self.prePress = 0
    self.postPress = 0
    self.edgePress = 0
    self.preStart = None
    self.preEnd = None
    self.postStart = None
    self.postEnd = None
    self.edgeStart = None
    self.edgeEnd = None
    self.x = None
    self.fitStart = None
    self.fitEnd = None
    self.filter_image = None
    self.rmax = 100 
    self.reso = None

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
    self.n_rows = self.stk_sam.n_rows
    self.n_cols = self.stk_sam.n_cols
    #calculate scaleimg
    self.sam_image_stack = self.stk_sam.absdata.copy() 
    self.bkg_image_stack = self.stk_bkg.absdata.copy()
    self.scale_image_stack = np.true_divide(self.sam_image_stack,self.bkg_image_stack)  
    ##self.sam_image_stack = None
    ##self.bkg_image_stack = None
    ##self.stk_sam = None
    ##self.stk_bkg = None
    ##self.anlz_sam = None
    ##self.anlz_bkg = None
    self.log_image_stack = -np.log(self.scale_image_stack[:,:,0:self.iev])
    self.raw_bulk = np.mean(np.mean(self.log_image_stack, axis=0), axis=0)
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


  def ShowImage(self,currentSliderStep,scale_min,scale_max,rawImagePosX = None,rawImagePosY = None,bin = None,edgeJump = None):
      self.orgImage = self.scale_image_stack[:,:,int(currentSliderStep)]
      self.currentImage = (self.orgImage - scale_min) / (scale_max - scale_min)
      self.currentImage[self.orgImage >= (scale_max)] = 1
      self.currentImage[self.orgImage <= (scale_min)] = 0
      
      self.edgeJump = edgeJump
      self.edgeDiff = np.array((255*self.scale_image_stack[:,:,0]), dtype=int) - np.array((255*self.scale_image_stack[:,:,int(self.iev - 1)]), dtype=int)
      self.filter_image = np.ones((self.n_rows, self.n_cols), dtype=np.int)
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
      #bin = bin/1024*379
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
      self.ui.slider_img.setValue(int(self.ui.current_img.text()))

  def SelectPoint(self):
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
      self.selectpointPress = True
      self.ui.bin.setEnabled(True)

  def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.ui.orgView and self.selectpointPress == True):
            self.rawImagePos = event.pos()
            self.rawImagePosX = self.rawImagePos.x()
	    self.rawImagePosY = self.rawImagePos.y()
            print('rawImagePos: (%d, %d)' % (self.rawImagePosX/379*self.n_rows, self.rawImagePosY/379*self.n_cols))
	    self.ui.x_cord.setText(str(int(self.rawImagePosX/379*self.n_rows)))
            self.ui.y_cord.setText(str(int(self.rawImagePosY/379*self.n_cols)))
            self.selectpointPress = False
	    QtGui.QApplication.restoreOverrideCursor()
            self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)
	if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.ui.fittingView and self.selectpointPress == True):
            self.fitImagePos = event.pos()
            self.fitImagePosX = self.fitImagePos.x()
	    self.fitImagePosY = self.fitImagePos.y()
            print('fitImagePos: (%d, %d)' % (self.fitImagePosX/329*self.n_rows, self.fitImagePosY/329*self.n_cols))
	    self.ui.x_cord.setText(str(int(self.fitImagePosX/329*self.n_rows)))
            self.ui.y_cord.setText(str(int(self.fitImagePosY/329*self.n_cols)))
            self.selectpointPress = False
	    QtGui.QApplication.restoreOverrideCursor()
        return QtGui.QWidget.eventFilter(self, source, event)
  
  def GetXCord(self):
      self.rawImagePosX = int(self.ui.x_cord.text())/self.n_rows*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def GetYCord(self):
      self.rawImagePosY = int(self.ui.y_cord.text())/self.n_cols*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def GetBin(self):
      self.bin = int(self.ui.bin.text())/self.n_rows*379
      self.ShowImage(self.currentSliderStep,self.scale_min,self.scale_max,self.rawImagePosX,self.rawImagePosY,self.bin,self.edgeJump)

  def ShowPlot(self,x,preStart=None,preEnd=None,postStart=None,postEnd=None,edgeStart=None,edgeEnd=None,prePress=None,postPress=None,edgePress=None,fitStart=None,fitEnd=None):
      self.figure = plt.figure(num=None, figsize=(5, 2), dpi=100, facecolor='w', edgecolor='k')
      self.canvas = FigureCanvas(self.figure)
      self.scene2 = QGraphicsScene(self)
      self.scene2.addWidget(self.canvas)
      self.ui.plotView.setScene(self.scene2)
      self.ax = self.figure.add_subplot(111)
      #X = self.rawImagePosX/379*1024
      #Y = self.rawImagePosY/379*1024
      X = int(self.ui.x_cord.text())
      Y = int(self.ui.y_cord.text())
      if "Fitted Results (ROI)" in x:
          if self.fRGB == None or self.index == None or self.min_R == None:
              QtGui.QMessageBox.information(self, "No Fitting","Please normalize and fit file first.")
              return
	  ff = np.empty(3,dtype=np.float16)
          if self.bin > 1 :
	      for i in range(int(self.bin/2)):
	          for j in range(int(self.bin/2)):
                      ff_all[i,j,:] = self.fRGB[:,int(self.index[(X-i):(X+i),(Y-j):(Y+j)])]
                      R_all[i,j] = self.min_R[X,Y]
              ff = np.mean(np.mean(ff_all, axis=0), axis=0)
              R = np.amax(np.amax(R_all, axis=0), axis=0)
	  else:
              ff = self.fRGB[0][int(self.index[X,Y])],self.fRGB[1][int(self.index[X,Y])],self.fRGB[2][int(self.index[X,Y])]
              R = self.min_R[X,Y]
          self.fittedcurve = np.empty(self.iev,dtype=np.float16)
	  if self.ref3 == None:
              self.fittedcurve = ff[0]*self.ref1 + ff[1]*self.ref2
	      self.ax.plot(self.ev, self.fittedcurve, '--', color="r", linewidth=4)
	      self.ax.annotate('Ref1 : %(a)i%%' % {"a":ff[0]*100},xy=(-3, 40.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
              self.ax.annotate('Ref2 : %(b)i%%' % {"b":ff[1]*100},xy=(-2.5, 30.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
          else:
              self.fittedcurve = np.add(np.multiply(ff[0],self.ref1),np.add(np.multiply(ff[1],self.ref2),np.multiply(ff[2],self.ref3)))
              print ff,ff[0],self.fittedcurve
	      self.ax.plot(self.ev, self.fittedcurve, '--', color="r", linewidth=4)
              self.ax.annotate('Ref1 : %(a)i%%' % {"a":ff[0]*100},xy=(-3, 40.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
              self.ax.annotate('Ref2 : %(b)i%%' % {"b":ff[1]*100},xy=(-2.5, 30.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
              self.ax.annotate('Ref3 : %(c)i%%' % {"c":ff[2]*100},xy=(-2, 20.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
              self.ax.annotate('R value = %(d)f' % {"d":R},xy=(-1.5, 10.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)


      if "Raw Spectrum (ROI) 'cyan *'" in x:
          if self.scale_image_stack == None:
              QtGui.QMessageBox.information(self, "Empty File","Please load and show file.")
              return
          if (self.rawImagePosX == None) or (self.rawImagePosY == None):
              QtGui.QMessageBox.information(self, "No ROI","Please select a point.")
              return
          if self.bin > 1 :
              data = self.log_image_stack[(X-self.bin/2):(X+self.bin/2+1),(Y-self.bin/2):(Y+self.bin/2+1),0:self.iev]
              #data = None
	      self.raw_roi = np.mean(np.mean(data, axis=0), axis=0)
              self.ax.plot(self.ev,self.raw_roi, '*-', color="c")
          else:
              self.raw_roi = self.log_image_stack[X,Y,0:self.iev]
	      self.ax.plot(self.ev, self.raw_roi, '*-', color="c")
      if "Raw Bulk Spectrum 'cyan o'" in x:
          if self.raw_bulk == None:
              QtGui.QMessageBox.information(self, "Empty File","Please load and show file.")
              return
          self.ax.plot(self.ev,self.raw_bulk, 'o-', color="c")
      if "Reference 1 'red -'" in x:
          if self.ref1 == None:
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 1.")
              return
          self.ax.plot(self.ev,self.ref1, '-', color="r")
      if "Reference 2 'green -'" in x:
          if self.ref2 == None:
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 2.")
              return
          self.ax.plot(self.ev,self.ref2, '-', color="g")
      if "Reference 3 'blue -'" in x:
          if self.ref3 == None:
              QtGui.QMessageBox.information(self, "Empty File","Please load Reference 3.")
              return
          self.ax.plot(self.ev,self.ref3, '-', color="blue")
      if "Normalized Bulk Spectrum 'magenta o'" in x:
          if self.norm_bulk == None:
              QtGui.QMessageBox.information(self, "Empty File","Please normalize the data first.")
              return
          self.ax.plot(self.ev,self.norm_bulk, 'o-', color="m")
      if "Normalized Spectrum (ROI) 'magenta *'" in x:
          if self.norm_image_stack == None:
              QtGui.QMessageBox.information(self, "Empty File","Please normalize the data first.")
              return
          if self.bin > 1 :
              data = self.norm_image_stack[(X-self.bin/2):(X+self.bin/2+1),(Y-self.bin/2):(Y+self.bin/2+1),0:self.iev]
              #data = None
	      self.norm_roi = np.mean(np.mean(data, axis=0), axis=0)
              self.ax.plot(self.ev,self.norm_roi, '*-', color="c")
          else:
	      self.norm_roi = self.norm_image_stack[X,Y,0:self.iev]
	      self.ax.plot(self.ev, self.norm_roi, '*-', color="m")

      if (preStart!=None)and(preEnd!=None):      
          plt.axvline(x=self.ev[preStart-1], ymin=0, ymax=1, linewidth=1, color='k')
          plt.axvline(x=self.ev[preEnd-1], ymin=0, ymax=1, linewidth=1, color='k')
      if (postStart!=None)and(postEnd!=None):
	  plt.axvline(x=self.ev[postStart-1], ymin=0, ymax=1, linewidth=1, color='k')
          plt.axvline(x=self.ev[postEnd-1], ymin=0, ymax=1, linewidth=1, color='k')
      if (edgeStart!=None)and(edgeEnd!=None):
          plt.axvline(x=self.ev[edgeStart-1], ymin=0, ymax=1, linewidth=1, linestyle='--', color='k')
          plt.axvline(x=self.ev[edgeEnd-1], ymin=0, ymax=1, linewidth=1, linestyle='--', color='k')

      if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
          if prePress == 1:
              base_pre = []
              base_pre = np.polyfit(self.ev[preStart-1:preEnd],self.raw_bulk[preStart-1:preEnd],1)
              self.preLine = base_pre[0]*self.ev[preStart-1:preEnd] + base_pre[1]
              self.ax.plot(self.ev[preStart-1:preEnd],self.preLine, '-', color="k")
          if postPress == 1:
              base_post = []
              base_post = np.polyfit(self.ev[postStart-1:postEnd], self.raw_bulk[postStart-1:postEnd], 1)
              self.postLine = base_post[0]*self.ev[postStart-1:postEnd] + base_post[1]
              self.ax.plot(self.ev[postStart-1:postEnd],self.postLine, '-', color="k")
	  if edgePress == 1:
              base_edge = []
              base_edge = np.polyfit(self.ev[edgeStart-1:edgeEnd], self.raw_bulk[edgeStart-1:edgeEnd], 1)
              self.postLine = base_edge[0]*self.ev[edgeStart-1:edgeEnd] + base_edge[1]
              self.ax.plot(self.ev[edgeStart-1:edgeEnd],self.postLine, '-', color="k")
      if fitStart!=None:
          plt.axvline(x=self.ev[fitStart-1], ymin=0, ymax=1, linewidth=1, color='r')
      if fitEnd!=None:
          plt.axvline(x=self.ev[fitEnd-1], ymin=0, ymax=1, linewidth=1, color='r')

      self.ax.annotate('Energy (eV)', xy=(-1, 0.8), xycoords='axes points',horizontalalignment='right', verticalalignment='bottom',fontsize=10)
      self.ax.annotate('Normalized ut', xy=(-325, 120), xycoords='axes points',horizontalalignment='left', verticalalignment='bottom',fontsize=10)
      self.canvas.draw()
      

  def PlotSpectrum(self):
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
      items = self.ui.listWidget.selectedItems()
      self.x=[]
      for i in range(len(items)):
          self.x.append(str(self.ui.listWidget.selectedItems()[i].text()))
      print self.x
      self.ShowPlot(self.x)
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
      if self.raw_roi == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Spectrum of ROI First!")
          return
      self.RawBkg = self.raw_roi
      QtGui.QMessageBox.information(self, "Notice","Current Raw Spectrum (ROI) was set as Baseline!")

  def FitBaseLine(self):
      if self.raw_roi == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Spectrum of ROI First!")
          return
      base = []
      base = np.polyfit(self.ev, self.raw_roi, 1)
      print(base)
      self.baseline = base[0]*self.ev + base[1]
      self.ax.plot(self.ev,self.baseline, '-', color="c")
      self.canvas.draw()
      QtGui.QMessageBox.information(self, "Notice","Current Fittend Raw Spectrum (ROI) was set as Baseline!")

  def BaseLineZero(self):
      self.baseline = np.zeros(self.iev, dtype=np.int)
      self.ax.set_ylim([-0.2,1.5])
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
          self.defaultState = 1
      else:
          self.defaultState = 0
          if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
	      self.ui.pre_start.setEnabled(True)
              self.ui.pre_end.setEnabled(True)
	      self.ui.post_start.setEnabled(True)
              self.ui.post_end.setEnabled(True)
              self.ui.edge_start.setEnabled(True)
	      self.ui.edge_end.setEnabled(True)
              self.ui.pre_plot.setEnabled(True)
	      self.ui.post_plot.setEnabled(True)
	      self.ui.edge_plot.setEnabled(True)
	  elif (str(self.ui.select_method.currentText()) == 'base line norm') or (str(self.ui.select_method.currentText()) == 'raw background norm'):
	      self.ui.pre_start.setEnabled(True)
              self.ui.pre_end.setEnabled(True)
	      self.ui.post_start.setEnabled(True)
              self.ui.post_end.setEnabled(True)
              self.ui.edge_start.setEnabled(False)
	      self.ui.edge_end.setEnabled(False)
              self.ui.pre_plot.setEnabled(True)
	      self.ui.post_plot.setEnabled(True)
	      self.ui.edge_plot.setEnabled(False)
	   
  def PreStart(self,value):
      self.preStart = int(value)
      self.ui.text_pre_start.setText(str(self.preStart))

  def PreEnd(self,value):
      self.preEnd = int(value)
      self.ui.text_pre_end.setText(str(self.preEnd))
      self.ui.pre_plot.setEnabled(True)

  def PostStart(self,value):
      self.postStart = int(value)
      self.ui.text_post_start.setText(str(self.postStart))

  def PostEnd(self,value):
      self.postEnd = int(value)
      self.ui.text_post_end.setText(str(self.postEnd))
      self.ui.post_plot.setEnabled(True)

  def EdgeStart(self,value):
      self.edgeStart = int(value)
      self.ui.text_edge_start.setText(str(self.edgeStart))

  def EdgeEnd(self,value):
      self.edgeEnd = int(value)
      self.ui.text_edge_end.setText(str(self.edgeEnd))
      self.ui.edge_plot.setEnabled(True)

  def PrePlot(self):
      if self.raw_bulk == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Bulk Spectrum First!")
          return
      self.prePress = 1
      self.ShowPlot(self.x,self.preStart,self.preEnd,self.postStart,self.postEnd,self.edgeStart,self.edgeEnd,self.prePress,self.postPress,self.edgePress)

  def PostPlot(self):
      if self.raw_bulk == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Bulk Spectrum First!")
          return
      self.postPress = 1
      self.ShowPlot(self.x,self.preStart,self.preEnd,self.postStart,self.postEnd,self.edgeStart,self.edgeEnd,self.prePress,self.postPress,self.edgePress)

  def EdgePlot(self):
      if self.raw_bulk == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Plot the Raw Bulk Spectrum First!")
          return
      self.edgePress = 1
      self.ShowPlot(self.x,self.preStart,self.preEnd,self.postStart,self.postEnd,self.edgeStart,self.edgeEnd,self.prePress,self.postPress,self.edgePress)

  def StartNormalize(self):
      if self.scale_image_stack == None:
          QtGui.QMessageBox.information(self, "Empty Data","Please Load the Raw Data First!")
          return
      #self.ui.XANESnormStatus.setText('status: running')
      self.norm_image_stack = np.empty((self.n_rows, self.n_cols, self.iev), dtype=np.float32)
      self.norm2_image_stack = np.empty((self.n_rows, self.n_cols, self.iev), dtype=np.float32)
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
      if str(self.ui.select_method.currentText()) == 'base line norm':
          if self.baseline == None:
              QtGui.QMessageBox.information(self, "Empty Baseline","Please Use 'Fit Base Line' or 'Base Line = 0' to Set the baseline First!")
              return
          if self.ui.check_select_zero.isChecked:
              self.baseline = np.zeros(self.iev, dtype=np.float32)
	  else:
              base = []
              base = np.polyfit(self.ev, self.raw_roi, 1)
              self.baseline = base[0]*self.ev + base[1]
	  data = self.log_image_stack 
          for i in range(int(data.shape[2])):
              data[:,:,i] = data[:,:,i] - self.baseline[i]
          print(data.shape)
          if self.defaultState == 1:
              scale_0 = np.mean(self.log_image_stack[:,:,0:4], axis=2)
              scale_1 = np.mean(self.log_image_stack[:,:,self.iev-5:self.iev-1], axis=2)
          else:
              scale_0 = np.mean(self.log_image_stack[:,:,self.preStart-1:self.preEnd-1], axis=2)
              scale_1 = np.mean(self.log_image_stack[:,:,self.postStart-1:self.postEnd-1], axis=2)
          print(scale_0)
          diff = scale_1-scale_0
          
          for i in range(int(data.shape[2])):
              self.norm2_image_stack[:,:,i] = data[:,:,i] - scale_0
              self.norm_image_stack[:,:,i] = (data[:,:,i] - scale_0)/diff
          print(self.norm_image_stack.shape)
          ##data = None
          self.norm_bulk = np.mean(np.mean(self.norm_image_stack, axis=0), axis=0)

      if str(self.ui.select_method.currentText()) == 'raw background norm':
          if self.raw_roi == None:
              QtGui.QMessageBox.information(self, "Empty Background","Please Select ROI and Plot to Set the Background First!")
              return
	  data = self.log_image_stack 
          for i in range(int(data.shape[2])):
              data[:,:,i] = data[:,:,i] - self.RawBkg[i]
          #print(data.shape)
          if self.defaultState == 1:
              scale_0 = np.mean(self.log_image_stack[:,:,0:4], axis=2)
              scale_1 = np.mean(self.log_image_stack[:,:,self.iev-5:self.iev-1], axis=2)
          else:
              scale_0 = np.mean(self.log_image_stack[:,:,self.preStart-1:self.preEnd-1], axis=2)
              scale_1 = np.mean(self.log_image_stack[:,:,self.postStart-1:self.postEnd-1], axis=2)
          #print(scale_0)
          diff = scale_1-scale_0
          #self.norm_image_stack = np.empty((self.n_rows, self.n_cols, self.iev), dtype=np.float32)
          for i in range(int(data.shape[2])):
              self.norm_image_stack[:,:,i] = (data[:,:,i] - scale_0)/diff
          print(self.norm_image_stack.shape)
          ##data = None
          self.norm_bulk = np.mean(np.mean(self.norm_image_stack, axis=0), axis=0)

      if str(self.ui.select_method.currentText()) == 'pre/post edge norm':
	  #self.norm_image_stack = np.empty((self.n_rows, self.n_cols, self.iev), dtype=np.float32)
          Post = []
          for i in range(int(self.log_image_stack.shape[0])):
              for j in range(int(self.log_image_stack.shape[1])):
		  if self.filter_image[i,j]:
		      spec = self.log_image_stack[i,j,:]
                      Post = np.polyfit(self.ev[self.postStart-1:self.postEnd],spec[self.postStart-1:self.postEnd],1)
                      midpoint = (self.edgeStart+self.edgeEnd)/2-1
                      postE0 = Post[0]*self.ev[midpoint]+Post[1]
	  	      self.norm_image_stack[i,j,:] = spec/postE0
	          else:
              	      self.norm_image_stack[i,j,:] = np.zeros(self.iev, dtype=np.float32)
	  self.norm_bulk = np.mean(np.mean(self.norm_image_stack, axis=0), axis=0)

      self.ui.XANESnormStatus.setText('status: complete')
      QtGui.QApplication.restoreOverrideCursor()
      #update widgets
      self.ui.fit_start.setEnabled(True)
      self.ui.fit_start.setMinimum(1)
      self.ui.fit_start.setMaximum(self.iev)
      self.ui.fit_end.setEnabled(True)
      self.ui.fit_end.setMinimum(1)
      self.ui.fit_end.setMaximum(self.iev)
      self.ui.bin_object.setEnabled(True)
      self.ui.smooth_object.setEnabled(True)
      

  def SaveSpectrum(self):
      if self.x == None:
          QtGui.QMessageBox.information(self, "Empty Selection","Please Select Data Type First!")
          return
      if "Raw Spectrum (ROI) 'cyan *'" in self.x:
          wildcard =  "TXT (*.txt)" 
      	  filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Raw ROI Spectrum', '', wildcard)
          f = open(filepath,'w')
          f.write('    Energy:               mut:\n')
	  for i in range(self.iev):
              f.write("%14.5f%14.4f\n"%(self.ev[i],self.raw_roi[i]))
          f.close()
      if "Normalized Spectrum (ROI) 'magenta *'" in self.x:
	  wildcard =  "TXT (*.txt)" 
      	  filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Normalized ROI Spectrum', '', wildcard)
          f = open(filepath,'w')
          f.write('    Energy:               mut:\n')
          for i in range(self.iev):
              f.write("%14.5f%14.4f\n"%(self.ev[i],self.norm_roi[i]))
          f.close()
      if "Raw Bulk Spectrum 'cyan o'" in self.x:
	  wildcard =  "TXT (*.txt)" 
      	  filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Raw Bulk Spectrum', '', wildcard)
          f = open(filepath,'w')
          f.write('    Energy:               mut:\n')
          for i in range(self.iev):
              f.write("%14.5f%14.4f\n"%(self.ev[i],self.raw_bulk[i]))
          f.close()
      if "Normalized Bulk Spectrum 'magenta o'" in self.x:
	  wildcard =  "TXT (*.txt)" 
      	  filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Normalized Bulk Spectrum', '', wildcard)
          f = open(filepath,'w')
          f.write('    Energy:               mut:\n')
          for i in range(self.iev):
              f.write("%14.5f%14.4f\n"%(self.ev[i],self.norm_bulk[i]))
          f.close()
      

  def SaveSpecFig(self):
      pixmap = QtGui.QPixmap(self)
      wildcard =  "TIFF (*.tiff)" 
      filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Spectrum Figure', '', wildcard)
      pixmap = QtGui.QPixmap.grabWidget(self.ui.plotView)
      pixmap.save(filepath)

  def ExportAthena(self):   
      ##self.scale_image_stack = None
      ##self.log_image_stack = None
      ##self.raw_bulk = None
      ##self.norm_image_stack = None
      ##self.norm_bulk = None
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
      
      X = self.rawImagePosX/379*1024
      Y = self.rawImagePosY/379*1024
      self.r_data = np.zeros(self.iev, dtype=np.int)
      if self.bin > 1 :
          sam_data = np.array(self.sam_image_stack[(X-self.bin/2):(X+self.bin/2+1),(Y-self.bin/2):(Y+self.bin/2+1),0:self.iev])          
          bkg_data = np.array(self.bkg_image_stack[(X-self.bin/2):(X+self.bin/2+1),(Y-self.bin/2):(Y+self.bin/2+1),0:self.iev])
          ##self.sam_image_stack = None
          ##self.bkg_image_stack = None
	  self.sam_data = np.mean(np.mean(sam_data, axis=0), axis=0)
          self.bkg_data = np.mean(np.mean(bkg_data, axis=0), axis=0)             
      else:
          self.sam_data = np.array(self.sam_image_stack[X,Y,0:self.iev])          
          self.bkg_data = np.array(self.bkg_image_stack[X,Y,0:self.iev])
	  ##self.sam_image_stack = None
          ##self.bkg_image_stack = None          

      wildcard =  "TXT (*.txt)" 
      filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Spectrum to Athena', '', wildcard)
      f = open(filepath,'w')
      f.write('    Energy:               I0            It            Ir\n')
      for i in range(self.iev):
          f.write("%14.5f%14.4f%14.4f%14.4f\n"%(self.ev[i],self.bkg_data[i],self.sam_data[i],self.r_data[i]))
      f.close()
      QtGui.QApplication.restoreOverrideCursor()

  def GetSmooth(self):
      self.smooth = int(self.ui.smooth_pts.text())

  def FitStart(self,value):
      self.fitStart = int(value)
      self.ui.text_fit_start.setText(str(self.fitStart))
      self.ShowPlot(self.x,self.preStart,self.preEnd,self.postStart,self.postEnd,self.edgeStart,self.edgeEnd,self.prePress,self.postPress,self.edgePress,self.fitStart,self.fitEnd)

  def FitEnd(self,value):
      self.fitEnd = int(value)
      self.ui.text_fit_end.setText(str(self.fitEnd))
      self.ShowPlot(self.x,self.preStart,self.preEnd,self.postStart,self.postEnd,self.edgeStart,self.edgeEnd,self.prePress,self.postPress,self.edgePress,self.fitStart,self.fitEnd)

  def GetResolution(self):
      self.reso = int(self.ui.resolution.text())

  def GetRmax(self):
      self.rmax = float(self.ui.Rmax.text())
      self.ui.update_image.setEnabled(True)

  def FittingMethod(self):
      self.ui.fitting.setEnabled(True)
      if str(self.ui.fitting_method.currentText()) == 'brute force':
          self.ui.resolution.setEnabled(True)

  def StartFit(self):
      QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
      if self.reso==None and str(self.ui.fitting_method.currentText()) == 'brute force':
          QtGui.QMessageBox.information(self, "Empty Resolution","Please Input Resolution First!")
          return
      if (self.fitStart==None) and (self.fitEnd==None):
          QtGui.QMessageBox.information(self, "Empty Fitting Range","Please Specify Fitting Range First!")
          return
      start = self.fitStart
      end = self.fitEnd
      if (self.ref1==None) and (self.ref2==None):
          QtGui.QMessageBox.information(self, "Empty Reference","Please Load 2-3 References First!")
          return
      if self.ui.bin_object.isChecked():
          if self.bin % 2 == 0:
              kernel_size=int(self.bin/2+1)
          else:
              kernel_size=int(self.bin/2)
          for i in range(self.iev):
              self.log_image_stack[:,:,i] = scipy.signal.medfilt2d(self.log_image_stack[:,:,i],kernel_size)
      if self.ui.smooth_object.isChecked():
          for i in range(self.n_rows):
	      for j in range(self.n_cols):
                  self.log_image_stack[i,j,:] = scipy.signal.medfilt(self.log_image_stack[i,j,:],kernel_size)

      t0 = time()
      if str(self.ui.fitting_method.currentText()) == 'brute force':
          if self.ref3 == None:
             self.min_R, self.index, self.fRGB = brute_force_2ref(self.ref1[start-1:end],self.ref2[start-1:end],self.norm_image_stack[:,:,start-1:end],self.reso)
          else:
             self.min_R, self.index, self.fRGB = brute_force_3ref(self.ref1[start-1:end],self.ref2[start-1:end],self.ref3[start-1:end],self.norm_image_stack[:,:,start-1:end],self.reso)
          self.ShowFittedImage(self.index,self.fRGB,self.rmax,self.filter_image,self.min_R)
      	  self.ui.status_expXANES.setText('status: complete')
          t1 = time()
          print t1 - t0
          self.ui.Rmax.setEnabled(True)
          self.ui.save_fitted.setEnabled(True)
          QtGui.QApplication.restoreOverrideCursor()

      if str(self.ui.fitting_method.currentText()) == 'Least Square':
	  if self.ref3 == None:
             self.min_R, self.fittedresult = least_square_2ref(self.ref1[start-1:end],self.ref2[start-1:end],self.norm_image_stack[:,:,start-1:end])
          else:
             self.min_R, self.fittedresult = least_square_3ref(self.ref1[start-1:end],self.ref2[start-1:end],self.ref3[start-1:end],self.norm_image_stack[:,:,start-1:end])
          self.ShowFittedImage_new(self.fittedresult,self.rmax,self.filter_image,self.min_R)
      	  self.ui.status_expXANES.setText('status: complete')
          t1 = time()
          print t1 - t0
          self.ui.Rmax.setEnabled(True)
          self.ui.save_fitted.setEnabled(True)
          QtGui.QApplication.restoreOverrideCursor()

      if str(self.ui.fitting_method.currentText()) == 'NNLS':
	  if self.ref3 == None:
             self.min_R, self.fittedresult = NNLS_2ref(self.ref1[start-1:end],self.ref2[start-1:end],self.norm2_image_stack[:,:,start-1:end])
          else:
             self.min_R, self.fittedresult = NNLS_3ref(self.ref1[start-1:end],self.ref2[start-1:end],self.ref3[start-1:end],self.norm2_image_stack[:,:,start-1:end])
          self.ShowFittedImage_new(self.fittedresult,self.rmax,self.filter_image,self.min_R)
      	  self.ui.status_expXANES.setText('status: complete')
          t1 = time()
          print t1 - t0
          self.ui.Rmax.setEnabled(True)
          self.ui.save_fitted.setEnabled(True)
          QtGui.QApplication.restoreOverrideCursor()

      
  def ShowFittedImage_new(self,fittedresult,rmax,filter_image,min_R):
      self.fittedresult[filter_image == 0] = [0,0,0]
      self.fittedresult[min_R >= rmax] = [0,0,0]
      image = qimage2ndarray.numpy2qimage(np.array(255*self.fittedresult, dtype=np.float32))
      pixmap = QtGui.QPixmap.fromImage(image)
      pixmap = pixmap.scaled(329, 329,QtCore.Qt.IgnoreAspectRatio)
      self.rotated_pixmap = pixmap.transformed(QtGui.QMatrix().rotate(-90),Qt.SmoothTransformation)
      #pixmap = QtGui.QPixmap.fromImage(ImageQt(scipy.misc.toimage(image)))
      self.scene3 = QGraphicsScene(self)
      item = QGraphicsPixmapItem(self.rotated_pixmap)
      self.scene3.addItem(item)
      self.ui.fittingView.setScene(self.scene3)

  def ShowFittedImage(self,index,fRGB,rmax,filter_image,min_R):
      self.fittedresult = np.empty((self.n_rows,self.n_cols,3), dtype=np.float32)
      print self.fittedresult.shape
      for i in range(self.n_rows):
	  for j in range(self.n_cols):
	      for k in range(3):
                  self.fittedresult[i,j,k] = fRGB[k,int(index[i,j])]
      self.fittedresult[filter_image == 0] = [0,0,0]
      self.fittedresult[min_R >= rmax] = [0,0,0]
      image = qimage2ndarray.numpy2qimage(np.array(255*self.fittedresult, dtype=np.float32))
      pixmap = QtGui.QPixmap.fromImage(image)
      pixmap = pixmap.scaled(329, 329,QtCore.Qt.IgnoreAspectRatio)
      self.rotated_pixmap = pixmap.transformed(QtGui.QMatrix().rotate(-90),Qt.SmoothTransformation)
      #pixmap = QtGui.QPixmap.fromImage(ImageQt(scipy.misc.toimage(image)))
      self.scene3 = QGraphicsScene(self)
      item = QGraphicsPixmapItem(self.rotated_pixmap)
      self.scene3.addItem(item)
      self.ui.fittingView.setScene(self.scene3)

  def SaveFitted(self):
      self.fittedresult = np.rot90(self.fittedresult)
      wildcard =  "TIFF (*.tiff)" 
      filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Spectrum Figure', '', wildcard)
      filename =  os.path.basename(str(filepath))
      matplotlib.image.imsave(filename, self.fittedresult)

  def UpdateImage(self):
      self.ShowFittedImage(self.index,self.fRGB,self.rmax,self.filter_image,self.min_R)

  def Restart(self):
      self.close()
      subprocess.call("python" + " call_specify_XANES_files.py", shell=True)

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  app.installEventFilter(myapp)
  sys.exit(app.exec_())

        
            
            
