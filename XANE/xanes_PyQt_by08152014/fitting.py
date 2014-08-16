#!/usr/bin/python
from __future__ import division
import numpy as np
import scipy
import scipy.io
from multiprocessing import Process, cpu_count
from PyQt4.QtGui import *
from scipy.optimize import minimize
from scipy.optimize import nnls
    
def brute_force_2ref(ref1,ref2,data,res):
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
        matrix_ref_com = fRGB[0,i]*matrix_ref1 + fRGB[1,i]*matrix_ref2
        sqr = np.square(data - matrix_ref_com)
        R_ref[:, :, i] = np.sum(sqr, axis=2) / sum_sqdata

    min_R = np.amin(R_ref, axis=2)
    index = scipy.argmin(R_ref, axis=2)
    return  min_R,  index,  fRGB

def brute_force_3ref(ref1,ref2,ref3,data,res):
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

def MP_brute_force_2ref(ref1,ref2,data,res):
    nb_proc = cpu_count()
    print("Your Computer has %s Cores"%nb_proc)
    
    return ref1,ref2,data

def MP_brute_force_3ref(ref1,ref2,ref3,data,res):
    nb_proc = cpu_count()
    print("Your Computer has %s Cores"%nb_proc)
    return ref1,ref2,data

def con_func_3ref(x, m_ref1, m_ref2, m_ref3, s_imgEstack):
    ''' This is the (least square) cost function to be minimized in the constrained optimization algorithm
    '''
    matrix_ref_com = x[0] * m_ref1 + x[1] * m_ref2 + x[2] * m_ref3
    sqr = (s_imgEstack - matrix_ref_com) * (s_imgEstack - matrix_ref_com)
    R_ref = np.sum(sqr)
    return R_ref

def con_func_2ref(x, m_ref1, m_ref2, s_imgEstack):
    ''' This is the (least square) cost function to be minimized in the constrained optimization algorithm

    '''
    matrix_ref_com = x[0] * m_ref1 + x[1] * m_ref2
    sqr = (s_imgEstack - matrix_ref_com) * (s_imgEstack - matrix_ref_com)
    R_ref = np.sum(sqr)
    return R_ref

def least_square_2ref(ref1,ref2,data):
    sum_sqdata = np.sum(np.square(data),axis=2)
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    final_fraction = np.zeros(a*b*3).reshape(a, b, 3)
    final_fval = np.zeros(a*b).reshape(a, b)
    matrix_ref1 = np.copy(data)
    matrix_ref2 = np.copy(data)
    for i in range(c):
        matrix_ref1[:, :, i] = ref1[i]
        matrix_ref2[:, :, i] = ref2[i]
    cons = ({'type' : 'eq',
         'fun' : lambda x: 1 - x[0] - x[1]})
    bnds = ((0, 1), (0, 1))
    for i in range(a):
        for j in range(b):
            res = minimize(con_func_2ref, [0.5, 0.5], args=(matrix_ref1[i, j, :], matrix_ref2[i, j, :], 
                       data[i, j, :]), method='SLSQP', bounds=bnds, constraints=cons, options = {'ftol': 1e-1})               
            final_fraction[i, j, 0] = res.x[0]
            final_fraction[i, j, 1] = res.x[1]
            final_fraction[i, j, 2] = 0
            final_fval[i, j] = res.fun / sum_sqdata[i, j]
    
    return final_fval, final_fraction
    
def least_square_3ref(ref1,ref2,ref3,data):
    sum_sqdata = np.sum(np.square(data),axis=2)
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    final_fraction = np.zeros(a*b*3).reshape(a, b, 3)
    final_fval = np.zeros(a*b).reshape(a, b)
    matrix_ref1 = np.copy(data)
    matrix_ref2 = np.copy(data)
    matrix_ref3 = np.copy(data)
    for i in range(c):
        matrix_ref1[:, :, i] = ref1[i]
        matrix_ref2[:, :, i] = ref2[i]
        matrix_ref3[:, :, i] = ref3[i]  
    cons = ({'type' : 'eq',
         'fun' : lambda x: 1 - x[0] - x[1] - x[2]})
    bnds = ((0, 1), (0, 1), (0, 1))
    for i in range(a):
        for j in range(b):
            res = minimize(con_func_3ref, [0.35, 0.35, 0.3], args=(matrix_ref1[i, j, :], matrix_ref2[i, j, :], matrix_ref3[i, j, :],
                       data[i, j, :]), method='SLSQP', bounds=bnds, constraints=cons, options = {'ftol': 1e-6})               
            final_fraction[i, j, 0] = res.x[0]
            final_fraction[i, j, 1] = res.x[1]
            final_fraction[i, j, 2] = res.x[2]
            final_fval[i, j] = res.fun / sum_sqdata[i, j]
    #dict1 = {}
    #dict1['fraction_Python'] = final_fraction
    #dict2 = {}
    #dict2['fval_Python'] = final_fval
  
    #scipy.io.savemat('fraction_Python_step5.mat', dict1)
    #scipy.io.savemat('fval_Python_step5.mat', dict2)
    
    return final_fval, final_fraction

def NNLS_3ref(ref1,ref2,ref3,data):
    sum_sqdata = np.sum(np.square(data),axis=2)
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    final_fraction = np.zeros(a*b*3).reshape(a, b, 3)
    final_fval = np.zeros(a*b).reshape(a, b)
    std = np.zeros((3, c), dtype='d')  

    std[0,:]=ref1
    std[1,:]=ref2
    std[2,:]=ref3

    for i in range(a):
        print i
        for j in range(b):
            [results, residue]=nnls(np.transpose(std), data[i,j,:])      
            final_fraction[i, j, 0] = results[0]
            final_fraction[i, j, 1] = results[1]
            final_fraction[i, j, 2] = results[2]
            final_fval[i, j] = residue/sum_sqdata[i,j]
    
    return final_fval, final_fraction

def NNLS_2ref(ref1,ref2,data):
    sum_sqdata = np.sum(np.square(data),axis=2)
    [a,b,c] = data.shape[0],data.shape[1],data.shape[2]
    final_fraction = np.zeros(a*b*3).reshape(a, b, 3)
    final_fval = np.zeros(a*b).reshape(a, b)
    std = np.zeros((2, c), dtype='d')  

    std[0,:]=ref1
    std[1,:]=ref2

    for i in range(a):
        print i
        for j in range(b):
            [results, residue]=nnls(np.transpose(std), data[i,j,:])      
            final_fraction[i, j, 0] = results[0]
            final_fraction[i, j, 1] = results[1]
            final_fraction[i, j, 2] = 0
            final_fval[i, j] = residue/sum_sqdata[i,j]
    
    return final_fval, final_fraction

   

