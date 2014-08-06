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


class common:
    def __init__(self):
        self.stack_loaded = 0
        #self.path = ''
        #self.filename = ''
        #self.font = ''

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

  def GetSamFile(self):
    if self.ui.samTxrm.isChecked() == True:
        wildcard =  "TXRM (*.txrm)" 
        self.window().LoadFile(wildcard)
        self.ui.text_XANES_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:    " +self.filename)
        self.sam_directory = self.directory
        self.sam_filename = self.filename
        self.sam_filepath = self.filepath 
    if self.ui.samXrm.isChecked() == True:
        wildcard =  "XRM (*.xrm)" 
        self.window().LoadFiles(wildcard)
        self.ui.text_XANES_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:    " +self.filename_first+ "\n" +self.filename_last)
        self.sam_directory = self.directory
        self.sam_filepaths = self.filepaths

  def GetBkgFile(self):
    if self.ui.bkgTxrm.isChecked() == True:
        wildcard =  "TXRM (*.txrm)" 
        self.window().LoadFile(wildcard)
        self.ui.text_BKG_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:     " +self.filename)
        self.bkg_directory = self.directory
        self.bkg_filename = self.filename
        self.bkg_filepath = self.filepath 
    if self.ui.bkgXrm.isChecked() == True:
        wildcard =  "XRM (*.xrm)" 
        self.window().LoadFiles(wildcard)
        self.ui.text_BKG_filename.setText("Filepath:     " +self.directory+ "\n" +"Filename:     " +self.filename_first+ "\n" +self.filename_last)
        self.bkg_directory = self.directory
        self.bkg_filepaths = self.filepaths

  def LoadFile(self, wildcard = ''):
    filepath = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', wildcard)
    filepath = str(filepath)
    if filepath == '':
      return      
    self.directory =  os.path.dirname(str(filepath))
    self.filename =  os.path.basename(str(filepath))
    self.filepath = filepath

  def LoadFiles(self, wildcard = ''):
    filepaths = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', '', wildcard)
    if filepaths == '':
      return      
    self.directory = os.path.dirname(str(filepaths[0]))
    self.filename_first = os.path.basename(str(filepaths[0]))
    self.filename_last = os.path.basename(str(filepaths[-1]))
    self.filepaths = filepaths

  def GetRef1File(self, wildcard = ''):
    wildcard =  "TXT (*.txt)" 
    self.window().LoadFile(wildcard)
    self.ref1 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref1.append(float(line.split()[1]))
    #print(ref1)
    self.ui.ref1name.setText(self.filename)

  def GetRef2File(self, wildcard = ''):
    wildcard = "TXT (*.txt)" 
    self.window().LoadFile(wildcard)
    self.ref2 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref2.append(float(line.split()[1]))
    self.ui.ref2name.setText(self.filename)

  def GetRef3File(self, wildcard = ''):
    wildcard = "TXT (*.txt)" 
    self.window().LoadFile(wildcard)
    self.ref3 = []
    with open (self.filepath, "r") as myfile:
        myfile.readline()
        for line in myfile:
            self.ref3.append(float(line.split()[1]))
    self.ui.ref3name.setText(self.filename)

  def LoadShowImage(self):
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
        self.stk_sam.read_txrm(self.sam_filepath)        
                
    if self.ui.samXrm.isChecked() == True:              
        self.stk_sam.new_data()
        self.anlz_sam.delete_data()
        #self.sam_filelist = os.path.basename(str(self.sam_filepaths))
        self.stk_sam.read_xrm_list(self.sam_filepaths) 

    if self.ui.bkgTxrm.isChecked() == True:
        self.stk_bkg.new_data()
        self.anlz_bkg.delete_data() 
        self.stk_bkg.read_txrm(self.bkg_filepath)

    if self.ui.bkgXrm.isChecked() == True:
        self.stk_bkg.new_data()
        self.anlz_bkg.delete_data()
        #self.bkg_filelist = os.path.basename(str(self.bkg_filepaths))
        self.stk_bkg.read_xrm_list(self.bkg_filepaths)
 
    self.common.stack_loaded == 1

    #update image information
    self.iev = int(self.stk_sam.n_ev)
    x=self.stk_sam.n_cols
    y=self.stk_sam.n_rows
    z=self.iev  
    print(z)             
    self.ix = int(x/2)
    self.iy = int(y/2)
    
    #calculate scaleimg
    sam_image_stack = self.stk_sam.absdata.copy() 
    bkg_image_stack = self.stk_bkg.absdata.copy()
    self.scale_image_stack = np.true_divide(sam_image_stack,bkg_image_stack)

    #refresh_widgets
    #show image
    self.ShowImage()
    QtGui.QApplication.restoreOverrideCursor()

  def ShowImage(self):
      image = qimage2ndarray.numpy2qimage(np.array(255*self.scale_image_stack[:,:,int(self.iev)-1], dtype=int))
      pixmap = QtGui.QPixmap.fromImage(image)
      pixmap = pixmap.scaled(379, 379,QtCore.Qt.IgnoreAspectRatio)
      rotated_pixmap = pixmap.transformed(
            QtGui.QMatrix().rotate(-90),
            Qt.SmoothTransformation
        )
      #pixmap = QtGui.QPixmap.fromImage(ImageQt(scipy.misc.toimage(image)))

      self.scene = QGraphicsScene(self)
      item = QGraphicsPixmapItem(rotated_pixmap)
      self.scene.addItem(item)
      self.ui.orgView.setScene(self.scene)



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())

        
            
            
