function varargout = X8C_XANE_2Dfitting_naiyun(varargin)
%X8C_XANE_2DFITTING_NAIYUN M-file for X8C_XANE_2Dfitting_naiyun.fig
%      X8C_XANE_2DFITTING_NAIYUN, by itself, creates a new X8C_XANE_2DFITTING_NAIYUN or raises the existing
%      singleton*.
%
%      H = X8C_XANE_2DFITTING_NAIYUN returns the handle to a new X8C_XANE_2DFITTING_NAIYUN or the handle to
%      the existing singleton*.
%
%      X8C_XANE_2DFITTING_NAIYUN('Property','Value',...) creates a new X8C_XANE_2DFITTING_NAIYUN using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to X8C_XANE_2Dfitting_naiyun_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      X8C_XANE_2DFITTING_NAIYUN('CALLBACK') and X8C_XANE_2DFITTING_NAIYUN('CALLBACK',hObject,...) call the
%      local function named CALLBACK in X8C_XANE_2DFITTING_NAIYUN.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help X8C_XANE_2Dfitting_naiyun

% Last Modified by GUIDE v2.5 20-Jun-2014 10:24:29

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @X8C_XANE_2Dfitting_naiyun_OpeningFcn, ...
                   'gui_OutputFcn',  @X8C_XANE_2Dfitting_naiyun_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
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


% --- Executes just before X8C_XANE_2Dfitting_naiyun is made visible.
function X8C_XANE_2Dfitting_naiyun_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for X8C_XANE_2Dfitting_naiyun
handles.output = hObject;

handles.samTxrmFmt = true;
handles.bkgTxrmFmt = true;

handles.scale_min = 0.0;
handles.scale_max = 100.0;
handles.currentSliderStep = 0;
handles.ln_imgEstack = [];
handles.scale_imgEstack_pixel = [];
handles.normbulkSpectrum = [];
handles.x = 0.0;
handles.y = 0.0;

handles.prealignment = false;
handles.usrbin = 1;
handles.res = 5;
handles.numSmoothPts = 1.0;
handles.scaleByDefault = true;
handles.refcounter = 0; 

handles.filter = [];
handles.fitted = false;
handles.fitcurvLine = [];
handles.index = [];
handles.MaxRfilter = [];

handles.Raw_Spectrum = false;
handles.Normalized_Spectrum = false;
handles.Raw_Bulk_Spectrum = false;
handles.Normalized_Bulk_Spectrum = false;
handles.Fitted_Spectrum = false;

handles.baselinePlot = [];
handles.baseline = [];
handles.baselinePlot_zero = [];
handles.baseline_zero = [];
handles.UseBaseNorm = true;
handles.select_zero = false;
handles.scale_imgEstack = [];
handles.RawBkg = [];

handles.ref1plot = false;
handles.ref2plot = false;
handles.ref3plot = false;

handles.FitStartLine = [];
handles.FitEndLine = [];

handles.PreEplot = false;
handles.PostEplot = false;
handles.EdgeEplot = false;

handles.edgePoint = [];
handles.preLine = [];
handles.postLine = [];

handles.numPreEstartLine = [];
handles.numPreEendLine = [];

handles.numPostEstartLine = [];
handles.numPostEendLine = [];

handles.EdgeStartLine = [];
handles.EdgeEndLine = [];

handles.bulkSpePlot = [];

handles.binobject = false;
handles.smoothobject = false;

handles.FitStartLine = [];
handles.FitEndLine = [];
handles.RmaxValue = 100;
handles.fitcurvLine = [];
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes X8C_XANE_2Dfitting_naiyun wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = X8C_XANE_2Dfitting_naiyun_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in samTxrm.
function samTxrm_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    set(handles.samXrm, 'Value', 0)
    handles.samTxrmFmt = true;  %sample data is in txrm format
else
    set(handles.samXrm, 'Value', 1)
    handles.samTxrmFmt = false;  %sample data is in xrm format
end
guidata(hObject, handles)


% --- Executes on button press in samXrm.
function samXrm_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    set(handles.samTxrm, 'Value', 0)
    handles.samTxrmFmt = false;
else
    set(handles.samTxrm, 'Value', 1)
    handles.samTxrmFmt = true;
end
guidata(hObject, handles)


% --- Executes on button press in button_load_XANES.
function button_load_XANES_Callback(hObject, eventdata, handles)
if handles.samTxrmFmt
    [handles.XANESFileName,handles.PathName,handles.FilterIndex] = ...
        uigetfile('*.txrm','Select the TXM XANES file stack');
    if handles.PathName == 0
        msgbox('please select txrm file!');
        return
    end
    %[folder, baseFileName, extension] = fileparts([handles.PathName handles.XANESFileName]);
	%if ~strcmpi(extension, '.txrm')
        %msgbox('wrong file type! please select txrm files!');
        %return
    %else
        set(handles.text_XANES_filename,'String',[handles.PathName handles.XANESFileName]);
   % end
else
    [handles.XANESFileName,handles.PathName,handles.FilterIndex] = ...
        uigetfile('*.xrm','Select any TXM XANES file within the target directory', 'MultiSelect', 'on');
    if handles.PathName == 0
        msgbox('please select xrm files!');
        return
    end
    %[folder, baseFileName, extension] = fileparts([handles.PathName handles.XANESFileName]);
	%if ~strcmpi(extension, '.xrm')
        %msgbox('wrong file type! please select xrm files!');
        %return
   % else
        set(handles.text_XANES_filename,'String',[handles.PathName handles.XANESFileName([1 end])]);
  %  end
end

set(handles.XANESnormStatus,'String', 'Status: none');
set(handles.resolution, 'String', '5')
cd(handles.PathName)
guidata(hObject,handles);

% --- Executes on button press in bkgTxrm.
function bkgTxrm_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    set(handles.bkgXrm, 'Value', 0)
    handles.bkgTxrmFmt = true;  %bkg data is in txrm format
else
    set(handles.bkgXrm, 'Value', 1)
    handles.bkgTxrmFmt = false;  %bkg data is in xrm format
end
guidata(hObject, handles)


% --- Executes on button press in bkgXrm.
function bkgXrm_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    set(handles.bkgTxrm, 'Value', 0)
    handles.bkgTxrmFmt = false;
else
    set(handles.bkgTxrm, 'Value', 1)
    handles.bkgTxrmFmt = true;
end
guidata(hObject, handles)


% --- Executes on button press in button_load_BKG.
function button_load_BKG_Callback(hObject, eventdata, handles)
if handles.bkgTxrmFmt
    [handles.BKGFileName,handles.BKGPathName,handles.FilterIndex] = ...
        uigetfile('*.txrm','Select the TXM XANES background file stack');
    if handles.BKGPathName == 0
        msgbox('please select txrm file!');
        return
    end
    %[folder, baseFileName, extension] = fileparts([handles.BKGPathName handles.BKGFileName]);
	%if ~strcmpi(extension, '.txrm')
       % msgbox('wrong file type! please select txrm files!');
        %return
    %else
        set(handles.text_BKG_filename,'String',[handles.BKGPathName handles.BKGFileName]);
   % end
