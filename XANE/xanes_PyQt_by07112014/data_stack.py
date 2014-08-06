# 
#   This file is part of Mantis, a Multivariate ANalysis Tool for Spectromicroscopy.
# 
#   Copyright (C) 2011 Mirna Lerotic, 2nd Look
#   http://2ndlook.co/products.html
#   License: GNU GPL v3
#
#   Mantis is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
#   Mantis is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details <http://www.gnu.org/licenses/>.


from __future__ import division



import numpy as np
import scipy.interpolate
import scipy.ndimage
import h5py 
import datetime 

import x1a_stk
import aps_hdf5
import xradia_xrm
import xradia_xrm_list
import accel_sdf
import data_struct

#----------------------------------------------------------------------
class data(x1a_stk.x1astk,aps_hdf5.h5, xradia_xrm.xrm, xradia_xrm_list.xrm,accel_sdf.sdfstk):
    def __init__(self, data_struct):
        x1a_stk.x1astk.__init__(self)
        aps_hdf5.h5.__init__(self)
        xradia_xrm.xrm.__init__(self)
        xradia_xrm_list.xrm.__init__(self)
        accel_sdf.sdfstk.__init__(self)
        
        self.data_struct = data_struct
        
        self.i0_dwell = None 
        
        self.n_ev = 0

#----------------------------------------------------------------------   
    def new_data(self):
        self.n_cols = 0
        self.n_rows = 0
        self.n_ev = 0
               
        self.x_dist = 0       
        self.y_dist = 0

        self.ev = 0         
        self.absdata = 0

        
        self.i0data = 0
        self.evi0 = 0
        
        self.od = 0
        self.od3d = 0
        
        self.xshifts = 0
        self.yshifts = 0
        

        self.data_struct.spectromicroscopy.normalization.white_spectrum = None
        self.data_struct.spectromicroscopy.normalization.white_spectrum_energy = None
        self.data_struct.spectromicroscopy.normalization.white_spectrum_energy_units = None
        
        self.data_struct.spectromicroscopy.optical_density = None      
           
#----------------------------------------------------------------------   
    def read_stk_i0(self, filename, extension):
        if extension == '.xas':
            x1a_stk.x1astk.read_stk_i0_xas(self,filename)
        elif extension == '.csv':
            x1a_stk.x1astk.read_stk_i0_csv(self,filename)
            
        self.calculate_optical_density()
        
        self.fill_h5_struct_normalization()
        
        
#----------------------------------------------------------------------   
    def read_sdf_i0(self, filename):
        accel_sdf.sdfstk.read_sdf_i0(self,filename)
        self.calculate_optical_density()
        
        self.fill_h5_struct_normalization()
        
        
#----------------------------------------------------------------------   
    def read_xrm_ReferenceImages(self, filenames):

        
        self.calculate_optical_density_from_refimgs(filenames)
        
        self.fill_h5_struct_normalization()
        
              

#---------------------------------------------------------------------- 
    def read_stk(self, filename):    
        self.new_data()  
        x1a_stk.x1astk.read_stk(self, filename)
        
        self.fill_h5_struct_from_stk()
        
        self.scale_bar()
        
#---------------------------------------------------------------------- 
    def read_sdf(self, filename):    
        self.new_data()  
        accel_sdf.sdfstk.read_sdf(self, filename)
        
        self.fill_h5_struct_from_stk()
        
        self.scale_bar()
  
#---------------------------------------------------------------------- 
    def read_h5(self, filename):    
        self.new_data()  
        aps_hdf5.h5.read_h5(self, filename, self.data_struct)
        
        if self.data_struct.spectromicroscopy.optical_density is not None: 
            #print 'reading optical density'
            self.i0data = self.data_struct.spectromicroscopy.normalization.white_spectrum 
            self.evi0 = self.data_struct.spectromicroscopy.normalization.white_spectrum_energy 
        
            self.od = self.data_struct.spectromicroscopy.optical_density
            
            self.od3d = self.od.copy()
            
            self.od3d = np.reshape(self.od3d, (self.n_cols, self.n_rows, self.n_ev), order='F')
                    
        elif self.data_struct.spectromicroscopy.normalization.white_spectrum is not None:
            self.calculate_optical_density()
            self.fill_h5_struct_normalization()

            
        self.scale_bar()
        
