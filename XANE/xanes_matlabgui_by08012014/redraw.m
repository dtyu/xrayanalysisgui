function redraw(handles)
if handles.fitted
    axes(handles.axes1);
    freezeColors 
    if isempty(handles.filter)
        imshow(handles.imgEstack(:,:,handles.currentSliderStep), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);axis equal;
    else
        imshow(handles.imgEstack(:,:,handles.currentSliderStep).*uint8(handles.filter), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);axis equal;
    end
    x = handles.x;
    y = handles.y;
    line([x-20 x+20], [y y], 'LineWidth',1.5,'Color',[1 0.5 0]);
    line([x x], [y-20 y+20], 'LineWidth',1.5,'Color',[1 0.5 0]);
    w = handles.usrbin;
    rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 1 0]);
    freezeColors
    axes(handles.axes3);
    if isempty(handles.filter)
        if isempty(handles.MaxRfilter)
            imshow(handles.index, handles.fRGB);axis equal;
        else
            imshow(handles.index.*handles.MaxRfilter, handles.fRGB);axis equal;
        end
    else
        if isempty(handles.MaxRfilter)
            imshow(handles.index.*handles.filter, handles.fRGB);axis equal;
        else
            imshow(handles.index.*handles.filter.*handles.MaxRfilter, handles.fRGB);axis equal;
        end
    end
    x = handles.x;
    y = handles.y;
    line([x-20 x+20], [y y], 'LineWidth',1.5,'Color',[1 0.5 0]);
    line([x x], [y-20 y+20], 'LineWidth',1.5,'Color',[1 0.5 0]);
    w = handles.usrbin;
    rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 1 0]);
    freezeColors
else
    axes(handles.axes1);
    if isempty(handles.filter)
        imshow(handles.imgEstack(:,:,handles.currentSliderStep), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);axis equal;
    else
        %toshow = handles.imgEstack(:,:,handles.ImagesTaken)
        %imshow(toshow(handles.filter), [handles.scale_min/100*255 handles.scale_max/100*255]);
        imshow(handles.imgEstack(:,:,handles.currentSliderStep).*uint8(handles.filter), [double(handles.scale_min)/100*255 double(handles.scale_max)/100*255]);axis equal;
    end
    x = handles.x;
    y = handles.y;
    line([x-20 x+20], [y y], 'LineWidth',1.5,'Color',[1 0.5 0]);
    line([x x], [y-20 y+20], 'LineWidth',1.5,'Color',[1 0.5 0]);
    w = handles.usrbin;
    rectangle('Position',[x-w/2,y-w/2,w,w], 'LineWidth',2,'LineStyle','--', 'EdgeColor', [1 1 0]);
end
