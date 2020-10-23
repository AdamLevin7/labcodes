%% Script for Importing Data from KDA files

% inputs: Select KDA files (can select multiples)
% outputs: .csv file with force data (FP1x, FP1y, FP1z, FP2x, FP2y, FP2z)
%          .jpeg with force vs time curve to check against .avi overlay

% Created by Harper Stewart 9/19/2020

%% Setting known variables
clear all; clc; close all;
gain = 3;
startRow = 7;
endRow = 7206;
%filename = 'F:\USC Biomechanics Research\HBIO 408\Tasks\Vayu Tasks\_001.KDA';
[file,path] = uigetfile('.KDA','Select KDA file','MultiSelect','on');
sampRate = 1200;

%% Adjusting file variable from string to cell
if ~iscell(file)
    file = {file};
end

%% Force Plate Information
% Assuming this is for B10 using Kistler 9281EA Force Plates ??
% Dimensions 600x400x100 mm
% Distances to transducers for calculations
a = 120/1000; % mm to meters
b = 200/1000; % mm to meters
az0 = 45/1000; % mm to meters

%% Create for loop for batch processing
for i = 1:length(file)

    filename = [path file{i}];

    %% Import KDA File

    [ForceData] = importForce_KDA(filename,gain,startRow,endRow);

    %% Creat Time Series for Plot Check
    time = transpose(0:1/sampRate:((1/sampRate)*length(ForceData.FP1_x1))-(1/sampRate));


    %% Add the forces

    % Time Series
    ForceDataP.time = time;
    %FP1
    ForceDataP.FP1_x = ForceData.FP1_x1+ForceData.FP1_x2;
    ForceDataP.FP1_y = ForceData.FP1_y1+ForceData.FP1_y2;
    ForceDataP.FP1_z = ForceData.FP1_z1+ForceData.FP1_z2+ForceData.FP1_z3+ForceData.FP1_z4;
    %FP1=2
    ForceDataP.FP2_x = ForceData.FP2_x1+ForceData.FP2_x2;
    ForceDataP.FP2_y = ForceData.FP2_y1+ForceData.FP2_y2;
    ForceDataP.FP2_z = ForceData.FP2_z1+ForceData.FP2_z2+ForceData.FP2_z3+ForceData.FP2_z4;
    %% Add in other parameters (Moments, CP)
    % Plate Moments
%     Mx = b * (fz1 + fz2 - fz3 - fz4) Plate moment about X-axis 3)
    ForceDataP.Mx1 = b* (ForceData.FP1_z1+ForceData.FP1_z2-ForceData.FP1_z3-ForceData.FP1_z4);
    ForceDataP.Mx2 = b* (ForceData.FP2_z1+ForceData.FP2_z2-ForceData.FP2_z3-ForceData.FP2_z4);
%     My = a * (-fz1 + fz2 + fz3 - fz4) Plate moment about Y-axis 3)
    ForceDataP.My1 = a .* (-ForceData.FP1_z1+ForceData.FP1_z2+ForceData.FP1_z3-ForceData.FP1_z4);
    ForceDataP.My2 = a .* (-ForceData.FP2_z1+ForceData.FP2_z2+ForceData.FP2_z3-ForceData.FP2_z4);
%     Mz = b * (-fx12 + fx34) + a * (fy14 - fy23) Plate moment about Z-axis 3)
    ForceDataP.Mz1 = b .* (-ForceData.FP1_x1+ForceData.FP1_x2) +a* (ForceData.FP1_y1-ForceData.FP1_y2);
    ForceDataP.Mz2 = b .* (-ForceData.FP2_x1+ForceData.FP2_x2) +a* (ForceData.FP1_y2-ForceData.FP2_y2);
%     Mx' = Mx + Fy*az0 Plate moment about top plate surface 
    ForceDataP.Mx1_top = ForceDataP.Mx1 + ForceDataP.FP1_y  .* az0;
    ForceDataP.Mx2_top = ForceDataP.Mx2 + ForceDataP.FP2_y .* az0;
%     My' = My - Fx*az0 Plate moment about top plate surface 
    ForceDataP.My1_top = ForceDataP.My1 + ForceDataP.FP1_x .* az0;
    ForceDataP.My2_top = ForceDataP.My2 + ForceDataP.FP2_x .* az0;
%     ax = -My' / Fz X-Coordinate of force application point (COP)
    ForceDataP.Ax1 = -ForceDataP.My1_top ./ ForceDataP.FP1_z;
    ForceDataP.Ax2 = -ForceDataP.My2_top ./ ForceDataP.FP2_z;
%     ay = Mx' / Fz Y-Coordinate of force application point (COP)
    ForceDataP.Ay1 = ForceDataP.Mx1_top ./ ForceDataP.FP1_z;
    ForceDataP.Ay2 = ForceDataP.Mx2_top ./ ForceDataP.FP2_z;
    
    %% Calculate the resultant force 
   ForceDataP.FRes1 = sqrt(...
            ForceDataP.FP1_x.^2 +...
            ForceDataP.FP1_y.^2 +...
            ForceDataP.FP1_z.^2);
    ForceDataP.FRes2 = sqrt(...
        ForceDataP.FP2_x.^2 +...
        ForceDataP.FP2_y.^2 +...
        ForceDataP.FP2_z.^2);

    %% Create a table with the data
    ForceTable = table(ForceDataP.time,ForceDataP.FP1_x,ForceDataP.FP1_y,ForceDataP.FP1_z,...
        ForceDataP.FRes1, ForceDataP.Ax1,ForceDataP.Ay1,...
        ForceDataP.FP2_x,ForceDataP.FP2_y,ForceDataP.FP2_z,...
        ForceDataP.FRes2, ForceDataP.Ax2,ForceDataP.Ay2);

    ForceTable.Properties.VariableNames = {'Time' 'FP1_Fx' 'FP1_Fy' 'FP1_Fz' 'FP1_Fres' 'FP1_Ax' 'FP1_Ay' 'FP2_Fx' 'FP2_Fy' 'FP2_Fz' 'FP2_Fres' 'FP2_Ax', 'FP2_Ay'};

    %% Plot the forces

    % FP1 
    h(1) = figure;
    
    subplot(3,1,1);
    plot(ForceDataP.time, ForceDataP.FP1_y)
    hold on
    plot(ForceDataP.time, ForceDataP.FP1_z)
    plot(ForceDataP.time, ForceDataP.FP1_x)
    legend('y','z','x')
    title('FP1') 

    subplot(3,1,2);
    plot(ForceDataP.time, ForceDataP.FP2_y)
    hold on
    plot(ForceDataP.time, ForceDataP.FP2_z)
    plot(ForceDataP.time, ForceDataP.FP2_x)
    legend('y','z','x')
    title('FP2') 

    subplot(3,1,3);
    plot(ForceDataP.time, ForceDataP.FP2_y+ForceDataP.FP1_y)
    hold on
    plot(ForceDataP.time, ForceDataP.FP2_z+ForceDataP.FP1_z)
    plot(ForceDataP.time, ForceDataP.FP2_x+ForceDataP.FP1_x)
    legend('y','z','x')
    title('Combined FP1 and FP2') 
    sgtitle(sprintf('Graph of %s', file{i}));

    % Write the data to a .csv file
    newFilename = [ filename(1:end-4) '_1200Hz' '.csv']; 
    writetable(ForceTable,newFilename,'Delimiter',',','QuoteStrings',true)

    % Save Figure
    saveas(h,[newFilename(1:end-4) '.jpeg'])

    %% Clear out the variables 
    clearvars -except gain startRow endRow file path sampRate a b az0
    
end