#---------------------------------------------------------------------- 
    def read_txrm(self, filename):    
        self.new_data()  
        xradia_xrm.xrm.read_txrm(self, filename, self.data_struct)
        
                
        self.scale_bar()
#---------------------------------------------------------------------- 
    def read_xrm_list(self, filename):    

        self.new_data()  
        xradia_xrm_list.xrm.read_xrm_list(self, filename, self.data_struct)
        
                
        self.scale_bar()
        
                
#---------------------------------------------------------------------- 
    def read_xrm(self, filename):    
        self.new_data()  
        xradia_xrm.xrm.read_xrm(self, filename, self.data_struct)
        
                
        self.scale_bar()
        
        
#---------------------------------------------------------------------- 
    def read_tiff(self, filename):    
        self.new_data()  
        
        import tiff_stack
        tiffstack = tiff_stack.TiffStackWrapper(filename)
        mode = tiffstack.get_mode()
        if mode == 'I;16B':
            imgmode = 16
        else:
            imgmode = 8
        
        frame0 = tiffstack.get_frame(0)
        imgstack = np.array((frame0))
          
        haveimg = True
        it = 1
        while haveimg:
            frame = tiffstack.get_frame(it)
            if frame == None:
                haveimg = False
            else:
                it+=1
                imgstack = np.dstack((imgstack,frame))
                
        if imgmode == 16:
            imgstack = imgstack.astype(np.uint16)
        else:
            imgstack = imgstack.astype(np.uint8)
            
        self.n_cols = imgstack.shape[0]
        self.n_rows = imgstack.shape[1]
        self.n_ev = imgstack.shape[2]
        
        
        pixelsize = 1
        #Since we do not have a scanning microscope we fill the x_dist and y_dist from pixel_size
        self.x_dist = np.arange(np.float(self.n_cols))*pixelsize
        self.y_dist = np.arange(np.float(self.n_rows))*pixelsize

        #Read energies from file
        import os
        basename, extension = os.path.splitext(filename) 
        engfilename = basename+'.txt'
        f = open(str(engfilename),'r')
        
        elist = []   
    
        for line in f:
            if line.startswith("*"):
                pass
            else:
                e = float(line)
                elist.append(e)
                
        self.ev = np.array(elist)
                
        f.close()
        
        
        
        msec = np.ones((self.n_ev))
         
        self.data_dwell = msec
                       
        self.absdata = imgstack
                
        #Check if the energies are consecutive, if they are not sort the data
        sort = 0
        for i in range(self.n_ev - 1):
            if self.ev[i] > self.ev[i+1]:
                sort = 1
                break
        if sort == 1:
            sortind = np.argsort(self.ev)
            self.ev = self.ev[sortind]
            self.absdata = self.absdata[:,:,sortind]

        
        self.original_n_cols = imgstack.shape[0]
        self.original_n_rows = imgstack.shape[1]
        self.original_n_ev = imgstack.shape[2]
        self.original_ev = self.ev.copy()
        self.original_absdata = self.absdata.copy()

       
        self.fill_h5_struct_from_stk()
         
        self.scale_bar()
        

