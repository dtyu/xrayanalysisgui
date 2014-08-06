function [XRMinfo, XRM_img]=loadXANES_XRM(XRMfilename)
XRMfilename
[info,err,errmsg] = freadss(XRMfilename{2}, ...
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
XRMinfo.ImgHeight = info{1};
XRMinfo.PixelSize = info{2};
XRMinfo.ImagesTaken = length(XRMfilename)-1;
Energy_temp = info{4};
XRMinfo.Energy = zeros(XRMinfo.ImagesTaken, 1);
XRMinfo.Position = info{5};
XRMinfo.RefXShift = int8(info{6});
XRMinfo.RefYShift = int8(info{7});

XRM_img = uint16(zeros(XRMinfo.ImgHeight, XRMinfo.ImgHeight, XRMinfo.ImagesTaken));

for i=1:XRMinfo.ImagesTaken
    i
    XRMinfo.ImgHeight
    %folder = num2str(fix(double(i-1)/100)+1);
    
    [img,err,errmsg] = freadss(XRMfilename{i+1}, ...
        {'ImageData1\Image1','PositionInfo\MotorPositions'}, ...
        {'uint16', 'single'});
    %size(img)
XRM_img_temp(:,:,i) = rot90(reshape(img{1}, XRMinfo.ImgHeight, XRMinfo.ImgHeight));
XRMinfo.Position = img{2};
XRMinfo.Energy_temp(i) = XRMinfo.Position(36:43:end);
end
XRMinfo.Energy_temp = XRMinfo.Energy_temp';
[XRMinfo.Energy,I] = sort(XRMinfo.Energy_temp);
for j = 1:size(XRM_img_temp,3)
    XRM_img(:,:,j) = XRM_img_temp(:,:,I(j));
end
