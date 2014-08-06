#!/usr/bin/python
from __future__ import division
import numpy as np
import scipy
import PyQt4.QtGui as QtGui

def fit2D_2ref_loop(ref1,ref2,data,res):
    #QtGui.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    total = 100/res + 1
    total = int(total)
    print res,total
    factor = (np.linspace(0,1,total))
    print factor
    fRGB = np.zeros((3,total), dtype=np.float32)
    fRGB[0,:] = factor
    fRGB[1,:] = 1-factor
    #self.fRGB[2,:] = np.zeros(total,dtype=np.int)
    #self.fRGB = np.append(self.fRGB,np.zeros(total,dtype=np.float32),axis=1)
    #print self.fRGB[0,1],ref1
    #print self.fRGB[0,1]*ref1
    #print fRGB
    sum_sqdata = np.sum(np.square(data),axis=2)
    print sum_sqdata.shape
    #print sum_sqdata[500,500:550]
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    R_ref = np.empty((a,b,total),dtype=np.float32)
    #index = np.empty((a,b),dtype=np.int)
    #min_R = np.empty((a,b),dtype=np.float32)
    for i in range(a):
        for j in range(b):
	    for k in range(int(total)):
                image_ref_com = np.add(np.multiply(fRGB[0,k],ref1),np.multiply(fRGB[1,k],ref2))
		sqr = np.square(data[i,j,:]-image_ref_com)
		R_ref[i,j,k] = np.sum(sqr)/sum_sqdata[i,j]        
    min_R = np.amin(R_ref, axis=2)
    index = np.argmin(R_ref, axis=2)
    
    #print sqr
    print index.shape
    #print R_ref[500,500,0:total-1]
    #print min_R[500,500:550]
    #wildcard =  "TXT (*.txt)" 
    #filepath = QtGui.QFileDialog.getSaveFileName(self, 'Save Spectrum to Athena', '', wildcard)
    #f = open(filepath,'w')
    #for i in range(a):
        #f.write("%14.5f\n"%( index[i,500]))
    #f.close()
    #QtGui.QApplication.restoreOverrideCursor()
    return  min_R,  index,  fRGB
    
def fit2D_2ref(ref1,ref2,data,res):
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    print a,b,c
    matrix_ref1 = np.copy(data)
    matrix_ref2 = np.copy(data)
    for i in range(c):
        matrix_ref1[:, :, i] = ref1[i]
        matrix_ref2[:, :, i] = ref2[i]
    total = 100/res + 1
    total = int(total)
    factor = (np.linspace(0,1,total))
    fRGB = np.zeros((3,total), dtype=np.float16)
    fRGB[0,:] = factor
    fRGB[1,:] = 1-factor
    sum_sqdata = np.sum(np.square(data),axis=2)
    R_ref = np.empty((a,b,total),dtype=np.float16)
    for i in range(total):
        print i
        combination = i
        matrix_ref_com = fRGB[0,i]*matrix_ref1 + fRGB[1,i]*matrix_ref2
        sqr = np.square(data - matrix_ref_com)
        R_ref[:, :, i] = np.sum(sqr, axis=2) / sum_sqdata

    min_R = np.amin(R_ref, axis=2)
    index = scipy.argmin(R_ref, axis=2)
    save_dir = 'D:/Research/BNL_2014_Summer_Intern/xanes_PyQT'
    f = open(save_dir+'/index.txt','w')
    for i in range(a):
        f.write("%14.5f\n"%( index[i,500]))
    f.close()
    return  min_R,  index,  fRGB

def fit2D_3ref(ref1,ref2,ref3,data,res):
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    matrix_ref1 = np.copy(data)
    matrix_ref2 = np.copy(data)
    matrix_ref3 = np.copy(data)
    for i in range(c):
        matrix_ref1[:, :, i] = ref1[i]
        matrix_ref2[:, :, i] = ref2[i]
        matrix_ref3[:, :, i] = ref3[i]
    max = 100 / res
    nchoosek_top = max + 2
    total = scipy.misc.comb(nchoosek_top, 2)
    RGB = np.ones(total*3).reshape(3, total)
    factor1 = 0
    factor2 = 0
    for i in range(int(total)):
        RGB[0][i] = max - factor1
        RGB[1][i] = max - RGB[0][i] - factor2
        RGB[2][i] = max - RGB[0][i] - RGB[1][i]    
        factor2 = factor2 + 1   
        if RGB[1][i] == 0:
            factor1 = factor1 + 1
            factor2 = 0
    fRGB = RGB * res / 100.0
    sqdata = data * data
    sum_sqdata =  np.sum(sqdata, axis=2)

    R_ref = np.empty((a,b,total),dtype=np.float16)

    for i in range(int(total)):
        print i
        matrix_ref_com = fRGB[0][i]*matrix_ref1 + fRGB[1][i]*matrix_ref2 + fRGB[2][i]*matrix_ref3
        sqr = (data - matrix_ref_com) * (data - matrix_ref_com)
        R_ref[:, :, i] = np.sum(sqr, axis=2) / sum_sqdata

    min_R = np.amin(R_ref, axis=2)
    index = scipy.argmin(R_ref, axis=2)
    return  min_R,  index,  fRGB