#---------------------------------------------------------------------- 
    def read_dpt(self, filename):    
        self.new_data()  
        
        n_rows = 11
        n_cols = 8 
        
        imgstack = np.zeros((n_rows,n_cols))
        

        f = open(str(filename),'r')
        
        elist = []   
    
        for line in f:
            if line.startswith("*"):
                pass
            else:
                x = line.split(',')
                e = float (x[0]) 
                x = x[1:]
                data = []
                for i in range(len(x)):
                    data.append(float(x[i]))
                elist.append(e)
                data = np.array(data)
                data = np.reshape(data, (n_rows, n_cols), order='F')
                imgstack = np.dstack((imgstack, data))
                
                
        imgstack = imgstack[:,:,1:]
                
        f.close()
        
        
            
        self.n_cols = imgstack.shape[0]
        self.n_rows = imgstack.shape[1]
        self.n_ev = imgstack.shape[2]
        
        
        pixelsize = 1
        #Since we do not have a scanning microscope we fill the x_dist and y_dist from pixel_size
        self.x_dist = np.arange(np.float(self.n_cols))*pixelsize
        self.y_dist = np.arange(np.float(self.n_rows))*pixelsize

                
        self.ev = np.array(elist)

        msec = np.ones((self.n_ev))
         
        self.data_dwell = msec
                       
        self.absdata = imgstack
                
        #Check if the energies are consecutive, if they are not sort the data
        sort = 0
        for i in range(self.n_ev - 1):
            if self.ev[i] > self.ev[i+1]:
                sort = 1
                break
        if sort == 1:
            sortind = np.argsort(self.ev)
            self.ev = self.ev[sortind]
            self.absdata = self.absdata[:,:,sortind]

        
        self.original_n_cols = imgstack.shape[0]
        self.original_n_rows = imgstack.shape[1]
        self.original_n_ev = imgstack.shape[2]
        self.original_ev = self.ev.copy()
        self.original_absdata = self.absdata.copy()

       
        self.fill_h5_struct_from_stk()
         
        self.scale_bar()
        
        
        #Fix the normalization
        self.evi0 = self.ev.copy()
        self.i0data = np.ones(self.n_ev)
        
        self.i0_dwell = self.data_dwell
   
        
        self.fill_h5_struct_normalization()
        
        #Optical density does not have to be calculated - use raw data
        
        self.od3d = self.absdata.copy()
        
        self.od = np.reshape(self.od3d, (n_rows*n_cols, self.n_ev), order='F')
        
        
                
#---------------------------------------------------------------------- 
    def fill_h5_struct_from_stk(self):   
        
        
        now = datetime.datetime.now()
        
        self.data_struct.implements = 'information:exchange:spectromicroscopy'
        self.data_struct.version = '1.0'
        
        self.data_struct.information.file_creation_datetime = now.strftime("%Y-%m-%dT%H:%M")
        self.data_struct.information.comment = 'Converted from .stk'
        
        
        self.data_struct.exchange.data = self.absdata
        self.data_struct.exchange.data_signal = 1
        self.data_struct.exchange.data_axes='x:y'
        
        self.data_struct.exchange.energy=self.ev
        self.data_struct.exchange.energy_units = 'ev'
        
        
        self.data_struct.exchange.x = self.x_dist
        self.data_struct.exchange.y = self.y_dist
        

        
#---------------------------------------------------------------------- 
    def fill_h5_struct_normalization(self):   
        
        self.data_struct.spectromicroscopy.normalization.white_spectrum = self.i0data 
        self.data_struct.spectromicroscopy.normalization.white_spectrum_energy = self.evi0
        self.data_struct.spectromicroscopy.normalization.white_spectrum_energy_units = 'eV'
        
        self.data_struct.spectromicroscopy.optical_density = self.od
        
    
#----------------------------------------------------------------------   
    def calc_histogram(self):
        #calculate average flux for each pixel
        self.averageflux = np.mean(self.absdata,axis=2)
        self.histogram = self.averageflux
        
        return
        
        
#----------------------------------------------------------------------   
    def i0_from_histogram(self, fluxmin, fluxmax):

        self.evi0hist = self.ev.copy()

        self.i0datahist = np.zeros(self.n_ev)

        i0_indices = np.where((fluxmin<self.averageflux)&(self.averageflux<fluxmax))
        if np.any(i0_indices):
            invnumel = 1./self.averageflux[i0_indices].shape[0]
            for ie in range(self.n_ev):  
                thiseng_abs = self.absdata[:,:,ie]
                self.i0datahist[ie] = np.sum(thiseng_abs[i0_indices])*invnumel


        self.evi0 = self.ev.copy()
        self.i0data = self.i0datahist 
        
        self.i0_dwell = self.data_dwell

        self.calculate_optical_density()   
        
        self.fill_h5_struct_normalization()
        
        return    
    
#----------------------------------------------------------------------   
    def UsePreNormalizedData(self):
    
        self.evi0 = self.ev.copy()
        self.i0data = np.ones(self.n_ev)
        
        self.i0_dwell = self.data_dwell
        
        self.od = np.empty((self.n_cols, self.n_rows, self.n_ev))
        for i in range(self.n_ev):
            self.od[:,:,i] = self.absdata[:,:,i]
        
           
        self.od3d = self.od.copy()
        
        n_pixels = self.n_cols*self.n_rows
        #Optical density matrix is rearranged into n_pixelsxn_ev
        self.od = np.reshape(self.od, (n_pixels, self.n_ev), order='F')
        
        self.fill_h5_struct_normalization()
        
        return
        
    
