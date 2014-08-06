%loadXANES TXRM file for beamline X8C
%Yu-chen Karen Chen-Wiegart, March 14 2013
%freadss function is created by Matthew Kidd and is freely available on
%MatLab file Exchange

%information need: energy, image size, pixel size


%TXRMfilename = 'C:\X8Cdata\016_XANES_test\20130305_002_LFPNo2_XANES9_sam1_aftercycle_relax.txrm'


function [TXRMinfo, TXRM_img]=loadXANESTXRM(TXRMfilename)

%this is the synthax for using freadss; you may edit the fields and
%relating data type for your own interests


[info,err,errmsg] = freadss(TXRMfilename, ...
    {'ImageInfo\ImageHeight', ... %1
     'ImageInfo\PixelSize', ... %2
     'ImageInfo\ImagesTaken', ... %3
     'ImageInfo\Energy',...%4
     'PositionInfo\MotorPositions', ... %5
     'Alignment\ReferenceXShifts', ... %6
     'Alignment\ReferenceYShifts' ... %7
   }, ... 
   {'uint32', 'uint32', 'uint32', 'single', 'single', 'single', 'single'}); 

% %simply re-save the sdata into readable variables
% 
TXRMinfo.ImgHeight = info{1};
TXRMinfo.PixelSize = info{2};
TXRMinfo.ImagesTaken = info{3};
Energy_temp = info{4};
TXRMinfo.Energy = zeros(TXRMinfo.ImagesTaken, 1);
TXRMinfo.Position = info{5};
TXRMinfo.RefXShift = int8(info{6});
TXRMinfo.RefYShift = int8(info{7});


TXRMinfo.Energy = TXRMinfo.Position(36:43:end);

% for i=1:TXRMinfo.ImagesTaken
% %TXRMinfo.Energy(i) = Energy_temp(1+(i-1)*10);
% TXRMinfo.Energy(i) = Energy_temp(i)
% end

TXRM_img = uint16(zeros(TXRMinfo.ImgHeight, TXRMinfo.ImgHeight, TXRMinfo.ImagesTaken));

for i=1:TXRMinfo.ImagesTaken

% [img,err,errmsg] = freadss(TXRMfilename, ...
%     {['ImageData1\Image' int2str(i)]}, ...
%     {'uint16'});

    i
    folder = num2str(fix(double(i-1)/100)+1)
    
    [img,err,errmsg] = freadss(TXRMfilename, ...
        {['ImageData' folder '\Image' int2str(i)]}, ...
        {'uint16'});
    

% size(img{1})
% size(TXRM_img(:,:,i))
TXRM_img(:,:,i) = rot90(reshape(img{1}, TXRMinfo.ImgHeight, TXRMinfo.ImgHeight));

end

%to display the image using imtool
% img = rot90(reshape(info{5},ImgHeight, ImgHeight));

% for i=1:5:ImagesTaken
% imtool(TXRM_img(:,:,i), [0 1000])
% end

end