else
    [handles.BKGFileName,handles.BKGPathName,handles.FilterIndex] = ...
        uigetfile('*.xrm','Select any TXM XANES file within the target directory', 'MultiSelect', 'on');
    if handles.BKGPathName == 0
        msgbox('please select xrm files!');
        return
    end
    %[folder, baseFileName, extension] = fileparts([handles.BKGPathName handles.BKGFileName]);
	%if ~strcmpi(extension, '.xrm')
        %msgbox('wrong file type! please select xrm files!');
        %return
    %else
        set(handles.text_BKG_filename,'String',[handles.BKGPathName handles.BKGFileName([1 end])]);
    %end
end
set(handles.XANESnormStatus,'String', 'Status: none');
set(handles.back_normal, 'Enable', 'on')
cd(handles.BKGPathName)
guidata(hObject,handles);

% --- Executes on button press in checkbox_prealignment.
function checkbox_prealignment_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    handles.prealignment = true;
else
    handles.prealignment = false;
end
guidata(hObject,handles);


% --- Executes on slider movement.
function slider_img_Callback(hObject, eventdata, handles)
handles.currentSliderStep = uint8(get(hObject, 'Value'));
set(handles.slider_img,'Value',handles.currentSliderStep);
set(handles.current_img,'String', num2str(handles.currentSliderStep));
axes(handles.axes1);
imshow(handles.imgEstack(:,:,handles.currentSliderStep), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);
freezeColors 
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function slider_img_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_img (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function slider_img_minscale_Callback(hObject, eventdata, handles)
handles.scale_min = uint8(get(hObject,'Value'));
set(handles.slider_img_minscale, 'Value', handles.scale_min);
axes(handles.axes1);
set(handles.text_minscale,'String', ['Min:' num2str(handles.scale_min) '%']);
imshow(handles.imgEstack(:,:,handles.currentSliderStep), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);
freezeColors 
guidata(hObject,handles);
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function slider_img_minscale_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_img_minscale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function slider_img_maxscale_Callback(hObject, eventdata, handles)
handles.scale_max = uint8(get(hObject,'Value'));
set(handles.slider_img_maxscale, 'Value', handles.scale_max);
axes(handles.axes1);
set(handles.text_maxscale,'String', ['Max:' num2str(handles.scale_max) '%']);
imshow(handles.imgEstack(:,:,handles.currentSliderStep), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);
freezeColors 
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function slider_img_maxscale_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider_img_maxscale (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in load_ref1.
function load_ref1_Callback(hObject, eventdata, handles)
[handles.Ref1FileName,handles.Ref1PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
if handles.Ref1PathName == 0
    msgbox('please select txt file!');
    return
end
[folder, baseFileName, extension] = fileparts([handles.Ref1PathName handles.Ref1FileName]);
if ~strcmpi(extension, '.txt')
    msgbox('wrong file type! please select txt files!');
    return
end
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

guidata(hObject,handles);


% --- Executes on button press in load_ref2.
function load_ref2_Callback(hObject, eventdata, handles)
[handles.Ref2FileName,handles.Ref2PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
if handles.Ref2PathName == 0
    msgbox('please select txt file!');
    return
end
[folder, baseFileName, extension] = fileparts([handles.Ref2PathName handles.Ref2FileName]);
if ~strcmpi(extension, '.txt')
    msgbox('wrong file type! please select txt files!');
    return
end
cd(handles.Ref2PathName)

set(handles.ref2name,'String',handles.Ref2FileName);
drawnow

handles.refcounter = 2;

ref2n = [handles.Ref2PathName handles.Ref2FileName];
fid2 = fopen(ref2n, 'rt');
line = fgets(fid2);
handles.ref2all = fscanf(fid2, '%f %f', [2 inf]);
handles.ref2 = handles.ref2all(2,:);
fclose(fid2);

guidata(hObject,handles);


% --- Executes on button press in load_ref3.
function load_ref3_Callback(hObject, eventdata, handles)
[handles.Ref3FileName,handles.Ref3PathName,handles.FilterIndex] = ...
    uigetfile('*.txt','Select the file of reference spectrum');
if handles.Ref3PathName == 0
    msgbox('please select txt file!');
    return
end
[folder, baseFileName, extension] = fileparts([handles.Ref3PathName handles.Ref3FileName]);
if ~strcmpi(extension, '.txt')
    msgbox('wrong file type! please select txt files!');
    return
end
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

guidata(hObject,handles);


function current_img_Callback(hObject, eventdata, handles)
user_current_img = get(hObject,'String');
set(handles.slider_img, 'Value', str2num(user_current_img));
handles.currentSliderStep = str2num(user_current_img);
axes(handles.axes1);
imshow(handles.imgEstack(:,:,str2num(user_current_img)), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);
freezeColors 
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of current_img as text
%        str2double(get(hObject,'String')) returns contents of current_img as a double


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


% --- Executes on button press in back_normal.
function back_normal_Callback(hObject, eventdata, handles)
set(handles.status_bkgnorm,'String', 'Status: running');
drawnow;

if handles.samTxrmFmt
    img_fn = [handles.PathName handles.XANESFileName];  %XANES image file name
    [img_info, handles.img] = loadXANESTXRM(img_fn);
else
    img_fn = [handles.PathName handles.XANESFileName];  %XANES image file name
    [img_info, handles.img] = loadXANES_XRM(img_fn);
%     imgdir = handles.PathName;
%     prefix = inputdlg('Enter the sample file name prefix:', 'Sample File');
%     Ei = inputdlg('Enter the sample initial energy:', 'Sample File');
%     Estep = inputdlg('Enter the sample energy step:', 'Sample File');
%     Ef = inputdlg('Enter the sample final energy:', 'Sample File');
%     ending = inputdlg('Enter the sample file name ending:', 'Sample File');
%     [img_info, handles.img] = loadXANESMultiXRM(imgdir, prefix{:}, Ei{:}, Estep{:}, Ef{:}, ending{:});
end

if handles.bkgTxrmFmt
    bkg_fn = [handles.BKGPathName handles.BKGFileName];  %XANES image file name
    [bkg_info, handles.bkg] = loadXANESTXRM(bkg_fn);
else
    bkg_fn = [handles.BKGPathName handles.BKGFileName];  %XANES image file name
    [bkg_info, handles.bkg] = loadXANES_XRM(bkg_fn);
%     bkgdir = handles.BKGPathName;
%     bkgprefix = inputdlg('Enter the background file name prefix:', 'Background File');
%     bkgEi = inputdlg('Enter the background initial energy:', 'Background File');
%     bkgEstep = inputdlg('Enter the background energy step:', 'Background File');
%     bkgEf = inputdlg('Enter the background final energy:', 'Background File');
%     bkgending = inputdlg('Enter the background file name ending:', 'Background File');
%     [bkg_info, handles.bkg] = loadXANESMultiXRM(bkgdir, bkgprefix{:}, bkgEi{:}, bkgEstep{:}, bkgEf{:}, bkgending{:});
end

handles.ImagesTaken = img_info.ImagesTaken;
handles.currentSliderStep = img_info.ImagesTaken;
handles.Energy = img_info.Energy;
handles.imgBin = 2048/(img_info.ImgHeight);
handles.imgHeight = img_info.ImgHeight;

handles.x = img_info.ImgHeight/2;
handles.y = img_info.ImgHeight/2;
set(handles.x_cord,'String',num2str(handles.imgHeight/2));
set(handles.y_cord,'String',num2str(handles.imgHeight/2));

%set(handles.PostEstart,'String',num2str(handles.ImagesTaken/2));
%set(handles.PostEend,'String',num2str(handles.ImagesTaken-10));
handles.numPostEstart = handles.ImagesTaken/2;
handles.numPostEend = handles.ImagesTaken;

if handles.prealignment
    for i=1:handles.ImagesTaken
        a= [-img_info.RefYShift(i), img_info.RefXShift(i)];
        handles.img(:,:,i) = circshift(handles.img(:,:,i), double(a));  %(y x)
        handles.bkg(:,:,i) = circshift(handles.bkg(:,:,i), double(a));
    end    
end

%background normalization
scaleimg = double(handles.img)./double(handles.bkg);
handles.imgEstack = uint8(scaleimg.*255);
clear handles.img
clear handles.bkg
%%display the normalized image
axes(handles.axes1)
imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255], 'InitialMagnification','fit');
colormap('gray');
freezeColors 

set(handles.slider_img,'Enable','on');
set(handles.current_img,'Enable','on');
set(handles.slider_img_minscale,'Enable','on');
set(handles.slider_img_maxscale,'Enable','on');

%slider_img setup
Min = 1;
Max = handles.ImagesTaken;
sliderStep = [1.0 1.0]./double(Max) ; % major and minor steps of 1 %need to fix the 50!!!!!!
set(handles.slider_img, 'Min', Min);
set(handles.slider_img, 'Max', Max);
set(handles.slider_img, 'SliderStep', sliderStep);
set(handles.slider_img, 'Value', Max); % set to beginning of sequence
%current_img & current_img setup
set(handles.current_img,'String', num2str(Max));
set(handles.total_img,'String', ['/' num2str(Max)]);

%slider_img_minscale setup
slider_img_minscale_Min = 0.0;
slider_img_minscale_Max = 100.0;
slider_img_minscale_sliderStep = [1.0 1.0]./double(slider_img_minscale_Max) ; 
set(handles.slider_img_minscale, 'Min', slider_img_minscale_Min);
set(handles.slider_img_minscale, 'Max', slider_img_minscale_Max);
set(handles.slider_img_minscale, 'SliderStep', slider_img_minscale_sliderStep);
set(handles.slider_img_minscale, 'Value', slider_img_minscale_Min); % set to beginning of sequence

%slider_img_maxscale setup
slider_img_maxscale_Min = 0.0;
slider_img_maxscale_Max = 100.0;
slider_img_maxscale_sliderStep = [1.0 1.0]./double(slider_img_maxscale_Max) ; 
set(handles.slider_img_maxscale, 'Min', slider_img_maxscale_Min);
set(handles.slider_img_maxscale, 'Max', slider_img_maxscale_Max);
set(handles.slider_img_maxscale, 'SliderStep', slider_img_maxscale_sliderStep);
set(handles.slider_img_maxscale, 'Value', slider_img_maxscale_Max); % set to beginning of sequence

%text_minscale & text_maxscale setup
set(handles.text_minscale,'String', ['Min:' num2str(slider_img_minscale_Min) '%']);
set(handles.text_maxscale,'String', ['Max:' num2str(slider_img_maxscale_Max) '%']);

th = str2double(get(handles.edit_edge_jump,'String'));
prepostEdgeDiff = handles.imgEstack(:,:,1) - handles.imgEstack(:,:,end);  %calculate the difference of below/above edge
handles.filter = prepostEdgeDiff >= th ;

ln_imgEstack = -log(scaleimg);  %negative sign: mu1t1+mu2t2+mu3t3
clear scaleimg
handles.ln_imgEstack = single(ln_imgEstack);

%handles.scale_imgEstack = zeros(handles.imgHeight,handles.imgHeight,handles.ImagesTaken);

set(handles.bin, 'String', num2str(handles.usrbin));
set(handles.status_bkgnorm,'String', 'Status: complete');

FitStart_Min = 1.0;
FitStart_Max = handles.ImagesTaken;
FitStart_sliderStep = [1.0 1.0]./double(FitStart_Max) ; 
set(handles.FitStart, 'Min', FitStart_Min);
set(handles.FitStart, 'Max', FitStart_Max);
set(handles.FitStart, 'SliderStep', FitStart_sliderStep);
set(handles.FitStart, 'Value', FitStart_Min);

FitEnd_Min = 1.0;
FitEnd_Max = handles.ImagesTaken;
FitEnd_sliderStep = [1.0 1.0]./double(FitEnd_Max) ; 
set(handles.FitEnd, 'Min', FitEnd_Min);
set(handles.FitEnd, 'Max', FitEnd_Max);
set(handles.FitEnd, 'SliderStep', FitEnd_sliderStep);
set(handles.FitEnd, 'Value', FitEnd_Min);

guidata(hObject,handles);

% --- Executes on selection change in popupmenu1.
function popupmenu1_Callback(hObject, eventdata, handles)
method_index_selected = get(hObject,'Value');
if ismember(1, method_index_selected)
    handles.UseBaseNorm = false;
    handles.UseRawBkg = false; 
    set(handles.SetRawBkg, 'Enable', 'off')
    set(handles.FitBaseLine, 'Enable', 'off')
    set(handles.BaseLineZero, 'Enable', 'off')
    set(handles.DefaultScaling, 'Value', 0)
    set(handles.DefaultScaling, 'Enable', 'off')
    set(handles.PreEstart, 'Enable', 'off')
    set(handles.PreEend, 'Enable', 'off')
    set(handles.PostEstart, 'Enable', 'off')
    set(handles.PostEend, 'Enable', 'off')
    set(handles.EdgeStart, 'Enable', 'off')
    set(handles.EdgeEnd, 'Enable', 'off')
    set(handles.check_select_zero, 'Enable', 'off')
end
if ismember(2, method_index_selected)
    handles.UseBaseNorm = true;
    handles.UseRawBkg = false; 
    set(handles.SetRawBkg, 'Enable', 'off')
    set(handles.FitBaseLine, 'Enable', 'on')
    set(handles.BaseLineZero, 'Enable', 'on')
    set(handles.DefaultScaling, 'Enable', 'on')
    set(handles.DefaultScaling, 'Value', 0)
    set(handles.PreEstart, 'Enable', 'on')
    set(handles.PreEend, 'Enable', 'on')
    set(handles.PostEstart, 'Enable', 'on')
    set(handles.PostEend, 'Enable', 'on')
    set(handles.EdgeStart, 'Enable', 'off')
    set(handles.EdgeEnd, 'Enable', 'off')
    set(handles.check_select_zero, 'Enable', 'on')
end
if ismember(3, method_index_selected)
    handles.UseBaseNorm = false;
    handles.UseRawBkg = true; 
    set(handles.SetRawBkg, 'Enable', 'on')
    set(handles.FitBaseLine, 'Enable', 'off')
    set(handles.BaseLineZero, 'Enable', 'off')
    set(handles.DefaultScaling, 'Enable', 'on')
    set(handles.DefaultScaling, 'Value', 0)
    set(handles.PreEstart, 'Enable', 'on')
    set(handles.PreEend, 'Enable', 'on')
    set(handles.PostEstart, 'Enable', 'on')
    set(handles.PostEend, 'Enable', 'on')
    set(handles.EdgeStart, 'Enable', 'off')
    set(handles.EdgeEnd, 'Enable', 'off')
    set(handles.check_select_zero, 'Enable', 'off')
end
if ismember(4, method_index_selected)
    handles.UseBaseNorm = false;
    handles.UseRawBkg = false;
    set(handles.SetRawBkg, 'Enable', 'off')
    set(handles.FitBaseLine, 'Enable', 'off')
    set(handles.BaseLineZero, 'Enable', 'off')
    set(handles.DefaultScaling, 'Value', 0)
    set(handles.DefaultScaling, 'Enable', 'off')
    set(handles.PreEstart, 'Enable', 'on')
    set(handles.PreEend, 'Enable', 'on')
    set(handles.PostEstart, 'Enable', 'on')
    set(handles.PostEend, 'Enable', 'on')
    set(handles.EdgeStart, 'Enable', 'on')
    set(handles.EdgeEnd, 'Enable', 'on')
    set(handles.check_select_zero, 'Enable', 'off')
end

PreEstart_Min = 0.0;
PreEstart_Max = 15.0;
PreEstart_sliderStep = [1.0 1.0]./double(PreEstart_Max) ; 
set(handles.PreEstart, 'Min', PreEstart_Min);
set(handles.PreEstart, 'Max', PreEstart_Max);
set(handles.PreEstart, 'SliderStep', PreEstart_sliderStep);
set(handles.PreEstart, 'Value', PreEstart_Min);

PreEend_Min = 0.0;
PreEend_Max = 30.0;
PreEend_sliderStep = [1.0 1.0]./double(PreEend_Max) ; 
set(handles.PreEend, 'Min', PreEend_Min);
set(handles.PreEend, 'Max', PreEend_Max);
set(handles.PreEend, 'SliderStep', PreEend_sliderStep);
set(handles.PreEend, 'Value', PreEend_Min);

PostEstart_Min = 10.0;
PostEstart_Max = handles.ImagesTaken;
PostEstart_sliderStep = [1.0 1.0]./double(PostEstart_Max) ; 
set(handles.PostEstart, 'Min', PostEstart_Min);
set(handles.PostEstart, 'Max', PostEstart_Max);
set(handles.PostEstart, 'SliderStep', PostEstart_sliderStep);
set(handles.PostEstart, 'Value', PostEstart_Min);

PostEend_Min = 20.0;
PostEend_Max = handles.ImagesTaken;
PostEend_sliderStep = [1.0 1.0]./double(PostEend_Max) ; 
set(handles.PostEend, 'Min', PostEend_Min);
set(handles.PostEend, 'Max', PostEend_Max);
set(handles.PostEend, 'SliderStep', PostEend_sliderStep);
set(handles.PostEend, 'Value', PostEend_Min);

EdgeStart_Min = 5.0;
EdgeStart_Max = 30.0;
EdgeStart_sliderStep = [1.0 1.0]./double(EdgeStart_Max) ; 
set(handles.EdgeStart, 'Min', EdgeStart_Min);
set(handles.EdgeStart, 'Max', EdgeStart_Max);
set(handles.EdgeStart, 'SliderStep', EdgeStart_sliderStep);
set(handles.EdgeStart, 'Value', EdgeStart_Min);

EdgeEnd_Min = 5.0;
EdgeEnd_Max = handles.ImagesTaken;
EdgeEnd_sliderStep = [1.0 1.0]./double(EdgeEnd_Max) ; 
set(handles.EdgeEnd, 'Min', EdgeEnd_Min);
set(handles.EdgeEnd, 'Max', EdgeEnd_Max);
set(handles.EdgeEnd, 'SliderStep', EdgeEnd_sliderStep);
set(handles.EdgeEnd, 'Value', EdgeEnd_Min);

guidata(hObject,handles);
% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1


% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in SetRawBkg.
function SetRawBkg_Callback(hObject, eventdata, handles)
if ~isempty(handles.RawBkg)
    delete(handles.RawBkg)
end
if isempty(handles.Original_pixel)
    msgbox('Please Plot the Raw Spectrum of ROI First!')
    return
end
handles.RawBkg = handles.Original_pixel;
guidata(hObject,handles);


% --- Executes on button press in FitBaseLine.
function FitBaseLine_Callback(hObject, eventdata, handles)
% if ~isempty(handles.baseline)
%     delete(handles.baseline)
% end
if isempty(handles.Original_pixel)
    msgbox('Please Plot the Raw Spectrum of ROI First!')
    return
end
% handles.Energy
% handles.Original_pixel
base=[];
base = polyfit(handles.Energy,handles.Original_pixel,1);
handles.baseline = base(1)*handles.Energy + base(2);

handles.baselinePlot = plot(handles.Energy, handles.baseline, 'g--');
guidata(hObject,handles);


% --- Executes on button press in BaseLineZero.
function BaseLineZero_Callback(hObject, eventdata, handles)
% if ~isempty(handles.baseline_zero)
%     delete(handles.baseline_zero)
% end
if isempty(handles.Original_pixel)
    msgbox('Please Plot the Raw Spectrum of ROI First!')
    return
end
dim2 = size(handles.Energy);
handles.baseline_zero = zeros(1, dim2(2));
handles.baselinePlot_zero = plot(handles.Energy, handles.baseline_zero, 'r--');
axis([min(handles.Energy),max(handles.Energy),-0.2,max(max(handles.Original_pixel),max(handles.bulkSpectrum))])
guidata(hObject,handles);


% --- Executes on button press in DefaultScaling.
function DefaultScaling_Callback(hObject, eventdata, handles)
if get(hObject, 'Value')
    handles.scaleByDefault = true;
    set(handles.PreEstart, 'Enable', 'off')
    set(handles.PreEend, 'Enable', 'off')
    set(handles.PostEstart, 'Enable', 'off')
    set(handles.PostEend, 'Enable', 'off')
else
    handles.scaleByDefault = false;
    set(handles.PreEstart, 'Enable', 'on')
    set(handles.PreEend, 'Enable', 'on')
    set(handles.PostEstart, 'Enable', 'on')
    set(handles.PostEend, 'Enable', 'on')
end

guidata(hObject,handles);

% Hint: get(hObject,'Value') returns toggle state of DefaultScaling


% --- Executes on slider movement.
function PreEstart_Callback(hObject, eventdata, handles)
handles.numPreEstart = uint8(get(hObject,'Value'));
set(handles.text_PreEstart,'String', ['PreEstart:' num2str(handles.numPreEstart)]);
guidata(hObject,handles);
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function PreEstart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PreEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function PreEend_Callback(hObject, eventdata, handles)
handles.numPreEend = uint8(get(hObject,'Value'));
set(handles.text_PreEend,'String', ['PreEend:' num2str(handles.numPreEend)]);
set(handles.PreEPlot,'Enable','on');
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function PreEend_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PreEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function PostEstart_Callback(hObject, eventdata, handles)
handles.numPostEstart = uint8(get(hObject,'Value'));
set(handles.text_PostEstart,'String', ['PostEstart:' num2str(handles.numPostEstart)]);
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function PostEstart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PostEstart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function PostEend_Callback(hObject, eventdata, handles)
handles.numPostEend = uint8(get(hObject,'Value'));
set(handles.text_PostEend,'String', ['PostEend:' num2str(handles.numPostEend)]);
set(handles.PostEPlot,'Enable','on');
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function PostEend_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PostEend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function EdgeStart_Callback(hObject, eventdata, handles)
handles.numEdgeStart = uint8(get(hObject,'Value'));
set(handles.text_EdgeStart,'String', ['EdgeStart:' num2str(handles.numEdgeStart)]);
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function EdgeStart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to EdgeStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function EdgeEnd_Callback(hObject, eventdata, handles)
handles.numEdgeEnd = uint8(get(hObject,'Value'));
set(handles.text_EdgeEnd,'String', ['EdgeEnd:' num2str(handles.numEdgeEnd)]);
set(handles.EdgeEPlot,'Enable','on');
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function EdgeEnd_CreateFcn(hObject, eventdata, handles)
% hObject    handle to EdgeEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in select_point.
function select_point_Callback(hObject, eventdata, handles)
if handles.currentSliderStep ==0
    msgbox('please specify and load file first!');
    return
end
    
[x,y] = ginputax(handles.axes1,1);
handles.x = uint16(x);
handles.y = uint16(y);
%redraw(handles);
%freezeColors 
set(handles.x_cord,'String', num2str(handles.x));
set(handles.y_cord,'String', num2str(handles.y));

%----------check here----------------
%handles.usrbin = 1;
set(handles.bin, 'String', num2str(handles.usrbin));
axes(handles.axes1);
redraw(handles);
freezeColors 

set(handles.bin,'Enable', 'on');
guidata(hObject,handles);



function x_cord_Callback(hObject, eventdata, handles)
if handles.currentSliderStep ==0
    msgbox('please specify and load file first!');
    return
end
handles.x = str2num(get(hObject,'String'));
redraw(handles);
guidata(hObject,handles);

% Hints: get(hObject,'String') returns contents of x_cord as text
%        str2double(get(hObject,'String')) returns contents of x_cord as a double


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
if handles.currentSliderStep ==0
    msgbox('please specify and load file first!');
    return
end
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



function bin_Callback(hObject, eventdata, handles)
handles.usrbin = str2num(get(hObject,'String'));
redraw(handles);
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of bin as text
%        str2double(get(hObject,'String')) returns contents of bin as a double


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



function SmoothPts_Callback(hObject, eventdata, handles)
previous_numSmoothPts = handles.numSmoothPts;
handles.numSmoothPts = str2double(get(hObject,'String'));
if handles.numSmoothPts < 1
    msgbox ('Number of points must be >= 1')
    set (handles.SmoothPts, 'String', num2str(uint8(previous_numSmoothPts)))
    handles.numSmoothPts = previous_numSmoothPts;
    return
end
if rem(handles.numSmoothPts, 2) == 0
    handles.numSmoothPts = handles.numSmoothPts - 1;
end

guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of SmoothPts as text
%        str2double(get(hObject,'String')) returns contents of SmoothPts as a double


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



function edit_edge_jump_Callback(hObject, eventdata, handles)
th = str2double(get(hObject,'String'));
prepostEdgeDiff = handles.imgEstack(:,:,1) - handles.imgEstack(:,:,end);  %calculate the difference of below/above edge
handles.filter = prepostEdgeDiff >= th ;  %logical array
redraw(handles);
guidata(hObject,handles);

% Hints: get(hObject,'String') returns contents of edit_edge_jump as text
%        str2double(get(hObject,'String')) returns contents of edit_edge_jump as a double


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


% --- Executes on button press in norm_spec.
function norm_spec_Callback(hObject, eventdata, handles)
set(handles.XANESnormStatus,'String','Status: running');
drawnow;
if isempty(handles.ln_imgEstack)
    msgbox('please specify and load file first!')
    set(handles.XANESnormStatus,'String','Status: none');
    return
end
handles.scale_imgEstack = handles.ln_imgEstack;

if handles.UseBaseNorm
    
    if isempty(handles.baseline)&&isempty(handles.baseline_zero)
        msgbox('use "Fit Base Line" or "Base Line = 0" to set the baseline first')
        set(handles.XANESnormStatus,'String','Status: none');
        return
    end
    
    if handles.select_zero
        for i=1:handles.ImagesTaken
            handles.scale_imgEstack(:,:,i) = handles.scale_imgEstack(:,:,i)- handles.baseline_zero(i);
        end
    else
        for i=1:handles.ImagesTaken
            handles.scale_imgEstack(:,:,i) = handles.scale_imgEstack(:,:,i)- handles.baseline(i);
        end
    end
    
    if handles.scaleByDefault
        ScalingMethod = 'default';
        scale_0 = mean(handles.scale_imgEstack(:,:,1:5),3);
        scale_1 = mean(handles.scale_imgEstack(:,:,end-4:end),3);
        
    else
        ScalingMethod = 'user define';
        ZeroStart = handles.numPreEstart;
        ZeroEnd = handles.numPreEend;
        OneStart = handles.numPostEstart;
        OneEnd = handles.numPostEend;

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
            handles.scale_imgEstack(:,:,i) = handles.scale_imgEstack(:,:,i)- handles.RawBkg(i);
        end
        
        if handles.scaleByDefault
            ScalingMethod = 'default';
            scale_0 = mean(handles.scale_imgEstack(:,:,1:5),3);
            scale_1 = mean(handles.scale_imgEstack(:,:,end-4:end),3);
            
        else
            ScalingMethod = 'user define';
            ZeroStart = handles.numPreEstart;
            ZeroEnd = handles.numPreEend;
            OneStart = handles.numPostEstart;
            OneEnd = handles.numPostEend;
            
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
        if isempty(handles.numPreEstart)|isempty(handles.numPreEend)|isempty(handles.numPostEstart)|isempty(handles.numPostEend)|isempty(handles.numEdgestart)|isempty(handles.numEdgeEnd)
            msgbox('use sliders to set scaling ranges first')
            set(handles.XANESnormStatus,'String','Status: none');
            return
        end
        
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

set(handles.XANESnormStatus,'String','Status:complete');
set(handles.SmoothPts, 'Enable', 'on');
set(handles.FitStart,'Enable','on');
set(handles.FitEnd,'Enable','on');

guidata(hObject,handles);


% --- Executes on selection change in listbox1.
function listbox1_Callback(hObject, eventdata, handles)
%items = get(hObject,'String');
index_selected = get(hObject,'Value');
if ismember(1, index_selected)
    handles.Raw_Spectrum = true;
else
    handles.Raw_Spectrum = false;
end
if ismember(2, index_selected)
    handles.Normalized_Spectrum = true;
else
    handles.Normalized_Spectrum = false;
end
if ismember(3, index_selected)
    handles.Raw_Bulk_Spectrum = true;
else
    handles.Raw_Bulk_Spectrum = false;
end
if ismember(4, index_selected)
    handles.Normalized_Bulk_Spectrum = true;
else
    handles.Normalized_Bulk_Spectrum = false;
end
if ismember(5, index_selected)
    handles.Fitted_Spectrum = true;
else
    handles.Fitted_Spectrum = false;
end
if ismember(6, index_selected)
    handles.ref1plot = true;
else
    handles.ref1plot = false;
end
if ismember(7, index_selected)
    handles.ref2plot = true;
else
    handles.ref2plot = false;
end
if ismember(8, index_selected)
    handles.ref3plot = true;
else
    handles.ref3plot = false;
end
guidata(hObject,handles);

% Hints: contents = cellstr(get(hObject,'String')) returns listbox1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from listbox1


% --- Executes during object creation, after setting all properties.
function listbox1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to listbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in update_spectrum.
function update_spectrum_Callback(hObject, eventdata, handles)
cla(handles.axes2,'reset')
ROI=handles.usrbin;
if (handles.Fitted_Spectrum == false)&&(handles.Raw_Spectrum == false)&&(handles.Raw_Bulk_Spectrum == false)&& ...
    (handles.Normalized_Spectrum == false)&&(handles.Normalized_Bulk_Spectrum == false)&& ...
    (handles.ref1plot == false)&&(handles.ref2plot == false)&&(handles.ref3plot == false)
    msgbox('please specify spectrum type first!')
    return
end
if handles.Fitted_Spectrum
    if ~isempty(handles.fitcurvLine)
        handles.fitcurvLine=[];
    end
    axes(handles.axes2);
    if handles.fitted
        if ROI > 1
            ROI_hsize = (ROI-1)/2; %ROI's half size
            a=0;
            ff = zeros(1,3);
            R = 0;
            for j = -ROI_hsize:ROI_hsize
                for k = -ROI_hsize:ROI_hsize
                    ff = ff + handles.fRGB(handles.index(handles.y+j,handles.x+k), :)./(ROI*ROI);   %squeeze is to reduce the matrix dimension
                    R = max(R, handles.min_R(handles.y+j,handles.x+k));
                    a = a+1;
                end
            end
        else
            ff = handles.fRGB(handles.index(handles.y,handles.x), :);
            R = handles.min_R(handles.y,handles.x);
        end
        
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
        handles.fitcurvLine = plot(handles.Energy, handles.fittedcurve, 'k.-', 'LineWidth', 2);
        %    actLegend = [actLegend; {strleg}]
        legend(strleg, 'location', 'SouthEast');
        %b=findobj(a,'type','line','linestyle','-');
        %set(b,'visible','off');
    else 
        msgbox('Please Fit the Spectrum First!')
        return
    end
end
hold on     

if handles.Raw_Spectrum
    if isempty(handles.ln_imgEstack)
        msgbox('Please Load the File First!')
        return
    end
    plotting = 'Original pixel';
    ShowValue = handles.Raw_Spectrum;
    Original_pixel = reshape(handles.ln_imgEstack(handles.y,handles.x, :),1,handles.ImagesTaken);
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
    handles.raw_spectrum = plot(handles.Energy, handles.Original_pixel, 'kO-');
end

hold on 

if handles.Raw_Bulk_Spectrum  
    if isempty(handles.ln_imgEstack)
        msgbox('Please Load the File First!')
        return
    end
    squeezed_ln_imgEstack = reshape(handles.ln_imgEstack, [handles.imgHeight*handles.imgHeight, handles.ImagesTaken]);
    point_spectrum = squeezed_ln_imgEstack(handles.filter, :);
    handles.bulkSpectrum=mean(point_spectrum);
    axes(handles.axes2);
    handles.raw_bulk_spectrum = plot(handles.Energy, handles.bulkSpectrum, 'k.-');
end

hold on

if handles.Normalized_Spectrum
    if isempty(handles.scale_imgEstack)
        msgbox('Please Normalize the Spectrum First!')
        return
    end
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
    end
    
    if handles.numSmoothPts ~= 1
        windowSize = handles.numSmoothPts;  %e.g. windowSize = 5
        groupDelay = double(floor(windowSize/2));   %e.g. groupDelay = 2
        handles.scale_imgEstack_pixel = filter(ones(1,groupDelay+1)/windowSize,1,handles.scale_imgEstack_pixel)...
                                        + flipdim(filter(ones(1,groupDelay+1)/windowSize,1,flipdim(handles.scale_imgEstack_pixel,2)),2)...
                                        - handles.scale_imgEstack_pixel/windowSize;
    end
        axes(handles.axes2);
        handles.norm_spectrum = plot(handles.Energy, handles.scale_imgEstack_pixel, 'ms-');
end

hold on 

if handles.Normalized_Bulk_Spectrum
    if isempty(handles.scale_imgEstack)
        msgbox('Please Normalize the Spectrum First!')
        return
    end
    squeezed_ln_imgEstack = reshape(handles.scale_imgEstack, [handles.imgHeight*handles.imgHeight, handles.ImagesTaken]);
    point_spectrum = squeezed_ln_imgEstack(handles.filter, :);
    handles.normbulkSpectrum= mean(point_spectrum);
    axes(handles.axes2);
    handles.norm_bulk_spectrum = plot(handles.Energy, handles.normbulkSpectrum, 'm^-');
end

hold on 

if handles.ref1plot
    axes(handles.axes2);
    handles.ref1Spec = plot(handles.ref1all(1,:), handles.ref1, 'r');
end
hold on

if handles.ref2plot
    axes(handles.axes2);
    handles.ref2Spec = plot(handles.ref2all(1,:), handles.ref2, 'g');
end
hold on

if handles.ref3plot
    axes(handles.axes2);
    handles.ref3Spec = plot(handles.ref3all(1,:), handles.ref3, 'b');
end
hold on

axes(handles.axes2);
xlabel('Energy (eV)');
ylabel('Normalized \mu t');
%h_legend=legend('Raw Spectrum','Raw Bulk Spectrum','Normalized Spectrum','Normalized Bulk Spectrum','Location','NorthWest');
%set(h_legend,'FontSize',5);
title('Raw(ROI):O    Normalized(ROI):square    Raw Bulk:dot    Normalized Bulk:triangle   Fitted:bold dot','FontSize',8);
handles.edgePoint = [];
handles.preLine = [];
handles.postLine = [];
handles.FitStartLine = [];
handles.FitEndLine = [];
handles.numPreEstartLine = [];
handles.numPreEendLine = [];
handles.numPostEstartLine = [];
handles.numPostEendLine = [];
handles.EdgeStartLine = [];
handles.EdgeEndLine = [];
set(handles.popupmenu1,'Enable','on');
guidata(hObject,handles);


% --- Executes on button press in SaveSpectrumFig.
function SaveSpectrumFig_Callback(hObject, eventdata, handles)
if (handles.x == 0.0)|(handles.y == 0.0)
    msgbox('Please Plot the Spectrum of ROI First!')
    return
end
[file,path] = uiputfile(['SpectrumName_x' num2str(handles.x) '_y' num2str(handles.y)...
    '_bin' num2str(handles.usrbin) '.tif']...
    ,'Save Spectrum Figure As');
if path == 0
    msgbox('please select a path first!');
    return
end
export_fig(handles.axes2, [path file]);



% --- Executes on button press in save_spectrum.
function save_spectrum_Callback(hObject, eventdata, handles)
prefix = inputdlg('Please Enter the Prefix for Selected Spectrums:', 'Prefix',1,{'SpectrumName'});
if handles.Raw_Spectrum
    if isempty(handles.Original_pixel)
        msgbox('Please Select the Raw Spectrum (ROI) First!')
        return
    end
    lineprofile = handles.Original_pixel;
    file = char(strcat(prefix,'_x',num2str(handles.x),'_y',num2str(handles.y),'_bin',num2str(handles.usrbin),'.txt'));
    path = handles.PathName;
    content = [handles.Energy; lineprofile];
    handles.spectrum_name = [path, file];
    cd(path)
    fid = fopen(handles.spectrum_name, 'wt');
    fprintf(fid, 'Energy\tmut\n');
    fprintf(fid, '%f %f\n', content);
    fclose(fid);
end

if handles.Raw_Bulk_Spectrum
    if isempty(handles.bulkSpectrum)
        msgbox('Please Select the Raw Bulk Spectrum First!')
        return
    end
    lineprofile = handles.bulkSpectrum;
    file = char(strcat(prefix,'Bulk','.txt'));
    path = handles.PathName;
    content = [handles.Energy; lineprofile];
    handles.spectrum_name = [path, file];
    cd(path)
    fid = fopen(handles.spectrum_name, 'wt');
    fprintf(fid, 'Energy\tmut\n');
    fprintf(fid, '%f %f\n', content);
    fclose(fid);
end

if handles.Normalized_Spectrum
    if isempty(handles.scale_imgEstack_pixel)
        msgbox('Please Select the Normalized Spectrum (ROI) First!')
        return
    end
    lineprofile = handles.scale_imgEstack_pixel;
    file = char(strcat(prefix,'Normalized','_x',num2str(handles.x),'_y',num2str(handles.y),'_bin',num2str(handles.usrbin),'.txt'));
    path = handles.PathName;
    content = [handles.Energy; lineprofile];
    handles.spectrum_name = [path, file];
    cd(path)
    fid = fopen(handles.spectrum_name, 'wt');
    fprintf(fid, 'Energy\tmut\n');
    fprintf(fid, '%f %f\n', content);
    fclose(fid);
end

if handles.Normalized_Bulk_Spectrum
    if isempty(handles.normbulkSpectrum)
        msgbox('Please Select the Normalized Bulk Spectrum First!')
        return
    end
    lineprofile = handles.normbulkSpectrum;
    file = char(strcat(prefix,'Normalized','Bulk','.txt'));
    path = handles.PathName;
    content = [handles.Energy; lineprofile];
    handles.spectrum_name = [path, file];
    cd(path)
    fid = fopen(handles.spectrum_name, 'wt');
    fprintf(fid, 'Energy\tmut\n');
    fprintf(fid, '%f %f\n', content);
    fclose(fid);
end


% --- Executes on slider movement.
function FitStart_Callback(hObject, eventdata, handles)
handles.numFitStart = uint8(get(hObject,'Value'));
set(handles.text_FitStart,'String', ['Start:' num2str(handles.numFitStart)]);
handles.FitStartLine = addline_zerotoone(handles, handles.FitStartLine, ...
    handles.numFitStart, 'k-');
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function FitStart_CreateFcn(hObject, eventdata, handles)
% hObject    handle to FitStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function FitEnd_Callback(hObject, eventdata, handles)
handles.numFitEnd = uint8(get(hObject,'Value'));
set(handles.text_FitEnd,'String', ['End:' num2str(handles.numFitEnd)]);
handles.FitEndLine = addline_zerotoone(handles, handles.FitEndLine, ...
    handles.numFitEnd, 'k-');
guidata(hObject,handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function FitEnd_CreateFcn(hObject, eventdata, handles)
% hObject    handle to FitEnd (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



function resolution_Callback(hObject, eventdata, handles)
handles.res = str2double(get(hObject, 'String'));
guidata(hObject,handles);

% Hints: get(hObject,'String') returns contents of resolution as text
%        str2double(get(hObject,'String')) returns contents of resolution as a double


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



function Rmax_Callback(hObject, eventdata, handles)
handles.RmaxValue = str2double(get(hObject,'String'));
handles.MaxRfilter = handles.min_R <= handles.RmaxValue;
%redraw(handles);
guidata(hObject,handles);

% Hints: get(hObject,'String') returns contents of Rmax as text
%        str2double(get(hObject,'String')) returns contents of Rmax as a double


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


% --- Executes on button press in bin_object.
function bin_object_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    handles.binobject = true;
else
    handles.binobject = false;
end
guidata(hObject,handles);

% Hint: get(hObject,'Value') returns toggle state of bin_object


% --- Executes on button press in smooth_object.
function smooth_object_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    handles.smoothobject = true;
else
    handles.smoothobject = false;
end
guidata(hObject,handles);


% Hint: get(hObject,'Value') returns toggle state of smooth_object


% --- Executes on button press in fitting.
function fitting_Callback(hObject, eventdata, handles)
if handles.refcounter < 2
    msgbox('Please load enough number of references!');
    set(handles.status_expXANES,'String', 'Status: none');
    return
end

if isempty(handles.scale_imgEstack)
    msgbox('Please load and normalize sample spectrum!');
    set(handles.status_expXANES,'String', 'Status: none');
    return
end

handles.fitted = true;

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
if handles.smoothobject
    windowSize = handles.numSmoothPts;
    groupDelay = double(floor(windowSize/2));
    %new_stack = filter(ones(1,windowSize)/windowSize,1,new_stack, [], 3);
    new_stack = filter(ones(1,groupDelay+1)/windowSize,1,new_stack, [], 3)...
              + flipdim(filter(ones(1,groupDelay+1)/windowSize,1,flipdim(new_stack, 3), [], 3),3)...
              - new_stack/windowSize;
end

numFitStart = handles.numFitStart;
numFitEnd = handles.numFitEnd;

if handles.refcounter == 2
    [handles.min_R, handles.index, handles.fRGB] = fit2D_2refs(handles.ref1(numFitStart:numFitEnd), handles.ref2(numFitStart:numFitEnd), ...
        new_stack(:,:,numFitStart:numFitEnd), handles.res);
else
    [handles.min_R, handles.index, handles.fRGB] = fit2D_3refs(handles.ref1(numFitStart:numFitEnd), handles.ref2(numFitStart:numFitEnd),...
        handles.ref3(numFitStart:numFitEnd), new_stack(:,:,numFitStart:numFitEnd), handles.res);
end

%axes(handles.axes1)
%imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);

axes(handles.axes3);
imshow(handles.index, handles.fRGB);
%freezeColors 


set(handles.status_expXANES,'String', 'Status: complete');
redraw(handles);
guidata(hObject,handles);


% --- Executes on button press in update_image.
function update_image_Callback(hObject, eventdata, handles)
if isempty(handles.index)
    msgbox('Please perform fitting first!');
    return
end

handles.MaxRfilter = handles.min_R <= handles.RmaxValue;

%axes(handles.axes1)
%imshow(handles.imgEstack(:,:,handles.ImagesTaken), [handles.scale_min/100*255 handles.scale_max/100*255]);

% axes(handles.axes3);
% imshow(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB);
redraw(handles);
guidata(hObject,handles);


% --- Executes on button press in save_fitted.
function save_fitted_Callback(hObject, eventdata, handles)
[file,path] = uiputfile('FittedResult.tif','Save Fitted Result As');
if path == 0
    msgbox('please select a path first!');
    return
end
if isempty(handles.index)
    msgbox('Please perform fitting first!');
    return
end
cd(path)
imwrite(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB, [path, file]);


% --- Executes on button press in PreEPlot.
function PreEPlot_Callback(hObject, eventdata, handles)
if ~isempty(handles.preLine)
    delete(handles.preLine);
end
axes(handles.axes2);

handles.pre = polyfit(handles.Energy(handles.numPreEstart:handles.numPreEend),...
    handles.bulkSpectrum(handles.numPreEstart:handles.numPreEend),1);

handles.preLine = plot(handles.Energy(handles.numPreEstart:handles.numPreEend), ...
    handles.pre(1)*handles.Energy(handles.numPreEstart:handles.numPreEend)+handles.pre(2), 'c--');

handles.numPreEstartLine = addline(handles, handles.numPreEstartLine, ...
    handles.numPreEstart, 'c-');

handles.numPreEendLine = addline(handles, handles.numPreEendLine, ...
    handles.numPreEend, 'c--');

hold on;
guidata(hObject,handles);


% --- Executes on button press in PostEPlot.
function PostEPlot_Callback(hObject, eventdata, handles)
if ~isempty(handles.postLine)
    delete(handles.postLine)
end
axes(handles.axes2);

handles.post = polyfit(handles.Energy(handles.numPostEstart:handles.numPostEend),...
    handles.bulkSpectrum(handles.numPostEstart:handles.numPostEend),1);

handles.postLine = plot(handles.Energy(handles.numPostEstart:handles.numPostEend), ...
    handles.post(1)*handles.Energy(handles.numPostEstart:handles.numPostEend)+handles.post(2), 'm--');

handles.numPostEstartLine = addline(handles, handles.numPostEstartLine, ...
    handles.numPostEstart, 'm-');

handles.numPostEendLine = addline(handles, handles.numPostEendLine, ...
    handles.numPostEend, 'm--');

hold on;
guidata(hObject,handles);


% --- Executes on button press in EdgeEPlot.
function EdgeEPlot_Callback(hObject, eventdata, handles)
if ~isempty(handles.edgePoint)
    delete(handles.edgePoint)
end
axes(handles.axes2);

handles.E0 = uint8((handles.numEdgeStart+handles.numEdgeEnd)./2);
handles.edgePoint = plot(handles.Energy(handles.E0), handles.bulkSpectrum(handles.E0), 'gx');

handles.EdgeStartLine = addline(handles, handles.EdgeStartLine, ...
    handles.numEdgeStart, 'b-');
handles.EdgeEndLine = addline(handles, handles.EdgeEndLine, ...
    handles.numEdgeEnd, 'b--');

hold on;
guidata(hObject,handles);


% --- Executes on button press in check_select_zero.
function check_select_zero_Callback(hObject, eventdata, handles)
if get(hObject,'Value')
    handles.select_zero = true;
else
    handles.select_zero = false;
end
guidata(hObject,handles);


% --- Executes on button press in athena.
function athena_Callback(hObject, eventdata, handles)
if handles.currentSliderStep ==0
    msgbox('please specify and load file first!');
    return
end
if (handles.x == 0.0)|(handles.y == 0.0)
    msgbox('Please Select ROI First!')
    return
end
[file,path] = uiputfile(['SpectrumName' '_x' num2str(handles.x) '_y' num2str(handles.y)...
        '_bin' num2str(handles.usrbin) '.txt']...
        ,'Save Spectrum As');
set(handles.XANESnormStatus,'String','Status: running');
fid = fopen([path file], 'wt');
num_img = handles.ImagesTaken;

fprintf(fid, '        Energy            I0            It            Ir\n')

ROI=handles.usrbin;

if ROI > 1
    ROI_hsize = (ROI-1)/2; %ROI's half size
    
    a=1;
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

point_spectrum_r = zeros(handles.ImagesTaken);
for i=1:num_img
    fprintf(fid, '%14.5f%14.4f%14.4f%14.4f\n', handles.Energy(i),...
        print_bkg_spectrum(i),...
        print_img_spectrum(i),...
        point_spectrum_r(i));
end
fclose(fid);
set(handles.XANESnormStatus,'String','Status: complete');


% --- Executes on button press in restart.
function restart_Callback(hObject, eventdata, handles)
choice = questdlg('Would you like to restart this program?', ...
	'Restart Program', ...
	'YES','NO','CANCEL','CANCEL');
% Handle response
switch choice
    case 'YES'
        close(gcbf)
        X8C_XANE_2Dfitting_naiyun
    case 'No'
        return
    case 'CANCEL'
        return
end