#----------------------------------------------------------------------   
    def set_i0(self, i0data, evdata):

        self.evi0 = evdata
        self.i0data = i0data 
        
        self.i0_dwell = self.data_dwell

        self.calculate_optical_density()
        
        self.fill_h5_struct_normalization()
    
        return  
    
#----------------------------------------------------------------------   
# Normalize the data: calculate optical density matrix D 
    def calculate_optical_density(self):

        n_pixels = self.n_cols*self.n_rows
        self.od = np.empty((self.n_cols, self.n_rows, self.n_ev))
        
        #little hack to deal with rounding errors
        self.evi0[self.evi0.size-1] += 0.001
        
        fi0int = scipy.interpolate.interp1d(self.evi0,self.i0data, kind='cubic', bounds_error=False, fill_value=0.0)      
        i0 = fi0int(self.ev)
        
        if (self.data_dwell is not None) and (self.i0_dwell is not None):

            i0 = i0*(self.data_dwell/self.i0_dwell)
        
        #zero out all negative values in the image stack
        negative_indices = np.where(self.absdata <= 0)
        if negative_indices:
            self.absdata[negative_indices] = 0.01
                           

        for i in range(self.n_ev):
            self.od[:,:,i] = - np.log(self.absdata[:,:,i]/i0[i])
        
        #clean up the result
        nan_indices = np.where(np.isfinite(self.od) == False)
        if nan_indices:
            self.od[nan_indices] = 0
            
        self.od3d = self.od.copy()
        

        #Optical density matrix is rearranged into n_pixelsxn_ev
        self.od = np.reshape(self.od, (n_pixels, self.n_ev), order='F')

        return
    

#----------------------------------------------------------------------   
# Normalize the data: calculate optical density matrix D 
    def calculate_optical_density_from_refimgs(self, files):

        n_pixels = self.n_cols*self.n_rows
        self.od = np.empty((self.n_cols, self.n_rows, self.n_ev))
                
        #zero out all negative values in the image stack
        negative_indices = np.where(self.absdata <= 0)
        if negative_indices:
            self.absdata[negative_indices] = 0.01
                           

        #Load reference images
        refimgs = np.empty((self.n_cols, self.n_rows, self.n_ev))
        refimgs_ev = []
        for i in range(len(files)):
            ncols, nrows, iev, imgdata = xradia_xrm.xrm.read_xrm_fileinfo(self, files[i], readimgdata = True)
            refimgs[:,:,i] = np.reshape(imgdata, (ncols, nrows), order='F')
            refimgs_ev.append(iev)
 
        #Check if the energies are consecutive, if they are not sort the data
        consec = 0
        for i in range(len(refimgs_ev) - 1):
            if refimgs_ev[i] > refimgs_ev[i+1]:
                consec = 1
                break
        if consec == 1:
            sortind = np.argsort(refimgs_ev)
            refimgs_ev = refimgs_ev[sortind]
            refimgs = refimgs[:,:,refimgs_ev]
        
            
        for i in range(self.n_ev):
            if self.ev[i] != refimgs_ev[i]:
                print 'Error, wrong reference image energy'
                return
            
            self.od[:,:,i] = - np.log(self.absdata[:,:,i]/refimgs[:,:,i])
        
        #clean up the result
        nan_indices = np.where(np.isfinite(self.od) == False)
        if nan_indices:
            self.od[nan_indices] = 0
            
        self.od3d = self.od.copy()
        

        #Optical density matrix is rearranged into n_pixelsxn_ev
        self.od = np.reshape(self.od, (n_pixels, self.n_ev), order='F')
        
        
        self.evi0 = refimgs_ev
        self.i0data = np.ones((self.n_ev))
        self.i0_dwell = self.data_dwell
        

        return    


