function varargout = X8C_XANES_2Dfitting_v8(varargin)

% X8C_XANES_2DFITTING_V8 MATLAB code for X8C_XANES_spectrum_.fig
%      X8C_XANES_2DFITTING_V8, by itself, creates a new X8C_XANES_2DFITTING_V8 or raises the existing
%      singleton*.
%
%      H = X8C_XANES_2DFITTING_V8 returns the handle to a new X8C_XANES_2DFITTING_V8 or the handle to
%      the existing singleton*.
%
%      X8C_XANES_2DFITTING_V8('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in X8C_XANES_2DFITTING_V8.M with the given input arguments.
%
%      X8C_XANES_2DFITTING_V8('Property','Value',...) creates a new X8C_XANES_2DFITTING_V8 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before X8C_XANES_2Dfitting_v8_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to X8C_XANES_2Dfitting_v8_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help X8C_XANES_2Dfitting_v8

% Last Modified by GUIDE v2.5 11-Apr-2014 17:24:52

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @X8C_XANES_2Dfitting_v8_OpeningFcn, ...
    'gui_OutputFcn',  @X8C_XANES_2Dfitting_v8_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before X8C_XANES_2Dfitting_v8 is made visible.
function X8C_XANES_2Dfitting_v8_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to X8C_XANES_2Dfitting_v8 (see VARARGIN)
hold on;
% Choose default command line output for X8C_XANES_2Dfitting_v8
handles.output = hObject;
% Wei Xu: useful initialization field
handles.refcounter = 0; % reference number
handles.scale_imgEstack = []; % sample spectrum
handles.index = []; % fitting result
handles.fitted = false; % fitting flag
handles.filter = [];
handles.MaxRfilter = [];
handles.usrbin = 1;
handles.binobject = false;

handles.ref1plot = false;
handles.ref2plot = false;
handles.ref3plot = false;

handles.prealignment = false;

handles.samTxrmFmt = true;
handles.bkgTxrmFmt = true;

handles.numEdgeStart = 20;
handles.numEdgeEnd = 25;

handles.scale_min = 0.0
handles.scale_max = 100.0

handles.bulkSpePlot = [];
handles.ExpoBulk = false;

handles.numPreEstartLine = [];
handles.numPreEendLine = [];

handles.numPostEstartLine = [];
handles.numPostEendLine = [];

handles.EdgeStartLine = [];
handles.EdgeEndLine = [];

handles.edgePoint = [];
handles.preLine = [];
handles.postLine = [];

handles.baselinePlot = [];
handles.baseline = [];

handles.FitStartLine = [];
handles.FitEndLine = [];

handles.sample = [];
handles.originalSample = [];
handles.ref1Spec = [];
handles.ref2Spec = [];
handles.ref3Spec = [];

handles.showNorm = false
handles.fitcurvLine = [];
handles.ShowNormPts = false;
handles.RawBkg = [];
handles.ShowNormBulk = false;

handles.UseBaseNorm = true;
handles.RminValue = 0.0;
handles.numSmoothPts = 1.0;
handles.scaleByDefault = true;
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes X8C_XANES_2Dfitting_v8 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = X8C_XANES_2Dfitting_v8_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in button_load_XANES.
function button_load_XANES_Callback(hObject, eventdata, handles)
% hObject    handle to button_load_XANES (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%
% handles.EdgeStartLine = [];
% handles.EdgeEndLine = [];

if handles.samTxrmFmt
    [handles.XANESFileName,handles.PathName,handles.FilterIndex] = ...
        uigetfile('*.txrm','Select the TXM XANES file stack');
    
else
    [handles.XANESFileName,handles.PathName,handles.FilterIndex] = ...
        uigetfile('*.xrm','Select any TXM XANES file within the target directory');
end

set(handles.text_XANES_filename,'String',[handles.PathName handles.XANESFileName]);
set(handles.status_bkgnorm,'String', 'Status: none');
set(handles.resolution, 'String', '5')
handles.res = 5

cd(handles.PathName)

guidata(hObject,handles);


% --- Executes on button press in button_load_BKG.
function button_load_BKG_Callback(hObject, eventdata, handles)
% hObject    handle to button_load_BKG (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if handles.bkgTxrmFmt
    [handles.BKGFileName,handles.BKGPathName,handles.FilterIndex] = ...
        uigetfile('*.txrm','Select the TXM XANES background file stack');
    
else
    [handles.BKGFileName,handles.BKGPathName,handles.FilterIndex] = ...
        uigetfile('*.xrm','Select any TXM XANES file within the target directory');
end

set(handles.text_BKG_filename,'String',[handles.BKGPathName handles.BKGFileName]);
set(handles.status_bkgnorm,'String', 'Status: none');
cd(handles.BKGPathName)

guidata(hObject,handles);

% --- Executes on button press in export_spectra.
function export_spectra_Callback(hObject, eventdata, handles)
% hObject    handle to export_spectra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%load the XANES .txrm file
%load the background .txrm file

%pixel by pixel normalization
%XANES/BKG

%spectrum normalization
%for each pixel, normalize the spectrum using the first 5 and last five;
%also ensure to export the log scale

%export each pixel into a ATHENA format text

[pathstr, name, ext] = fileparts(handles.XANESFileName)
set(handles.status_expXANES,'String','Status: running');
fid = fopen([handles.PathName name '_x' num2str(handles.x) '_y' num2str(handles.y) '_bin' num2str(handles.usrbin) '.txt'], 'wt')
num_img = handles.ImagesTaken

fprintf(fid, '        Energy            I0            It            Ir\n')


% for i=1:num_img
% fprintf(fid, '%14.5f%14.4f%14.4f\n', handles.Energy(i), ...
%     handles.bkg(handles.y, handles.x, i), ...
%     handles.img(handles.y, handles.x, i) )
% end

%%%%%%%%%%%%%%%%%%Binning!!%%%%%%%%%%%%%%%%%
ROI=handles.usrbin

if ROI > 1
    ROI_hsize = (ROI-1)/2 %ROI's half size
    
    a=1
    point_spectrum_bkg = zeros(handles.ImagesTaken, ROI*ROI);
    point_spectrum_img = zeros(handles.ImagesTaken, ROI*ROI);
    
    for j = -ROI_hsize:ROI_hsize
        for k = -ROI_hsize:ROI_hsize
            
            point_spectrum_bkg(:,a) = squeeze(handles.bkg(handles.y+j,handles.x+k, :));   %squeeze is to reduce the matrix dimension
            point_spectrum_img(:,a) = squeeze(handles.img(handles.y+j,handles.x+k, :));
            a = a+1;
        end
    end
    
    print_bkg_spectrum =mean(point_spectrum_bkg');
    print_img_spectrum =mean(point_spectrum_img');
    
else
    print_bkg_spectrum = reshape(handles.bkg(handles.y,handles.x,:),1,handles.ImagesTaken);
    print_img_spectrum = reshape(handles.img(handles.y,handles.x,:),1,handles.ImagesTaken);
    %    spectrum = squeeze(imgEstack(pointx,pointy, :))   %squeeze is to reduce the matrix dimension
end




for i=1:num_img
    fprintf(fid, '%14.5f%14.4f%14.4f\n', handles.Energy(i), ...
        print_bkg_spectrum(i), ...
        print_img_spectrum(i));
end

fclose(fid);

set(handles.status_expXANES,'String','Status: complete');

%export an image identify the x and y (0, 0)




%FUTURE STEPs:
%display XANES image during normalization
%seperate different steps and say "ok", etc.


% --- Executes on slider movement.
function slider_img_Callback(hObject, eventdata, handles)
% hObject    handle to slider_img (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider

% Ensure model is open.
% model_open(handles)
% Get the new value for the Kf Gain from the slider.

currentSliderStep = uint8(get(hObject, 'Value'))

% Set the value of the KfCurrentValue to the new value
% set by slider.
set(handles.slider_img,'Value',currentSliderStep);
set(handles.current_img,'String', num2str(currentSliderStep));
axes(handles.axes1);
imshow(handles.imgEstack(:,:,currentSliderStep), [handles.scale_min/100*255 handles.scale_max/100*255]);


% --- Executes during object creation, after setting all properties.
function slider_img_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_img (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in back_normal.
function back_normal_Callback(hObject, eventdata, handles)
% hObject    handle to back_normal (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if ~isempty(handles.edgePoint)
    delete(handles.edgePoint)
end

if ~isempty(handles.preLine)
    delete(handles.preLine)
end

if ~isempty(handles.postLine)
    delete(handles.postLine)
end




%future: seperate the load function - load the image and then load the
%background images

% reset previous refult
handles.filter = [];
handles.fitted = false;
handles.fitcurvLine = [];
% if ~isempty(handles.fitcurvLine)
%     delete(handles.fitcurvLine)
% end

set(handles.status_bkgnorm,'String', 'Status: running');
drawnow;
%information need: energy, image size, pixel size

if handles.samTxrmFmt
    img_fn = [handles.PathName handles.XANESFileName];  %XANES image file name
    [img_info, handles.img] = loadXANESTXRM(img_fn);
else
    imgdir = handles.PathName
    prefix = inputdlg('Enter the sample file name prefix:', 'Sample File');
    Ei = inputdlg('Enter the sample initial energy:', 'Sample File');
    Estep = inputdlg('Enter the sample energy step:', 'Sample File');
    Ef = inputdlg('Enter the sample final energy:', 'Sample File');
    ending = inputdlg('Enter the sample file name ending:', 'Sample File');
    [img_info, handles.img] = loadXANESMultiXRM(imgdir, prefix{:}, Ei{:}, Estep{:}, Ef{:}, ending{:});
end

if handles.bkgTxrmFmt
    bkg_fn = [handles.BKGPathName handles.BKGFileName];  %XANES image file name
    [bkg_info, handles.bkg] = loadXANESTXRM(bkg_fn);
else
    bkgdir = handles.BKGPathName
    bkgprefix = inputdlg('Enter the background file name prefix:', 'Background File');
    bkgEi = inputdlg('Enter the background initial energy:', 'Background File');
    bkgEstep = inputdlg('Enter the background energy step:', 'Background File');
    bkgEf = inputdlg('Enter the background final energy:', 'Background File');
    bkgending = inputdlg('Enter the background file name ending:', 'Background File');
    [bkg_info, handles.bkg] = loadXANESMultiXRM(bkgdir, bkgprefix{:}, bkgEi{:}, bkgEstep{:}, bkgEf{:}, bkgending{:});
end


handles.ImagesTaken = img_info.ImagesTaken
handles.Energy = img_info.Energy
handles.imgBin = 2048/(img_info.ImgHeight)
handles.imgHeight = img_info.ImgHeight

handles.x = img_info.ImgHeight/2
handles.y = img_info.ImgHeight/2
set(handles.x_cord,'String',num2str(handles.ImagesTaken/2));
set(handles.y_cord,'String',num2str(handles.ImagesTaken/2));

set(handles.PostEstart,'String',num2str(handles.ImagesTaken/2));
set(handles.PostEend,'String',num2str(handles.ImagesTaken-10));
handles.numPostEstart = handles.ImagesTaken/2
handles.numPostEend = handles.ImagesTaken

% %      handles.RefXShift = img_info.RefXShift
% %      handles.RefYShift = img_info.RefYShift

%add condition if shift is required by users

%if shift is off
%      handles.img = img
%      handles.bkg = bkg


%if shift is on:
if handles.prealignment
    % %      for i=1:handles.ImagesTaken
    % %      a= [-img_info.RefYShift(i), img_info.RefXShift(i)]
    % %
    % %      handles.img(:,:,i) = circshift(img(:,:,i), double(a))  %(y x)
    % %      handles.bkg(:,:,i) = circshift(bkg(:,:,i), double(a))
    % %      end
    
    for i=1:handles.ImagesTaken
        a= [-img_info.RefYShift(i), img_info.RefXShift(i)]
        
        handles.img(:,:,i) = circshift(handles.img(:,:,i), double(a))  %(y x)
        handles.bkg(:,:,i) = circshift(handles.bkg(:,:,i), double(a))
    end
    
end


%background normalization
scaleimg = double(handles.img)./double(handles.bkg);
handles.imgEstack = uint8(scaleimg.*255);
clear handles.img
clear handles.bkg


%%display the normalized image
axes(handles.axes1)
imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);

Min = 1;
Max = handles.ImagesTaken;

sliderStep = [1.0 1.0]./double(Max) ; % major and minor steps of 1 %need to fix the 50!!!!!!

set(handles.slider_img, 'Min', Min);
set(handles.slider_img, 'Max', Max);
set(handles.slider_img, 'SliderStep', sliderStep);
set(handles.slider_img, 'Value', Max); % set to beginning of sequence

set(handles.current_img,'String', num2str(Max));
set(handles.total_img,'String', ['/' num2str(Max)]);


th = str2double(get(handles.edit_edge_jump,'String'));
prepostEdgeDiff = handles.imgEstack(:,:,1) - handles.imgEstack(:,:,end);  %calculate the difference of below/above edge
handles.filter = prepostEdgeDiff >= th ;

%%%%%%%%%%%%%%%%%%%%for users who use Athena, they'll do this part in Athena themselves anyways...%%%%%%%%%%%%%%%%%%5
%spectra scaling
%% natural log scaling
ln_imgEstack = -log(scaleimg);  %negative sign: mu1t1+mu2t2+mu3t3
clear scaleimg
handles.ln_imgEstack = single(ln_imgEstack);


%% XANES scaling

handles.scale_imgEstack = handles.ln_imgEstack

% scale_0 = mean(ln_imgEstack(:,:,1:5),3);
% %scale_1 = mean(ln_imgEstack(:,:,end-4:end),3);
% handles.numPEpts
% scale_1 = mean(ln_imgEstack(:,:,end-handles.numPEpts:end),3);
% scale_1(130,91)
%
% expand_scale_0 = ln_imgEstack;
% clear ln_imgEstack
%
% %expand_scale_1 = ln_imgEstack;
% expand_scale_1 = expand_scale_0;
% handles.scale_imgEstack = expand_scale_0;
%
% for i=1:img_info.ImagesTaken
%     expand_scale_0(:,:,i) = scale_0;
%     expand_scale_1(:,:,i) = scale_1;
% end
%
% %handles.scale_imgEstack = (ln_imgEstack - expand_scale_0)./(expand_scale_1-expand_scale_0);
% handles.scale_imgEstack = handles.scale_imgEstack - expand_scale_0;
% expand_scale_1 = expand_scale_1 - expand_scale_0;
% clear expand_scale_0
% handles.scale_imgEstack = handles.scale_imgEstack./expand_scale_1;
% clear expand_scale_1


%pass to fitting program: handles.scale_imgEstack


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%interest pixel location
%%next step: need to be able to identify the specific pixel by clicking on the image
%      handles.interest_pixel_x = 712;
%      handles.interest_pixel_y = 854;
%
%
%      %extract the spectrum from the specific location
%
%      %ln_imgEstack_pixel = reshape(ln_imgEstack(interest_pixel_y,interest_pixel_x,:),1,img_info.ImagesTaken)
%      handles.scale_imgEstack_pixel = reshape(handles.scale_imgEstack(handles.interest_pixel_y,handles.interest_pixel_x,:),1,img_info.ImagesTaken)
%
%      %display the spectrum
%      axes(handles.axes2)
%      %plot(img_info.Energy, ln_imgEstack_pixel)
%      plot(img_info.Energy, handles.scale_imgEstack_pixel)

%handles.usrbin = 1
set(handles.bin, 'String', num2str(handles.usrbin));
set(handles.status_bkgnorm,'String', 'Status: complete');

guidata(hObject,handles);


% --- Executes on button press in select_point.
function select_point_Callback(hObject, eventdata, handles)
% hObject    handle to select_point (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[x, y] = ginput(1);

% axes(handles.axes1);
% if handles.fitted
%     if isempty(handles.filter)
%         imshow(handles.index, handles.fRGB);
%     else
%         imshow(handles.index.*handles.filter, handles.fRGB);
%     end
% else
%     if isempty(handles.filter)
%         imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);
%     else
%         imshow(handles.imgEstack(:,:,handles.ImagesTaken).*handles.filter, [handles.scale_min/100*255 handles.scale_max/100*255]);
%     end
% end
%
% line([x-20 x+20], [y y], 'LineWidth',1.5,'Color',[1 0.5 0]);
% line([x x], [y-20 y+20], 'LineWidth',1.5,'Color',[1 0.5 0]);
% % w = handles.usrbin/2;
% % rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 0.5 0]);
%
% w = handles.usrbin;
% rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 1 0]);

handles.x = uint16(x);
handles.y = uint16(y);
% [handles.x, handles.y] = uint16([x, y])

redraw(handles);

set(handles.x_cord,'String', num2str(handles.x));
set(handles.y_cord,'String', num2str(handles.y));

%----------check here----------------
%handles.usrbin = 1;
set(handles.bin, 'String', num2str(handles.usrbin));

guidata(hObject,handles);


function bin_Callback(hObject, eventdata, handles)
% hObject    handle to bin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bin as text
%        str2double(get(hObject,'String')) returns contents of bin as a double

handles.usrbin = str2num(get(hObject,'String'));
redraw(handles);
guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function bin_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in update.
function update_Callback(hObject, eventdata, handles)
% hObject    handle to update (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% handles.EdgeStartLine = [];
% handles.EdgeEndLine = [];

%extract the spectrum from the specific location

%ln_imgEstack_pixel = reshape(ln_imgEstack(interest_pixel_y,interest_pixel_x,:),1,img_info.ImagesTaken)

if ~isempty(handles.sample)
    delete(handles.sample)
    handles.sample = []
end

if ~isempty(handles.originalSample)
    delete(handles.originalSample)
    handles.originalSample = []
end
ROI=handles.usrbin;

if handles.ShowNormPts
    plotting = 'ShowNormPoint'
    ShowValue = handles.ShowNormPoint
    handles.scale_imgEstack_pixel = reshape(handles.scale_imgEstack(handles.y,handles.x, :),1,handles.ImagesTaken);
    
    if ROI > 1
        ROI_hsize = (ROI-1)/2; %ROI's half size
        
        a=1;
        point_spectrum = zeros(handles.ImagesTaken, ROI*ROI);
        
        for j = -ROI_hsize:ROI_hsize
            for k = -ROI_hsize:ROI_hsize
                
                point_spectrum(:,a) = squeeze(handles.scale_imgEstack(handles.y+j,handles.x+k, :));   %squeeze is to reduce the matrix dimension
                a = a+1;
            end
        end
        
        handles.scale_imgEstack_pixel = mean(point_spectrum');
        
        
    else
        handles.scale_imgEstack_pixel = reshape(handles.scale_imgEstack(handles.y,handles.x,:),1,handles.ImagesTaken);
        %    spectrum = squeeze(imgEstack(pointx,pointy, :))   %squeeze is to reduce the matrix dimension
    end
    
    if handles.numSmoothPts ~= 1
        windowSize = handles.numSmoothPts;  %e.g. windowSize = 5
        groupDelay = double(floor(windowSize/2));   %e.g. groupDelay = 2
        %LastEnergies = ones(1,groupDelay)   %e.g. 1:2
        
       
        
        handles.scale_imgEstack_pixel = filter(ones(1,groupDelay+1)/windowSize,1,handles.scale_imgEstack_pixel)...
                                        + flipdim(filter(ones(1,groupDelay+1)/windowSize,1,flipdim(handles.scale_imgEstack_pixel,2)),2)...
                                        - handles.scale_imgEstack_pixel/windowSize
%         handles.scale_imgEstack_pixel = (filter(ones(1,groupDelay)/groupDelay,1,handles.scale_imgEstack_pixel)...
%                                         + flipdim(filter(ones(1,groupDelay)/groupDelay,1,flipdim(handles.scale_imgEstack_pixel,2)),2)...
%                                         - handles.scale_imgEstack_pixel/groupDelay)*groupDelay/windowSize
        
        
        %handles.scale_imgEstack_pixel = [handles.scale_imgEstack_pixel(groupDelay+1:end) zeros(1,groupDelay)];
        
        
        %handles.scale_imgEstack_pixel = [handles.scale_imgEstack_pixel(groupDelay+1:end) LastEnergies];
        
        %fdata = filter(ones(1,windowSize)/windowSize, 1, data);
        %f2data = [fdata(groupDelay+1:end); zeros(groupDelay,1)];
        
        
        %             
        
        %span = handles.numSmoothPts; % Size of the averaging window
%         %window = ones(span,1)/span;
%         window = ones(span,1);
%         handles.scale_imgEstack_pixel = convn(handles.scale_imgEstack_pixel,window,'same');
%         
        
    end


    
    %display the spectrum
    axes(handles.axes2);
    %plot(img_info.Energy, ln_imgEstack_pixel)
    %actLegend = []
    
    handles.sample = plot(handles.Energy, handles.scale_imgEstack_pixel, 'k');
    
    %actLegend = [actLegend; {'sample'}]
    
    %%%%if user wants to show the original spectrum also (not only showing the
    %%%%normalized one)
else
    plotting = 'Original pixel'
    ShowValue = handles.ShowNormPoint
    Original_pixel = reshape(handles.ln_imgEstack(handles.y,handles.x, :),1,handles.ImagesTaken);
    
    %handles.scale_imgEstack_pixel = reshape(handles.scale_imgEstack(handles.y,handles.x, :),1,handles.ImagesTaken);
    
    if ROI > 1
        ROI_hsize = (ROI-1)/2; %ROI's half size
        
        a=1;
        point_spectrum = zeros(handles.ImagesTaken, ROI*ROI);
        
        for j = -ROI_hsize:ROI_hsize
            for k = -ROI_hsize:ROI_hsize
                
                point_spectrum(:,a) = squeeze(handles.ln_imgEstack(handles.y+j,handles.x+k, :));   %squeeze is to reduce the matrix dimension
                a = a+1;
            end
        end
        
        handles.Original_pixel = mean(point_spectrum');
        
        
    else
        handles.Original_pixel = reshape(handles.ln_imgEstack(handles.y,handles.x,:),1,handles.ImagesTaken);
    end
    
    axes(handles.axes2);
    handles.originalSample = plot(handles.Energy, handles.Original_pixel, 'k-');
    
end

if handles.ref1plot
    if ~isempty(handles.ref1Spec)
        delete(handles.ref1Spec)
    end
    
    handles.ref1Spec = plot(handles.ref1all(1,:), handles.ref1, 'r');
    set(handles.ref1Spec,'Visible','on');
    %actLegend = [actLegend; {'ref1'}]
elseif ~isempty(handles.ref1Spec)
    set(handles.ref1Spec,'Visible','off');
end

if handles.ref2plot
    if ~isempty(handles.ref2Spec)
        delete(handles.ref2Spec)
    end
    
    handles.ref2Spec = plot(handles.ref2all(1,:), handles.ref2, 'g');
    set(handles.ref2Spec,'Visible','on');
    %actLegend = [actLegend; {'ref2'}]
elseif ~isempty(handles.ref2Spec)
    set(handles.ref2Spec,'Visible','off');
end

if handles.ref3plot
    if ~isempty(handles.ref3Spec)
        delete(handles.ref3Spec)
    end
    
    handles.ref3Spec = plot(handles.ref3all(1,:), handles.ref3, 'b');
    set(handles.ref3Spec,'Visible','on');
    %actLegend = [actLegend; {'ref3'}]
elseif ~isempty(handles.ref3Spec)
    set(handles.ref3Spec,'Visible','off');
    
end




% if handles.ref1plot
%     handles.ref1Spec = plot(handles.ref1all(1,:), handles.ref1, 'r');
%     %actLegend = [actLegend; {'ref1'}]
% elseif ~isempty(handles.ref1Spec)
%         delete(handles.ref1Spec)
%         handles.ref1Spec = []
% end
%
% if handles.ref2plot
%
%     handles.ref2Spec = plot(handles.ref2all(1,:), handles.ref2, 'g');
%     %actLegend = [actLegend; {'ref2'}]
% elseif ~isempty(handles.ref2Spec)
%         delete(handles.ref2Spec)
%         handles.ref2Spec = []
% end
%
% if handles.ref3plot
%     handles.ref3Spec = plot(handles.ref3all(1,:), handles.ref3, 'b');
%     %actLegend = [actLegend; {'ref3'}]
% elseif ~isempty(handles.ref3Spec)
%         delete(handles.ref3Spec)
%         handles.ref3Spec = []
%
% end

if ~isempty(handles.fitcurvLine)
    delete(handles.fitcurvLine)
end

if handles.fitted
    ff = handles.fRGB(handles.index(handles.y,handles.x), :);
    R = handles.min_R(handles.y,handles.x)
    if handles.refcounter == 3
        handles.fittedcurve = ff(1)*handles.ref1 + ff(2)*handles.ref2 + ff(3)*handles.ref3;
        strleg = [num2str(int16(ff(1)*100)), '%, ', num2str(int16(ff(2)*100)), '%, ', num2str(int16(ff(3)*100)), '%', ...
            ' R value = ', num2str(R)];
    end
    if handles.refcounter == 2
        handles.fittedcurve = ff(1)*handles.ref1 + ff(2)*handles.ref2;
        strleg = [num2str(int16(ff(1)*100)), '%, ', num2str(int16(ff(2)*100)), '%', ...
            'R value = ', num2str(R)];
    end
    handles.fitcurvLine = plot(handles.Energy, handles.fittedcurve, 'Color', [0.7 0.4 1], 'LineWidth', 2, 'LineStyle', ':');
    %    actLegend = [actLegend; {strleg}]
    legend(strleg, 'location', 'SouthEast')
    
end

%legend(actLegend, 'location', 'SouthEast')



xlabel('Energy (eV)');
ylabel('Normalized \mu t');

%!!!!!!!!!! plot: check reference plot or not!!!!!
%!!!!!!!!!! need to save the spectrum
guidata(hObject,handles);



function current_img_Callback(hObject, eventdata, handles)
% hObject    handle to current_img (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of current_img as text
%        str2double(get(hObject,'String')) returns contents of current_img as a double


user_current_img = get(hObject,'String');
set(handles.slider_img, 'Value', str2num(user_current_img));
axes(handles.axes1);
imshow(handles.imgEstack(:,:,str2num(user_current_img)), [handles.scale_min/100*255 handles.scale_max/100*255]);



% --- Executes during object creation, after setting all properties.
function current_img_CreateFcn(hObject, eventdata, handles)
% hObject    handle to current_img (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_scale_min_Callback(hObject, eventdata, handles)
% hObject    handle to edit_scale_min (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_scale_min as text
%        str2double(get(hObject,'String')) returns contents of edit_scale_min as a double

handles.scale_min = str2double(get(hObject, 'String'));

axes(handles.axes1);
imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);

guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function edit_scale_min_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_scale_min (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit_scale_max_Callback(hObject, eventdata, handles)
% hObject    handle to edit_scale_max (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_scale_max as text
%        str2double(get(hObject,'String')) returns contents of edit_scale_max as a double


handles.scale_max = str2double(get(hObject, 'String'));

axes(handles.axes1);
imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);

guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function edit_scale_max_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_scale_max (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


%for future:
%1. show where the crusor is: impixelinfo
%2. input the coordinate by typing the number


% --- Executes on button press in save_spectrum.
function save_spectrum_Callback(hObject, eventdata, handles)
% hObject    handle to save_spectrum (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% open a dialog for user to enter a file name

if ~handles.ExpoBulk
    lineprofile = handles.scale_imgEstack_pixel;
    [file,path] = uiputfile(['SpectrumName' '_x' num2str(handles.x) '_y' num2str(handles.y)...
        '_bin' num2str(handles.usrbin) '.txt']...
        ,'Save Spectrum As');
    
else
    lineprofile = handles.bulkSpectrum;
    [file,path] = uiputfile(['SpectrumName_BulkSpectrum.txt']...
        ,'Save Spectrum As');
    
end

content = [handles.Energy; lineprofile];

%!!!!!!!!!!!!! add directory



handles.spectrum_name = [path, file];
cd(path)


%x = inputdlg('Enter the file name:', 'Save current spectrum');
%handles.spectrum_name = [x{:} '.txt'];


fid = fopen(handles.spectrum_name, 'wt');
fprintf(fid, 'Energy\tmut\n');
fprintf(fid, '%f %f\n', content);
fclose(fid);


% --- Executes on button press in pushbutton9.
function pushbutton9_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



function edit_edge_jump_Callback(hObject, eventdata, handles)
% hObject    handle to edit_edge_jump (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit_edge_jump as text
%        str2double(get(hObject,'String')) returns contents of edit_edge_jump as a double
th = str2double(get(hObject,'String'));

%th = str2double(get(handles.edit_edge_jump_Callback,'String'));

%deal with the pixels that have edge jump

prepostEdgeDiff = handles.imgEstack(:,:,1) - handles.imgEstack(:,:,end);  %calculate the difference of below/above edge
handles.filter = prepostEdgeDiff >= th ;  %logical array
redraw(handles);
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function edit_edge_jump_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit_edge_jump (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in update_image.
function update_image_Callback(hObject, eventdata, handles)
% hObject    handle to update_image (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if isempty(handles.index)
    msgbox('Please perform fitting first!');
    return
end

handles.MaxRfilter = handles.min_R <= handles.RmaxValue

axes(handles.axes1);
imshow(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB);
%imshow(handles.index.*handles.filter, handles.fRGB);

guidata(hObject,handles);

% --- Executes on button press in fitting.
function fitting_Callback(hObject, eventdata, handles)
% hObject    handle to fitting (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if handles.refcounter < 2
    msgbox('Please load enough number of references!');
    set(handles.status_expXANES,'String', 'Status: none');
    return
end

if isempty(handles.scale_imgEstack)
    msgbox('Please load sample spectrum!');
    set(handles.status_expXANES,'String', 'Status: none');
    return
end

set(handles.status_expXANES,'String', 'Status: running');
drawnow;

if handles.binobject
    h = ones(handles.usrbin);
    h = h/sum(h(:));
    [imgW, imgH, eN] = size(handles.scale_imgEstack);
    new_stack = zeros(imgW, imgH, eN);
    for e = 1:eN
        new_stack(:,:,e) = filter2(h, handles.scale_imgEstack(:,:,e));
    end
    
else
    new_stack = handles.scale_imgEstack;
end
    ori_stack = new_stack;
if handles.numSmoothPts ~= 1
    windowSize = handles.numSmoothPts;
    groupDelay = double(floor(windowSize/2));
    %new_stack = filter(ones(1,windowSize)/windowSize,1,new_stack, [], 3);

    
    new_stack = filter(ones(1,groupDelay+1)/windowSize,1,new_stack, [], 3)...
              + flipdim(filter(ones(1,groupDelay+1)/windowSize,1,flipdim(new_stack, 3), [], 3),3)...
              - new_stack/windowSize;
end

%use the entire spectrum
% if handles.refcounter == 2
%     [handles.index, handles.fRGB] = fit2D_2refs(handles.ref1, handles.ref2, new_stack, handles.res);
% else
%     [handles.index, handles.fRGB] = fit2D_3refs(handles.ref1, handles.ref2, handles.ref3, new_stack, handles.res);
% end

%use just the selected energy range

numFitStart = handles.numFitStart
numFitEnd = handles.numFitEnd


if handles.refcounter == 2
    [handles.min_R, handles.index, handles.fRGB] = fit2D_2refs(handles.ref1(numFitStart:numFitEnd), handles.ref2(numFitStart:numFitEnd), ...
        new_stack(:,:,numFitStart:numFitEnd), handles.res);
else
    [handles.min_R, handles.index, handles.fRGB] = fit2D_3refs(handles.ref1(numFitStart:numFitEnd), handles.ref2(numFitStart:numFitEnd),...
        handles.ref3(numFitStart:numFitEnd), new_stack(:,:,numFitStart:numFitEnd), handles.res);
end

handles.fitted = true;

axes(handles.axes1);
imshow(handles.index, handles.fRGB);

set(handles.status_expXANES,'String', 'Status: complete');

guidata(hObject,handles);

% --- Executes on button press in load_ref2.
function load_ref2_Callback(hObject, eventdata, handles)
% hObject    handle to load_ref2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[handles.Ref2FileName,handles.Ref2PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
cd(handles.Ref2PathName)

set(handles.ref2name,'String',handles.Ref2FileName);
drawnow

% count the number of references
handles.refcounter = 2;

ref2n = [handles.Ref2PathName handles.Ref2FileName];
fid2 = fopen(ref2n, 'rt');
line = fgets(fid2);
handles.ref2all = fscanf(fid2, '%f %f', [2 inf]);
handles.ref2 = handles.ref2all(2,:);
fclose(fid2);
%
% axes(handles.axes2);
% plot(handles.ref2all(1,:), handles.ref2, 'g');
% hold on;

guidata(hObject,handles);

% --- Executes on button press in load_ref3.
function load_ref3_Callback(hObject, eventdata, handles)
% hObject    handle to load_ref3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[handles.Ref3FileName,handles.Ref3PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
cd(handles.Ref3PathName)
set(handles.ref3name,'String',handles.Ref3FileName);
drawnow

% count the number of references
handles.refcounter = 3;

ref3n = [handles.Ref3PathName handles.Ref3FileName];
fid3 = fopen(ref3n, 'rt');
line = fgets(fid3);
handles.ref3all = fscanf(fid3, '%f %f', [2 inf]);
handles.ref3 = handles.ref3all(2,:);
fclose(fid3);

% axes(handles.axes2);
% plot(handles.ref3all(1,:), handles.ref3, 'b');
% hold on;

guidata(hObject,handles);

% --- Executes on button press in load_ref1.
function load_ref1_Callback(hObject, eventdata, handles)
% hObject    handle to load_ref1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[handles.Ref1FileName,handles.Ref1PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
cd(handles.Ref1PathName)

set(handles.ref1name,'String',handles.Ref1FileName);
drawnow

% count the number of references
handles.refcounter = 1;

ref1n = [handles.Ref1PathName handles.Ref1FileName];
fid1 = fopen(ref1n, 'rt');
line = fgets(fid1);
handles.ref1all = fscanf(fid1, '%f %f', [2 inf]);
handles.ref1 = handles.ref1all(2,:);
fclose(fid1);

% axes(handles.axes2);
% plot(handles.ref1all(1,:), handles.ref1, 'r');
% hold on;

guidata(hObject,handles);

% --- Executes on button press in check_spectrum.
function check_spectrum_Callback(hObject, eventdata, handles)
% hObject    handle to check_spectrum (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
img_fn = [handles.PathName handles.XANESFileName];
msg = ['Please notice the current sample file is:' img_fn];
msgbox(msg);

% --- Executes on button press in save_fitted.
function save_fitted_Callback(hObject, eventdata, handles)
% hObject    handle to save_fitted (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%x = inputdlg('Enter the file name:', 'Save the fitting result');
%imwrite(handles.index.*handles.filter, handles.fRGB, [x{:} '.tif']);

[file,path] = uiputfile('FittedResult.tif','Save Fitted Result As');
cd(path)

imwrite(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB, [path, file]);


% --- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox1

if get(hObject, 'Value')
    handles.ref1plot = true
else
    handles.ref1plot = false
end

guidata(hObject,handles);

% --- Executes on button press in checkbox2.
function checkbox2_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox2

if get(hObject, 'Value')
    handles.ref2plot = true
else
    handles.ref2plot = false
end

guidata(hObject,handles);

% --- Executes on button press in checkbox3.
function checkbox3_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox3


if get(hObject, 'Value')
    handles.ref3plot = true
else
    handles.ref3plot = false
end

guidata(hObject,handles);


% --- Executes on button press in samTxrm.
function samTxrm_Callback(hObject, eventdata, handles)
% hObject    handle to samTxrm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of samTxrm

if get(hObject, 'Value')
    set(handles.samXrm, 'Value', 0)
    handles.samTxrmFmt = true  %sample data is in txrm format
else
    set(handles.samXrm, 'Value', 1)
    handles.samTxrmFmt = false  %sample data is in xrm format
end

guidata(hObject, handles)




% --- Executes on button press in bkgTxrm.
function bkgTxrm_Callback(hObject, eventdata, handles)
% hObject    handle to bkgTxrm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of bkgTxrm

if get(hObject, 'Value')
    set(handles.bkgXrm, 'Value', 0)
    handles.bkgTxrmFmt = true  %bkg data is in txrm format
else
    set(handles.bkgXrm, 'Value', 1)
    handles.bkgTxrmFmt = false  %bkg data is in xrm format
end

guidata(hObject, handles)


% --- Executes on button press in samXrm.
function samXrm_Callback(hObject, eventdata, handles)
% hObject    handle to samXrm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of samXrm

if get(hObject, 'Value')
    set(handles.samTxrm, 'Value', 0)
    handles.samTxrmFmt = false
else
    set(handles.samTxrm, 'Value', 1)
    handles.samTxrmFmt = true
end

guidata(hObject, handles)


% --- Executes on button press in bkgXrm.
function bkgXrm_Callback(hObject, eventdata, handles)
% hObject    handle to bkgXrm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of bkgXrm

if get(hObject, 'Value')
    set(handles.bkgTxrm, 'Value', 0)
    handles.bkgTxrmFmt = false
else
    set(handles.bkgTxrm, 'Value', 1)
    handles.bkgTxrmFmt = true
end

guidata(hObject, handles)


% --- Executes on button press in SaveSpecturmFig.
function SaveSpecturmFig_Callback(hObject, eventdata, handles)
% hObject    handle to SaveSpecturmFig (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[file,path] = uiputfile(['SpectrumName_x' num2str(handles.x) '_y' num2str(handles.y)...
    '_bin' num2str(handles.usrbin) '.tif']...
    ,'Save Spectrum Figure As');
%
%     F=getframe(handles.axes2); %select axes in GUI
%     figure(); %new figure
%     image(F.cdata); %show selected axes in new figure
%     saveas(gcf, [path file]); %save figure
%     close(gcf); %and close it

export_fig(handles.axes2, [path file]);



function resolution_Callback(hObject, eventdata, handles)
% hObject    handle to resolution (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



% Hints: get(hObject,'String') returns contents of resolution as text
%        str2double(get(hObject,'String')) returns contents of resolution as a double


handles.res = str2double(get(hObject, 'String'));
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function resolution_CreateFcn(hObject, eventdata, handles)
% hObject    handle to resolution (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in bin_object.
function bin_object_Callback(hObject, eventdata, handles)
% hObject    handle to bin_object (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of bin_object
if get(hObject,'Value')
    handles.binobject = true;
else
    handles.binobject = false;
end
guidata(hObject,handles);


% --- Executes on button press in checkbox_prealignment.
function checkbox_prealignment_Callback(hObject, eventdata, handles)
%%
% hObject    handle to checkbox_prealignment (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if get(hObject, 'Value')
    handles.prealignment = true
else
    handles.prealignment = false
end
guidata(hObject,handles);

% Hint: get(hObject,'Value') returns toggle state of checkbox_prealignment


% --- Executes on button press in bulk_spec.
function bulk_spec_Callback(hObject, eventdata, handles)
% hObject    handle to bulk_spec (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% handles.preLine = []
% handles.postLine = []
% handles.edgePoint = []

hold on
if ~isempty(handles.bulkSpePlot)
    delete(handles.bulkSpePlot)
end

if ~handles.ShowNormBulk
    squeezed_ln_imgEstack = reshape(handles.ln_imgEstack, [handles.imgHeight*handles.imgHeight, handles.ImagesTaken]);
    point_spectrum = squeezed_ln_imgEstack(handles.filter, :);
    
else
    squeezed_ln_imgEstack = reshape(handles.scale_imgEstack, [handles.imgHeight*handles.imgHeight, handles.ImagesTaken]);
    
    
    point_spectrum = squeezed_ln_imgEstack(handles.filter, :);
    
end

handles.bulkSpectrum=mean(point_spectrum);
axes(handles.axes2);
handles.bulkSpePlot = plot(handles.Energy, handles.bulkSpectrum, 'm');


handles.numPreEstart = uint8(str2double(get(handles.PreEstart,'String')));
handles.numPreEstartLine = addline(handles, handles.numPreEstartLine, ...
    handles.numPreEstart, 'c-');

handles.numPreEend = uint8(str2double(get(handles.PreEend,'String')));
handles.numPreEendLine = addline(handles, handles.numPreEendLine, ...
    handles.numPreEend, 'b--');


handles.numPostEstart = uint8(str2double(get(handles.PostEstart,'String')));
handles.numPostEstartLine = addline(handles, handles.numPostEstartLine, ...
    handles.numPostEstart, 'm-');

handles.numPostEend = uint8(str2double(get(handles.PostEend,'String')));
handles.numPostEendLine = addline(handles, handles.numPostEendLine, ...
    handles.numPostEend, 'r--');


handles.numEdgeStart = uint8(str2double(get(handles.EdgeStart,'String')));
handles.EdgeStartLine = addline(handles, handles.EdgeStartLine, ...
    handles.numEdgeStart, 'y-');

handles.numEdgeEnd = uint8(str2double(get(handles.EdgeEnd,'String')));
handles.EdgeEndLine = addline(handles, handles.EdgeEndLine, ...
    handles.numEdgeEnd, 'g--');

guidata(hObject,handles);




function redraw(handles)
axes(handles.axes1);
if handles.fitted
    if isempty(handles.filter)
        if isempty(handles.MaxRfilter)
            imshow(handles.index, handles.fRGB);
        else
            imshow(handles.index.*handles.MaxRfilter, handles.fRGB);
        end
    else
        if isempty(handles.MaxRfilter)
            imshow(handles.index.*handles.filter, handles.fRGB);
        else
            imshow(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB);
        end
    end
else
    if isempty(handles.filter)
        imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);
    else
        %toshow = handles.imgEstack(:,:,handles.ImagesTaken)
        %imshow(toshow(handles.filter), [handles.scale_min/100*255 handles.scale_max/100*255]);
        imshow(handles.imgEstack(:,:,handles.ImagesTaken).*uint8(handles.filter), [handles.scale_min/100*255 handles.scale_max/100*255]);
    end
end

x = handles.x;
y = handles.y;

line([x-20 x+20], [y y], 'LineWidth',1.5,'Color',[1 0.5 0]);
line([x x], [y-20 y+20], 'LineWidth',1.5,'Color',[1 0.5 0]);

w = handles.usrbin;
rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 1 0]);



function x_cord_Callback(hObject, eventdata, handles)
% hObject    handle to x_cord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of x_cord as text
%        str2double(get(hObject,'String')) returns contents of x_cord as a double

handles.x = str2num(get(hObject,'String'));
redraw(handles);
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function x_cord_CreateFcn(hObject, eventdata, handles)
% hObject    handle to x_cord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function y_cord_Callback(hObject, eventdata, handles)
% hObject    handle to y_cord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.y = str2num(get(hObject,'String'));
redraw(handles);
guidata(hObject,handles);

% Hints: get(hObject,'String') returns contents of y_cord as text
%        str2double(get(hObject,'String')) returns contents of y_cord as a double


% --- Executes during object creation, after setting all properties.
function y_cord_CreateFcn(hObject, eventdata, handles)
% hObject    handle to y_cord (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function PreEstart_Callback(hObject, eventdata, handles)
% hObject    handle to PreEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%handles.numpreEstart = str2num(get(hObject,'String'));


handles.numPreEstart = uint8(str2double(get(hObject,'String')));
handles.numPreEstartLine = addline(handles, handles.numPreEstartLine, ...
    handles.numPreEstart, 'c-');


guidata(hObject,handles);


% Hints: get(hObject,'String') returns contents of PreEstart as text
%        str2double(get(hObject,'String')) returns contents of PreEstart as a double


% --- Executes during object creation, after setting all properties.
function PreEstart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PreEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function PreEend_Callback(hObject, eventdata, handles)
% hObject    handle to PreEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of PreEend as text
%        str2double(get(hObject,'String')) returns contents of PreEend as a double

handles.numPreEend = uint8(str2double(get(hObject,'String')));
handles.numPreEendLine = addline(handles, handles.numPreEendLine, ...
    handles.numPreEend, 'b--');

guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function PreEend_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PreEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
    
    
    
end



function PostEstart_Callback(hObject, eventdata, handles)
% hObject    handle to PostEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of PostEstart as text
%        str2double(get(hObject,'String')) returns contents of PostEstart as a double

%handles.numPostEstart = str2num(get(hObject,'String'));

handles.numPostEstart = uint8(str2double(get(hObject,'String')));
handles.numPostEstartLine = addline(handles, handles.numPostEstartLine, ...
    handles.numPostEstart, 'm-');

guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function PostEstart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PostEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function PostEend_Callback(hObject, eventdata, handles)
% hObject    handle to PostEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of PostEend as text
%        str2double(get(hObject,'String')) returns contents of PostEend as a double

handles.numPostEend = uint8(str2double(get(hObject,'String')));
handles.numPostEendLine = addline(handles, handles.numPostEendLine, ...
    handles.numPostEend, 'r--');


guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function PostEend_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PostEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function EdgeStart_Callback(hObject, eventdata, handles)
% hObject    handle to EdgeStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of EdgeStart as text
%        str2double(get(hObject,'String')) returns contents of EdgeStart as a double

% if ~isempty(handles.EdgeStartLine)
%     delete(handles.EdgeStartLine)
% end

handles.numEdgeStart = uint8(str2double(get(hObject,'String')));
handles.EdgeStartLine = addline(handles, handles.EdgeStartLine, ...
    handles.numEdgeStart, 'y-');
%syntax for addline:
%newLineHandle = addline(handles, currentLineHandle, currentEvalue, color)

guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function EdgeStart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to EdgeStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function EdgeEnd_Callback(hObject, eventdata, handles)
% hObject    handle to EdgeEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of EdgeEnd as text
%        str2double(get(hObject,'String')) returns contents of EdgeEnd as a double
%
% if ~isempty(handles.EdgeEndLine)
%     delete(handles.EdgeEndLine)
% end

handles.numEdgeEnd = uint8(str2double(get(hObject,'String')));
handles.EdgeEndLine = addline(handles, handles.EdgeEndLine, ...
    handles.numEdgeEnd, 'g--');

guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function EdgeEnd_CreateFcn(hObject, eventdata, handles)
% hObject    handle to EdgeEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in norm_spec.
function norm_spec_Callback(hObject, eventdata, handles)
% hObject    handle to norm_spec (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


%pseudo-code: for each point:
% pre = polyfit(handles.Energy(3:10),spec(3:10),1)
% post = polyfit(E(end-50:end),spec(end-50:end),1)
%
% preE0 = handles.pre(1)*e0+pre(2)
% postE0 = post(1)*E0+post(2)
% postE0 = post(1)*e0+post(2)
% edgeDiff = postE0 - preE0
% normSpec = spec-pre(1)*E+pre(2)
% norm2Spec=normSpec./edgeDiff
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
set(handles.XANESnormStatus,'String','Status: running');
drawnow;

handles.scale_imgEstack = handles.ln_imgEstack;

if handles.UseBaseNorm
    
    if isempty(handles.baseline)
        msgbox('use "Fit Base Line" to set the baseline first')
        set(handles.XANESnormStatus,'String','Status: none');
        return
    end
    
    for i=1:handles.ImagesTaken
        handles.scale_imgEstack(:,:,i) = handles.scale_imgEstack(:,:,i)- handles.baseline(i)
    end
    
    if handles.scaleByDefault
        ScalingMethod = 'default'
        scale_0 = mean(handles.scale_imgEstack(:,:,1:5),3);
        scale_1 = mean(handles.scale_imgEstack(:,:,end-4:end),3);
        
    else
        ScalingMethod = 'user define'
        ZeroStart = handles.numPreEstart
        ZeroEnd = handles.numPreEend
        OneStart = handles.numPostEstart
        OneEnd = handles.numPostEend

        scale_0 = mean(handles.scale_imgEstack(:,:,ZeroStart:ZeroEnd),3);
        scale_1 = mean(handles.scale_imgEstack(:,:,OneStart:OneEnd),3);
        
    end
    
    expand_scale_0 = handles.scale_imgEstack;
    expand_scale_1 = handles.scale_imgEstack;
    
    for i=1:handles.ImagesTaken
        expand_scale_0(:,:,i) = scale_0;
        expand_scale_1(:,:,i) = scale_1;
    end
    
    handles.scale_imgEstack = (handles.scale_imgEstack - expand_scale_0)./(expand_scale_1-expand_scale_0);
    
    
else if handles.UseRawBkg
        
        if isempty(handles.RawBkg)
            msgbox('use "Set as Raw Bkg" to set a spectrum as the raw background first')
            set(handles.XANESnormStatus,'String','Status: none');
            return
        end
            
        for i=1:handles.ImagesTaken
            handles.scale_imgEstack(:,:,i) = handles.scale_imgEstack(:,:,i)- handles.RawBkg(i)
        end
        
        if handles.scaleByDefault
            ScalingMethod = 'default'
            scale_0 = mean(handles.scale_imgEstack(:,:,1:5),3);
            scale_1 = mean(handles.scale_imgEstack(:,:,end-4:end),3);
            
        else
            ScalingMethod = 'user define'
            ZeroStart = handles.numPreEstart
            ZeroEnd = handles.numPreEend
            OneStart = handles.numPostEstart
            OneEnd = handles.numPostEend
            
            scale_0 = mean(handles.scale_imgEstack(:,:,ZeroStart:ZeroEnd),3);
            scale_1 = mean(handles.scale_imgEstack(:,:,OneStart:OneEnd),3);
            
        end
        
        expand_scale_0 = handles.scale_imgEstack;
        expand_scale_1 = handles.scale_imgEstack;
        
        for i=1:handles.ImagesTaken
            expand_scale_0(:,:,i) = scale_0;
            expand_scale_1(:,:,i) = scale_1;
        end
        
        handles.scale_imgEstack = (handles.scale_imgEstack - expand_scale_0)./(expand_scale_1-expand_scale_0);
        
        
        
    else % if choosing using hte pre/post-edge normalization
        
        E0 = handles.Energy(handles.E0);
        warning('off','all');
        
        pre = [0 0];
        
        for i=1:handles.imgHeight
            for j=1:handles.imgHeight
                if (handles.filter(i,j))
                    
                    spec = handles.ln_imgEstack(i,j,:);
                    spec = spec(:)';
                    
                    %option1: fitted with linear line at pre-edge
                    %  pre = polyfit(...
                    %      handles.Energy(handles.numPreEstart:handles.numPreEend),...
                    %      spec(handles.numPreEstart:handles.numPreEend),1);
                    
                    
                    pre(2) = mean(spec(handles.numPreEstart:handles.numPreEend));
                    
                    post = polyfit(...
                        handles.Energy(handles.numPostEstart:handles.numPostEend),...
                        spec(handles.numPostEstart:handles.numPostEend),1);
                    
                    preE0 = pre(1)*E0+pre(2);
                    postE0 = post(1)*E0+post(2);
                    edgeDiff = postE0 - preE0;
                    
                    handles.scale_imgEstack(i,j,:) = ...
                        (spec-(pre(1)*handles.Energy+pre(2)))./edgeDiff;
                else
                    handles.scale_imgEstack(i,j,:) = zeros(size(handles.scale_imgEstack(i,j,:)));
                end
            end
        end
        
        warning('on','all');
        
    end
end

set(handles.XANESnormStatus,'String','Status: complete');
set(handles.ShowNormPoint, 'Enable', 'on');
set(handles.ShowNormPoint, 'Value', true);
handles.ShowNormPts = true;

set(handles.ShowNormBulkSpec, 'Enable', 'on');
set(handles.SmoothPts, 'Enable', 'on');

%%%%%%%%%%%%%%%%%%%%%!!!!!!!!!!!!!!!!!

% handles.numFitStart = uint8(str2double(get(handles.FitStart,'String')));
% handles.FitStartLine = addline(handles, handles.FitStartLine, ...
%     handles.numFitStart, 'k-');
%
% handles.numFitEnd = uint8(str2double(get(handles.FitEnd,'String')));
% handles.FitEndLine = addline(handles, handles.FitEndLine, ...
%     handles.numFitEnd, 'k--');

guidata(hObject,handles);


function newLineHandle = addline(handles, currentLineHandle, currentEvalue, colorNlinestyle)
axes(handles.axes2);
hold on
if ~isempty(currentLineHandle)
    delete(currentLineHandle)
end

linex(1:2) = handles.Energy(currentEvalue)
liney(1:2) = [min(handles.bulkSpectrum),max(handles.bulkSpectrum)]
newLineHandle = plot(linex,liney, colorNlinestyle);  %# Create a line with PLOT


% %%%%%%%%%%%%%%%%%%%%%%
% hLine = plot(...);  %# Create a line with PLOT
% delete(hLine);      %# ...and delete it
% %Alternatively, if you didn't save the handle in a variable, you can search for it using FINDOBJ, then delete it when you find it.
%
% %If you don't actually want to delete it, but simply turn the visibility of the line on and off, you can set the 'Visible' property of the graphics object accordingly:
%
% set(hLine,'Visible','off');  %# Make it invisible
% set(hLine,'Visible','on');   %# Make it visible


% --- Executes on button press in PreEdgeSet.
function PreEdgeSet_Callback(hObject, eventdata, handles)
% hObject    handle to PreEdgeSet (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if ~isempty(handles.preLine)
    delete(handles.preLine)
end

%option1: linear fitting
handles.pre = polyfit(handles.Energy(handles.numPreEstart:handles.numPreEend),...
    handles.bulkSpectrum(handles.numPreEstart:handles.numPreEend),1)

%option2: just straight line
%  spec = handles.bulkSpectrum(:)
%  handles.pre = [0 0]
%  handles.pre(1) = 0
%  handles.pre(2) = mean(spec(handles.numPreEstart:handles.numPreEend))
%

%%need to be modified
handles.preLine = plot(handles.Energy, ...
    handles.pre(1)*handles.Energy+handles.pre(2), 'c--')

guidata(hObject,handles);



% --- Executes on button press in PostEdgeSet.
function PostEdgeSet_Callback(hObject, eventdata, handles)
% hObject    handle to PostEdgeSet (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%handles.postLine = []

if ~isempty(handles.postLine)
    delete(handles.postLine)
end

handles.post = polyfit(handles.Energy(handles.numPostEstart:handles.numPostEend),...
    handles.bulkSpectrum(handles.numPostEstart:handles.numPostEend),1)
handles.postLine = plot(handles.Energy, ...
    handles.post(1)*handles.Energy+handles.post(2), 'm--')
guidata(hObject,handles)

% --- Executes on button press in EdgeSet.
function EdgeSet_Callback(hObject, eventdata, handles)
% hObject    handle to EdgeSet (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


if ~isempty(handles.edgePoint)
    delete(handles.edgePoint)
end

%handles.edge = polyfit(handles.Energy(handles.numEdgeStart:handles.numEdgeEnd),...
%    handles.bulkSpectrum(handles.numEdgeStart:handles.numEdgeEnd),1)
%handles.edgePoint = plot(handles.Energy, handles.edge(1)*handles.Energy+handles.edge(2), 'c--')

handles.E0 = uint8((handles.numEdgeStart+handles.numEdgeEnd)./2)
handles.edgePoint = plot(handles.Energy(handles.E0), handles.bulkSpectrum(handles.E0), 'gx')
guidata(hObject,handles)

%handles.edgeLine = []


% --- Executes on button press in ShowNormBulkSpec.
function ShowNormBulkSpec_Callback(hObject, eventdata, handles)
% hObject    handle to ShowNormBulkSpec (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of ShowNormBulkSpec
if get(hObject, 'Value')
    handles.ShowNormBulk = true
else
    handles.ShowNormBulk = false
end
guidata(hObject,handles);


% --- Executes on button press in exportBulk.
function exportBulk_Callback(hObject, eventdata, handles)
% hObject    handle to exportBulk (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of exportBulk

if get(hObject, 'Value')
    handles.ExpoBulk = true
else
    handles.ExpoBulk = false
end

guidata(hObject,handles);


% --- Executes on button press in ShowNormPoint.
function ShowNormPoint_Callback(hObject, eventdata, handles)
% hObject    handle to ShowNormPoint (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if get(hObject, 'Value')
    handles.ShowNormPts = true
    set(handles.SmoothPts, 'Enable', 'on');
else
    handles.ShowNormPts = false
    set(handles.SmoothPts, 'Enable', 'off');
end
guidata(hObject,handles);

% Hint: get(hObject,'Value') returns toggle state of ShowNormPoint



function FitStart_Callback(hObject, eventdata, handles)
% hObject    handle to FitStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of FitStart as text
%        str2double(get(hObject,'String')) returns contents of FitStart as a double

handles.numFitStart = uint8(str2double(get(hObject,'String')));
handles.FitStartLine = addline(handles, handles.FitStartLine, ...
    handles.numFitStart, 'k-');
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function FitStart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to FitStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function FitEnd_Callback(hObject, eventdata, handles)
% hObject    handle to FitEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of FitEnd as text
%        str2double(get(hObject,'String')) returns contents of FitEnd as a double
handles.numFitEnd = uint8(str2double(get(hObject,'String')));
handles.FitEndLine = addline(handles, handles.FitEndLine, ...
    handles.numFitEnd, 'k-');
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function FitEnd_CreateFcn(hObject, eventdata, handles)
% hObject    handle to FitEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in BaseLineNorm.
function BaseLineNorm_Callback(hObject, eventdata, handles)
% hObject    handle to BaseLineNorm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of BaseLineNorm

if get(hObject, 'Value')
    set(handles.EdgeNorm, 'Value', 0)
    set(handles.RawBkgNorm, 'Value', 0)
    handles.UseBaseNorm = true
    handles.UseRawBkg = false   
    set(handles.DefaultScaling, 'Enable', 'on')
    drawnow;
% else
%     set(handles.EdgeNorm, 'Value', 1)
%     handles.UseBaseNorm = false
%         
%     drawnow;
end
guidata(hObject, handles)



% --- Executes on button press in RawBkgNorm.
function RawBkgNorm_Callback(hObject, eventdata, handles)
% hObject    handle to RawBkgNorm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of RawBkgNorm

if get(hObject, 'Value')
    set(handles.BaseLineNorm, 'Value', 0)
    set(handles.EdgeNorm, 'Value', 0)
    handles.UseBaseNorm = false
    handles.UseRawBkg = true   
    set(handles.DefaultScaling, 'Enable', 'on')
    drawnow;
% else
%     set(handles.BaseLineNorm, 'Value', 1)
%     handles.UseBaseNorm = true
%     drawnow;
end

guidata(hObject,handles);

% --- Executes on button press in EdgeNorm.
function EdgeNorm_Callback(hObject, eventdata, handles)
% hObject    handle to EdgeNorm (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of EdgeNorm
if get(hObject, 'Value')
    set(handles.BaseLineNorm, 'Value', 0)
    set(handles.RawBkgNorm, 'Value', 0)
    handles.UseBaseNorm = false
    handles.UseRawBkg = false   
    set(handles.DefaultScaling, 'Enable', 'off')
    drawnow;
% else
%     set(handles.BaseLineNorm, 'Value', 1)
%     handles.UseBaseNorm = true
%     drawnow;
end
guidata(hObject, handles)

% --- Executes on button press in FitBaseLine.
function FitBaseLine_Callback(hObject, eventdata, handles)
% hObject    handle to FitBaseLine (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%handles.Energy
%
%base = polyfit(handles.Energy,handles.scale_imgEstack_pixel,1);
base = polyfit(handles.Energy,handles.Original_pixel,1);

handles.baseline = base(1)*handles.Energy + base(2);


if ~isempty(handles.baselinePlot)
    delete(handles.baselinePlot)
end
handles.baselinePlot = plot(handles.Energy, handles.baseline, 'g--')

guidata(hObject,handles);

% --- Executes on button press in SetBaseLine.


function Rmax_Callback(hObject, eventdata, handles)
% hObject    handle to Rmax (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Rmax as text
%        str2double(get(hObject,'String')) returns contents of Rmax as a double

handles.RmaxValue = str2double(get(hObject,'String'))
handles.MaxRfilter = handles.min_R <= handles.RmaxValue
redraw(handles);
guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function Rmax_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Rmax (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in SetRawBkg.
function SetRawBkg_Callback(hObject, eventdata, handles)
% hObject    handle to SetRawBkg (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.RawBkg = handles.Original_pixel
guidata(hObject,handles);


% --- Executes on button press in DefaultScaling.
function DefaultScaling_Callback(hObject, eventdata, handles)
% hObject    handle to DefaultScaling (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if get(hObject, 'Value')
    handles.scaleByDefault = true
else
    handles.scaleByDefault = false
end

guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of DefaultScaling



function SmoothPts_Callback(hObject, eventdata, handles)
% hObject    handle to SmoothPts (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of SmoothPts as text
%        str2double(get(hObject,'String')) returns contents of SmoothPts as a double

previous_numSmoothPts = handles.numSmoothPts
handles.numSmoothPts = str2double(get(hObject,'String'));

if handles.numSmoothPts < 1
    msgbox ('Number of points must be >= 1')
    set (handles.SmoothPts, 'String', num2str(uint8(previous_numSmoothPts)))
    handles.numSmoothPts = previous_numSmoothPts
    return
end

if rem(handles.numSmoothPts, 2) == 0
    handles.numSmoothPts = handles.numSmoothPts - 1
end




guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function SmoothPts_CreateFcn(hObject, eventdata, handles)
% hObject    handle to SmoothPts (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in BaseLineZero.
function BaseLineZero_Callback(hObject, eventdata, handles)
% hObject    handle to BaseLineZero (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

dim2 = size(handles.Energy)
handles.baseline = zeros(1, dim2(2))
guidata(hObject,handles);
