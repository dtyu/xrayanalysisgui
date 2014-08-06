if isempty(handles.numPreEstart)|isempty(handles.numPreEend)|isempty(handles.numPostEstart)|isempty(handles.numPostEend)|isempty(handles.numEdgestart)|isempty(handles.numEdgeEnd)
    msgbox('use sliders to set scaling ranges first')
    set(handles.XANESnormStatus,'String','Status: none');
    return
end
        
E0 = handles.Energy(handles.E0);
warning('off','all');

base(:,:)= mean(handles.ln_imgEstack(:,:,handles.numPreEstart:handles.numPreEend));
post(:,:,:) = zeros(handles.imgHeight,handles.imgHeight,2);
for i=1:handles.imgHeight
    for j=1:handles.imgHeight
        if (handles.filter(i,j))
            post(i,j,:) = polyfit(handles.Energy(handles.numPostEstart:handles.numPostEend),handles.ln_imgEstack(i,j,handles.numPostEstart:handles.numPostEend),1);
        else
            post(i,j,:) = [0,mean(handles.ln_imgEstack(i,j,handles.numPostEstart:handles.numPostEend))];
        end
    end
end

%preE0 = pre(1)*E0+pre(2);
%postE0 = post(1)*E0+post(2);
%edgeDiff = postE0 - preE0;
                    
handles.scale_imgEstack(:,:,:) = (handles.ln_imgEstack(:,:,:)-base(:,:))./(post(:,:,1)*E0+post(:,:,2)-base(:,:));