#----------------------------------------------------------------------   
    def scale_bar(self): 
           
        x_start = np.amin(self.y_dist)
        x_stop = np.amax(self.y_dist)
        
        onepixsize = np.abs(self.y_dist[1]-self.y_dist[0])
                
        bar_microns = 0.2*np.abs(x_stop-x_start)
        
        
        if bar_microns >= 10.:
            bar_microns = 10.*int(0.5+0.1*int(0.5+bar_microns))
            bar_string = str(int(0.01+bar_microns)).strip()
        elif bar_microns >= 1.:      
            bar_microns = float(int(0.5+bar_microns))
            if bar_microns == 1.:
                bar_string = '1'
            else:
                bar_string = str(int(0.01+bar_microns)).strip()
        else:
            bar_microns = np.maximum(0.1*int(0.5+10*bar_microns),0.1)
            bar_string = str(bar_microns).strip()
            
        self.scale_bar_string = bar_string


        self.scale_bar_pixels_x = int(0.5+float(self.n_rows)*
                       float(bar_microns)/float(abs(x_stop-x_start)))
        
        self.scale_bar_pixels_y = int(0.01*self.n_rows)
        
        if self.scale_bar_pixels_y < 2:
                self.scale_bar_pixels_y = 2
                
             
             
    
#----------------------------------------------------------------------   
    def write_xas(self, filename, evdata, data):
        f = open(filename, 'w')
        print>>f, '*********************  X-ray Absorption Data  ********************'
        print>>f, '*'
        print>>f, '* Formula: '
        print>>f, '* Common name: '
        print>>f, '* Edge: '
        print>>f, '* Acquisition mode: '
        print>>f, '* Source and purity: ' 
        print>>f, '* Comments: Stack list ROI ""'
        print>>f, '* Delta eV: '
        print>>f, '* Min eV: '
        print>>f, '* Max eV: '
        print>>f, '* Y axis: '
        print>>f, '* Contact person: '
        print>>f, '* Write date: '
        print>>f, '* Journal: '
        print>>f, '* Authors: '
        print>>f, '* Title: '
        print>>f, '* Volume: '
        print>>f, '* Issue number: '
        print>>f, '* Year: '
        print>>f, '* Pages: '
        print>>f, '* Booktitle: '
        print>>f, '* Editors: '
        print>>f, '* Publisher: '
        print>>f, '* Address: '
        print>>f, '*--------------------------------------------------------------'
        for ie in range(self.n_ev):
            print>>f, '\t%.6f\t%.6f' %(evdata[ie], data[ie])
        
        f.close()
    
        return  
    
#----------------------------------------------------------------------   
    def write_csv(self, filename, evdata, data, cname = ''):
        f = open(filename, 'w')
        print>>f, '*********************  X-ray Absorption Data  ********************'
        print>>f, '*'
        print>>f, '* Formula: '
        print>>f, '* Common name: ', cname
        print>>f, '* Edge: '
        print>>f, '* Acquisition mode: '
        print>>f, '* Source and purity: ' 
        print>>f, '* Comments: Stack list ROI ""'
        print>>f, '* Delta eV: '
        print>>f, '* Min eV: '
        print>>f, '* Max eV: '
        print>>f, '* Y axis: '
        print>>f, '* Contact person: '
        print>>f, '* Write date: '
        print>>f, '* Journal: '
        print>>f, '* Authors: '
        print>>f, '* Title: '
        print>>f, '* Volume: '
        print>>f, '* Issue number: '
        print>>f, '* Year: '
        print>>f, '* Pages: '
        print>>f, '* Booktitle: '
        print>>f, '* Editors: '
        print>>f, '* Publisher: '
        print>>f, '* Address: '
        print>>f, '*--------------------------------------------------------------'
        for ie in range(self.n_ev):
            print>>f, '%.6f, %.6f' %(evdata[ie], data[ie])
        
        f.close()
    
        return  
    
#----------------------------------------------------------------------   
#Read x-ray absorption spectrum
    def read_xas(self, filename):
        
        spectrum_common_name = ' '
 
        f = open(str(filename),'rU')
        
        elist = []
        ilist = []    
    
        for line in f:
            if line.startswith('*'):
                if 'Common name' in line:
                    spectrum_common_name = line.split(':')[-1].strip()

            else:
                e, i = [float (x) for x in line.split()] 
                elist.append(e)
                ilist.append(i)
                
        spectrum_evdata = np.array(elist)
        spectrum_data = np.array(ilist) 
                
        f.close()
        
        if spectrum_evdata[-1]<spectrum_evdata[0]:
            spectrum_evdata = spectrum_evdata[::-1]
            spectrum_data = spectrum_data[::-1]
        
        return spectrum_evdata, spectrum_data, spectrum_common_name

