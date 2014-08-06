# 
#   This file is part of Mantis, a Multivariate ANalysis Tool for Spectromicroscopy.
# 
#   Copyright (C) 2011 Benjamin Watts, Paul Scherrer Institut
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


import re, numpy
from os.path import splitext, exists



#----------------------------------------------------------------------
class HDR_FileParser:
  """Parse .hdr file for metadata."""
  def __init__(self, fileName):
    self.__file = open(fileName)
    # compile some regular expressions
    self.MatchReStruct = re.compile('[\s\{\}\(\)=";]')
    self.MatchReArray = re.compile('[,\s\{\(\);]')
    #Parse the HDR file
    self.hdr = self.parseStructure()
    self.num_regions = int(self.hdr['ScanDefinition']['Regions'][0])
    self.num_channels = int(self.hdr['Channels'][0])
    self.file_path, self.file_ext = splitext(fileName)
    self.data_size = self.parse_DataSize()
    self.data_names = self.parseDataNames()
    self.__file.close()


#----------------------------------------------------------------------
  def parseStructure(self):
    """.hdr files consist of structures and arrays. This routine sorts through the structure parts."""
    Structure = {}
    BuildWord=''
    BeforeEq=True
    QuotedWord=False
    raw = self.__file.read(1)
    while len(raw) > 0:#until we reach the end of the file
      matched = self.MatchReStruct.match(raw)
      if matched == None:
        BuildWord+=raw
      elif matched.group() == '"':
        QuotedWord= not QuotedWord
      elif QuotedWord==True:
        BuildWord+=raw
      elif matched.group() == '=':
        FieldName=BuildWord
        BuildWord=''
        BeforeEq=False
      elif matched.group() == ';':
        Structure[FieldName]=BuildWord
        BuildWord=''
        BeforeEq=True
      elif matched.group() == '{':
        #Must be after =
        BuildWord = self.parseStructure()
      elif matched.group() == '}':
        #break loop and return dictionary
        break
      elif matched.group() == '(':
        #Must be after =
        BuildWord= self.parseArray()
      elif matched.group() == ')':
        #This should not happen
        print ') in structure'
      raw = self.__file.read(1)
    return Structure
  
#----------------------------------------------------------------------
  def parseArray(self):
    """.hdr files consist of structures and arrays. This rountine sorts through the array parts."""
    Array = []
    BuildWord=''
    raw = self.__file.read(1)
    while len(raw) > 0:#until we reach the end of the file
      matched = self.MatchReArray.match(raw)
      if matched == None:
        BuildWord+=raw
      elif matched.group() == ',':
        if len(BuildWord) > 0:
          Array.append(BuildWord)
          BuildWord=''
      elif matched.group() == ';':
        print '; in array'
      elif matched.group() == '{':
        Array.append(self.parseStructure())
      elif matched.group() == '(':
        Array.append(self.parseArray())
      elif matched.group() == ')':
        if len(BuildWord) > 0:
          Array.append(BuildWord)
        break
      raw = self.__file.read(1)
    return Array
  
#----------------------------------------------------------------------
  def parseDataNames(self):
    """Figure out names for the .xsp or .xim files that contain the actual data, then check that the files actually exist, printing warnings if they don't."""
    DataNames = []#Regions
    DataNames2 = []#Channels
    DataNames3 = []#Energies
    Alphabet = 'abcdefghijklmnopqrstuvwxyz'
    DataFlag = self.hdr['ScanDefinition']['Flags']
    if DataFlag in ['Spectra','Multi-Region Spectra']:
      for num_R in range(self.num_regions):
        DataNames2 = []
        for num_Ch in range(self.num_channels):
          DataNames2.append([self.file_path+'_'+str(num_R)+'.xsp'])
        DataNames.append(DataNames2)
    elif DataFlag == 'Image':
      DataNames2 = []
      for num_Ch in range(self.num_channels):
        DataNames2.append([self.file_path+'_'+Alphabet[num_Ch]+'.xim'])
      DataNames.append(DataNames2)
    elif DataFlag == 'Multi-Region Image':
      for num_R in range(self.num_regions):
        DataNames2 = []
        for num_Ch in range(self.num_channels):
          DataNames2.append([self.file_path+'_'+Alphabet[num_Ch]+str(num_R)+'.xim'])
        DataNames.append(DataNames2)
    elif DataFlag == 'Image Stack':
      DataNames2 = []
      for num_Ch in range(self.num_channels):
        DataNames3 = []
        for num_E in range(self.data_size[0][2]):
          DataNames3.append(self.file_path+'_'+Alphabet[num_Ch]+str(num_E).zfill(3)+'.xim')
        DataNames2.append(DataNames3)
      DataNames = [DataNames2]
    else:
      print "WARNING! Unknown flag:", DataFlag
    for num_R in range(len(DataNames)):#Check that names correspond to existing files
      for num_Ch in range(len(DataNames[num_R])):
        for num_E in range(len(DataNames[num_R][num_Ch])):
          if exists(DataNames[num_R][num_Ch][num_E]) == False:
            print "WARNING! Data file doesn't exist:", DataNames[num_R][num_Ch][num_E]
    return DataNames
 
