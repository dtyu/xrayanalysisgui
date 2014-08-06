% for 2 references 
function [min_R, index, fRGB] = fit2D_2refs(scale_spec_ref1, scale_spec_ref2, scale_imgEstack, res)
%spectrum fitting pixel by pixel
% debug mode
%load('Cu_CuO_Cu2O_E8960_9040eV_natlog.mat');
%load('scale_imgEstack.mat');

% initializing the reference matrix 
matrix_ref1 = scale_imgEstack;
matrix_ref2 = scale_imgEstack;
  
% use matrix operation to do the fitting
numE = size(scale_spec_ref1(:));
%step = 5; %resolution of the fitting
step = res

numE
for i=1:numE  
    matrix_ref1(:,:,i) = scale_spec_ref1(i);
    matrix_ref2(:,:,i) = scale_spec_ref2(i);
end

% brute force fitting process
total = 100/step + 1;
factor1 = [0:step:100]';
fRGB = double([factor1, 100-factor1])/100;
fRGB = [fRGB, zeros(total,1)];
sum_sqdata = sum(scale_imgEstack.*scale_imgEstack,3);
[imgW, imgH, energyN] = size(scale_imgEstack);
R_ref = zeros(imgW, imgH, total);

for i=1:total
    i
    matrix_ref_com = fRGB(i,1)*matrix_ref1 + fRGB(i,2)*matrix_ref2; %linear combination of ref1-2  
    sqr =(scale_imgEstack - matrix_ref_com).*(scale_imgEstack - matrix_ref_com);
    
    R_ref(:,:,i) = sum(sqr,3)./sum_sqdata;

end

[min_R,index] = min(R_ref,[], 3);
fRGB = vertcat([0 0 0], fRGB);
index = index + 1;

end

