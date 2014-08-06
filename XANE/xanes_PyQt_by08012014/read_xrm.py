import xradia_xrm as xx
#import data_stack_sim as dstack
import data_struct as dstruct
import matplotlib.pyplot as plt
import sys
import numpy as npy
import scipy
import os

#filename=sys.argv[1]
#bgfile=sys.argv[2]

#n_input = npy.size(sys.argv)
#if(n_input == 4):
#	imgname=sys.argv[3]
#if(n_input == 3):
imgname='Image'

#filename = 'C:/X8Cdata/009_XANES_Cu/CuO_XANES_script/CuO9040.xrm'
#bgfile = 'C:/X8Cdata/009_XANES_Cu/CuO_XANES_script/CuObkg9040.xrm'
filename = 'D:/Research/BNL_2014_Summer_Intern/xrmFileSet1/20131011_024_FeF3_CellB10_insitu_XANES01_sam_7289.xrm'
bgfile = 'D:/Research/BNL_2014_Summer_Intern/xrmFileSet1/20131011_024_FeF3_CellB10_insitu_XANES01_bkg_7289.xrm'
n_input = 3


#save_dir = os.getcwd()+'/'+filename[:len(filename)-5]
#if not os.path.exists(save_dir):
        #os.makedirs(save_dir)

#filename='20120222_032_11-5NB_theta.txrm'
#bgfile='20120222_031_11-5NB_bkg.xrm'



reader = xx.xrm()
array = dstruct

reader.read_xrm(filename,array)
nx, ny, nz_dt = npy.shape(array.exchange.data)
dt = npy.zeros((nx,ny,nz_dt))
dt = array.exchange.data[:,:,:]

plt.figure(1)
plt.imshow(dt[:,:,0])
save_dir = 'D:/Research/BNL_2014_Summer_Intern/xrmFileSet1'
#save_dir = 'C:\X8Cdata\009_XANES_Cu\CuO_XANES_script\test'

f = open(save_dir+'/configure.txt','w')
f.write('Data creation date: \n')
f.write(str(array.information.file_creation_datetime))
f.write('\n')
f.write('=======================================\n')
f.write('Sample name: \n')
f.write(str(array.information.sample.name))
f.write('\n')
f.write('=======================================\n')
f.write('Experimenter name: \n')
f.write(str(array.information.experimenter.name))
f.write('\n')
f.write('=======================================\n')
f.write('Xray energy: \n')
f.write(str(array.exchange.energy))
f.write(str(array.exchange.energy_units))
f.write('\n')
f.write('=======================================\n')
f.write('nx, ny: \n')
f.write(str(dt.shape[0]))
f.write(', ')
f.write(str(dt.shape[1]))
f.write('\n')
f.write('=======================================\n')
f.write('Number of frames: \n')
f.write(str(dt.shape[2]))
f.write('\n')
f.write('=======================================\n')
f.write('Angles: \n')
f.write(str(array.exchange.angles))
f.write('\n')
f.write('=======================================\n')
f.write('Data type: \n')
f.write(str(dt.dtype))
f.write('\n')
f.write('=======================================\n')
f.write('Data axes: \n')
f.write(str(array.exchange.data_axes))
f.write('\n')
f.write('=======================================\n')
f.write('Data dwell: \n')
f.write(str(array.spectromicroscopy.data_dwell))
f.write('\n')
f.write('=======================================\n')
f.write('x distance: \n')
f.write(str(array.exchange.x))
f.write('\n')
f.write('=======================================\n')
f.write('x units: \n')
f.write(str(array.exchange.x_units))
f.write('\n')
f.write('=======================================\n')
f.write('y distance: \n')
f.write(str(array.exchange.y))
f.write('\n')
f.write('=======================================\n')
f.write('y units: \n')
f.write(str(array.exchange.y_units))
f.write('\n')
f.close()



reader.read_xrm(bgfile,array)
nx, ny, nz = npy.shape(array.exchange.data)
bg = npy.zeros((nx,ny,nz))
bg = array.exchange.data[:,:,:]

plt.figure(2)
plt.imshow(bg[:,:,0])

index = npy.where(bg == 0.)
bg[index] = 1.
for i in range(0,nz_dt):
    dt[:,:,i] = dt[:,:,i] / bg[:,:,0]
    scipy.misc.imsave(save_dir+'/'+imgname+'_'+str(i)+'.tif', dt[:,:,i])


plt.figure(3)
plt.imshow(dt[:,:,0])


f = open(save_dir+'/binary_array.dat','w')
f.write(dt)
f.close()