#----------------------------------------------------------------------
  def parse_DataSize(self):
    """Calculate data array size. This is useful for making sure all of the lists of data are the correct length."""
    DataSize = []
    for R_num in range(self.num_regions):
      DataSize.append([1,1,1])# [PAxis,QAxis,StackAxis] (switch to [X1,X2,E] later)]
      DataSize[R_num][0] = int(self.hdr['ScanDefinition']['Regions'][R_num+1]['PAxis']['Points'][0])
      if 'QAxis' in self.hdr['ScanDefinition']['Regions'][R_num+1] and 'Points' in self.hdr['ScanDefinition']['Regions'][R_num+1]['QAxis']:
        DataSize[R_num][1] = int(self.hdr['ScanDefinition']['Regions'][R_num+1]['QAxis']['Points'][0])
      if 'StackAxis' in self.hdr['ScanDefinition'] and 'Points' in self.hdr['ScanDefinition']['StackAxis']:
        DataSize[R_num][2] = int(self.hdr['ScanDefinition']['StackAxis']['Points'][0])
      if self.hdr['ScanDefinition']['Type'] in ['NEXAFS Point Scan','NEXAFS Line Scan']:
        DataSize[R_num] = [DataSize[R_num][1],1,DataSize[R_num][0]]#switch to [X1,X2,E] format
#        DataSize[R_num] = [1,DataSize[R_num][1],DataSize[R_num][0]]#also works, but might be problematic for finding number of spatial points
    return DataSize




#----------------------------------------------------------------------
#----------------------------------------------------------------------
class sdfstk:
    def __init__(self):
        pass
    
#----------------------------------------------------------------------
    def read_sdf(self, filename):
        HDR = HDR_FileParser(filename)
        
        if HDR.hdr['ScanDefinition']['Flags'] == 'Image Stack':
            if HDR.num_regions > 1:
                if HDR.num_channels > 1:
                    print "Only first region and first detector data will be loaded."
                else:
                    print "Only first region will be loaded."
            elif HDR.num_channels > 1:
                print "Only first detector data will be loaded."

            self.x_dist = numpy.array([float(i) for i in HDR.hdr['ScanDefinition']['Regions'][1]['PAxis']['Points'][1:] ])
            self.y_dist = numpy.array([float(i) for i in HDR.hdr['ScanDefinition']['Regions'][1]['QAxis']['Points'][1:] ])
            self.ev = numpy.array([float(i) for i in HDR.hdr['ScanDefinition']['StackAxis']['Points'][1:] ])

            self.n_cols = numpy.array(len(self.y_dist))
            self.n_rows = numpy.array(len(self.x_dist))
            self.n_ev = numpy.array(len(self.ev))

            msec = float(HDR.hdr['ScanDefinition']['Dwell'])
            self.data_dwell = numpy.ones((self.n_ev))*msec

            imagestack = numpy.empty((self.n_cols,self.n_rows,self.n_ev), numpy.int32)
            for i in range(len(HDR.data_names[0][0])):
                imagestack[:,:,i] = numpy.loadtxt(HDR.data_names[0][0][i], numpy.int32)

            self.absdata = numpy.empty((self.n_cols, self.n_rows, self.n_ev))

            self.absdata = numpy.reshape(imagestack, (self.n_cols, self.n_rows, self.n_ev), order='F')       

            self.original_n_cols = self.n_cols.copy()
            self.original_n_rows = self.n_rows.copy()
            self.original_n_ev = self.n_ev.copy()
            self.original_ev = self.ev.copy()
            self.original_absdata = self.absdata.copy()
        else:
            print "Only Image Stack files are supported."
      
        return
    
#----------------------------------------------------------------------
    def read_sdf_i0(self, filename):
        HDR = HDR_FileParser(filename)
        
        if 'ScanType' in HDR.hdr['ScanDefinition'] and HDR.hdr['ScanDefinition']['ScanType'] == 'Spectra':
            Energies = HDR.hdr['ScanDefinition']['Regions'][1]['PAxis']['Points'][1:]
            tempimage = numpy.loadtxt(HDR.data_names[0][0][0], numpy.float32)
            Data = tempimage[:,1]
        elif HDR.hdr['ScanDefinition']['Type'] == 'NEXAFS Line Scan':
            Energies = HDR.hdr['ScanDefinition']['Regions'][1]['PAxis']['Points'][1:]
            tempimage = numpy.loadtxt(HDR.data_names[0][0][0], numpy.int32)
            Data = numpy.mean(tempimage,axis=0)
        else:# Image Stack
            Energies = HDR.hdr['ScanDefinition']['StackAxis']['Points'][1:]
            tempimage = numpy.empty((HDR.data_size[0][0],HDR.data_size[0][1]), numpy.int32)
            Data = numpy.empty((HDR.data_size[0][2]), numpy.int32)
            for i in range(len(HDR.data_names[0][0])):
                tempimage = numpy.loadtxt(HDR.data_names[0][0][i], numpy.int32)
                Data[i] = numpy.mean(tempimage)

        
        msec = float(HDR.hdr['ScanDefinition']['Dwell'])#shouldn't this be needed?
        self.i0_dwell = msec
        self.evi0 = numpy.array([float(i) for i in Energies])
        self.i0data = Data                
        return
