function newLineHandle = addline(handles, currentLineHandle, currentEvalue, colorNlinestyle)
axes(handles.axes2);
hold on
if ~isempty(currentLineHandle)
    delete(currentLineHandle)
end

linex(1:2) = handles.Energy(currentEvalue);
liney(1:2) = [min(handles.bulkSpectrum),max(handles.bulkSpectrum)];
newLineHandle = plot(linex,liney, colorNlinestyle);  %# Create a line with PLOT