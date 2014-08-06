% for three references
function [min_R, index, fRGB] = fit2D_3refs(scale_spec_ref1, scale_spec_ref2, scale_spec_ref3, scale_imgEstack, res)
%spectrum fitting pixel by pixel
% debug mode
%load('Cu_CuO_Cu2O_E8960_9040eV_natlog.mat');
%load('scale_imgEstack.mat');

% initializing the reference matrix 
matrix_ref1 = scale_imgEstack;
matrix_ref2 = scale_imgEstack;
matrix_ref3 = scale_imgEstack;
  
% use matrix operation to do the fitting
numE = size(scale_spec_ref1(:));
%step = 10; %resolution of the fitting
step = res;

for i=1:numE  
    matrix_ref1(:,:,i) = scale_spec_ref1(i);
    matrix_ref2(:,:,i) = scale_spec_ref2(i);
    matrix_ref3(:,:,i) = scale_spec_ref3(i);
end

% brute force fitting process 
max = 100/step;

nchoosek_top = max + 2;
total = nchoosek(nchoosek_top, 2);

RGB = ones(total,3);

factor1 = 0;
factor2 = 0;


for i=1:total

    RGB(i,1) = max - factor1;
    RGB(i,2) = max - RGB(i,1)- factor2; 
    RGB(i,3) = max - RGB(i,1)- RGB(i,2);
    
    factor2 = factor2+1;

    if RGB(i,2) == 0; 
        factor1 = factor1+1;
        factor2 = 0;
    end
    
            
end

fRGB = double(RGB)*step/100; %fRGB = fraction
clear RGB;
sum_sqdata = sum(scale_imgEstack.*scale_imgEstack,3);
[imgW, imgH, energyN] = size(scale_imgEstack);
R_ref = zeros(imgW, imgH, total);

for i=1:total
    i
    matrix_ref_com = fRGB(i,1)*matrix_ref1 + fRGB(i,2)*matrix_ref2 + fRGB(i,3)*matrix_ref3; %linear combination of ref1-3  
    sqr =(scale_imgEstack - matrix_ref_com).*(scale_imgEstack - matrix_ref_com);
  
    R_ref(:,:,i) = sum(sqr,3)./sum_sqdata;

end

[min_R,index] = min(R_ref,[], 3);

fRGB = vertcat([0 0 0], fRGB);
index = index + 1;

end