#----------------------------------------------------------------------   
#Read x-ray absorption spectrum
    def read_csv(self, filename):
        
        spectrum_common_name = ' '
 
        f = open(str(filename),'rU')
        
        elist = []
        ilist = []    
        
        
        #Check the first character of the line and skip if not a number
        allowedchars = ['0','1','2','3','4','5','6','7','8','9','-','.']
    

        for line in f:
            if line.startswith('*'):
                if 'Common name' in line:
                    spectrum_common_name = line.split(':')[-1].strip()
            elif line[0] not in allowedchars:
                continue
            else:
                e, i = [float (x) for x in line.split(',')] 
                elist.append(e)
                ilist.append(i)
                
                
        spectrum_evdata = np.array(elist)
        spectrum_data = np.array(ilist) 
                
        f.close()
        
        if spectrum_evdata[-1]<spectrum_evdata[0]:
            spectrum_evdata = spectrum_evdata[::-1]
            spectrum_data = spectrum_data[::-1]
        
        return spectrum_evdata, spectrum_data, spectrum_common_name
        
                
    
#----------------------------------------------------------------------   
#Register images using Fourier Shift Theorem
    def register_images(self, ref_image, image2, have_ref_img_fft = False):
        
        if have_ref_img_fft == False:
            self.ref_fft = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(ref_image)))
        img2_fft = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(image2)))
        
        fr = (self.ref_fft*img2_fft.conjugate())/(np.abs(self.ref_fft)*np.abs(img2_fft))
        fr = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(fr)))
        fr = np.abs(fr)
        
        shape = ref_image.shape
        
        xc, yc = np.unravel_index(np.argmax(fr), shape)
        
        # Limit the search to 1 pixel border
        if xc == 0:
            xc=1
        if xc == shape[0]-1:
            xc = shape[0]-2
            
        if yc == 0:
            yc=1
        if yc == shape[1]-1:
            yc = shape[1]-2
            
        #Use peak fit to find the shifts 
        xpts = [xc-1,xc,xc+1]
        ypts = fr[xpts,yc]     
        xf, fit = self.peak_fit(xpts, ypts)

        xpts = [yc-1,yc,yc+1]
        ypts = fr[xc,xpts]     
        yf, fit = self.peak_fit(xpts, ypts)   
              
        
        xshift = xf - np.float(shape[0])/2.0
        yshift = yf - np.float(shape[1])/2.0
        
                
        return xshift, yshift, fr
    

#----------------------------------------------------------------------   
#Apply image registration
    def apply_image_registration(self, image, xshift, yshift):
        
        shape = image.shape
        nx = shape[0]
        ny = shape[1]
        
        outofboundariesval = np.sum(image)/float(nx*ny)        
        shifted_img = scipy.ndimage.interpolation.shift(image,[xshift,yshift],
                                                        mode='constant', 
                                                        cval=outofboundariesval)
        
        return shifted_img
    
#----------------------------------------------------------------------   
#Apply image registration
    def crop_registed_images(self, images, xshifts, yshifts):
        
        min_xshift = np.min(xshifts)
        max_xshift = np.max(xshifts)
        
        min_yshift = np.min(yshifts)
        max_yshift = np.max(yshifts)
        
        # if the image is moved to the right (positive) we need to crop the left side 
        xleft = np.ceil(max_xshift)
        if xleft < 0:
            xleft = 0
        # if the image is moved to the left (negative) we need to crop the right side 
        xright = np.floor(self.n_cols+min_xshift)
        if xright>(self.n_cols):
            xright = self.n_cols
        
        ybottom = np.ceil(max_yshift)
        if ybottom <0:
            ybottom = 0
        ytop = np.floor(self.n_rows+min_yshift)
        if ytop > (self.n_rows):
            ytop = self.n_rows
            
            
        cropped_stack = images[xleft:xright, ybottom:ytop, :]
        
        return cropped_stack, xleft, xright, ybottom, ytop


#----------------------------------------------------------------------   
#Quadratic peak fit: Fits the 3 data pairs to y=a+bx+cx^2, returning fit=[a,b,c]'
#  and xpeak at position of inflection'
    def peak_fit(self, x, y):
        
        y1y0=y[1]-y[0]
        y2y0=y[2]-y[0]
        x1x0=np.float(x[1]-x[0])
        x2x0=np.float(x[2]-x[0])
        x1x0sq=np.float(x[1]*x[1]-x[0]*x[0])
        x2x0sq=np.float(x[2]*x[2]-x[0]*x[0])
                
        c_num=y2y0*x1x0-y1y0*x2x0
        c_denom=x2x0sq*x1x0-x1x0sq*x2x0
        
        if c_denom == 0:
            print 'Divide by zero error'
            return 

        c=c_num/np.float(c_denom)
        if x1x0 == 0:
            print 'Divide by zero error'
            return

        b=(y1y0-c*x1x0sq)/np.float(x1x0)
        a=y[0]-b*x[0]-c*x[0]*x[0]
  
        fit=[a,b,c]
        if c == 0:
            xpeak=0.
            print 'Cannot find xpeak'
            return
        else:
            #Constrain the fit to be within these three points. 
            xpeak=-b/(2.0*c)
            if xpeak < x[0]:
                xpeak = np.float(x[0])
            if xpeak > x[2]:
                xpeak = np.float(x[2])
        
        return xpeak, fit
        
        
#-----------------------------------------------------------------------------
#Despike image using Enhanced Lee Filter
    def despike(self, image, leefilt_percent = 50.0):
        
        fimg = self.lee_filter(image)
        
        leefilt_max = np.amax(fimg)
        threshold = (1.+0.01*leefilt_percent)*leefilt_max
    
        
        datadim = np.int32(image.shape)

        ncols = datadim[0].copy()
        nrows =  datadim[1].copy()
              
        spikes = np.where(image > threshold)
        n_spikes = fimg[spikes].shape[0]
        

        result_img = image.copy()
        
        if n_spikes > 0:

            xsp = spikes[0]
            ysp = spikes[1]
            for i in range(n_spikes):
                ix = xsp[i]
                iy = ysp[i]
                print ix,iy
                if ix == 0:
                    ix1 = 1
                    ix2 = 2
                elif ix == (ncols-1):
                    ix1 = ncols-2
                    ix2 = ncols -3
                else:
                    ix1 = ix - 1
                    ix2 = ix + 1
                    
                if iy == 0:
                    iy1 = 1
                    iy2 = 2
                elif iy == (nrows-1):
                    iy1 = nrows-2
                    iy2 = nrows-3
                else:
                    iy1 = iy - 1
                    iy2 = iy + 1      
                 
                print result_img[ix,iy]
                result_img[ix,iy] = 0.25*(image[ix1,iy]+image[ix2,iy]+
                                          image[ix,iy1]+image[ix,iy2])  
                print result_img[ix,iy]
            
        return result_img        
                                        
            
#-----------------------------------------------------------------------------   
# Lee filter
    def lee_filter(self, image):
    
        nbox = 5 #The size of the filter box is 2N+1.  The default value is 5.
        sig = 5.0 #Estimate of the standard deviation.  The default is 5.
        
        delta = int((nbox - 1)/2) #width of window
        
        datadim = np.int32(image.shape)
        
        
        n_cols = datadim[0].copy()
        n_rows =  datadim[1].copy()
        
        Imean = np.zeros((n_cols,n_rows))
        scipy.ndimage.filters.uniform_filter(image, size=nbox, output=Imean)
        
        Imean2 = Imean**2
        
        #variance
        z = np.empty((n_cols,n_rows))
        

        for l in range(delta, n_cols-delta):
            for s in range(delta, n_rows-delta):    
                
                z[l,s] = np.sum((image[l-delta:l+delta,s-delta:s+delta]-Imean[l,s])**2)
                

        z = z / float(nbox**2-1.0)
        
        z = (z + Imean2)/float(1.0+sig**2)-Imean2
        
        ind = np.where(z < 0)
        n_ind = z[ind].shape[0]
        if n_ind > 0:
            z[ind] = 0
        
        lf_image = Imean + (image-Imean)*(z/(Imean2*sig**2+z))
        
        return lf_image
        
