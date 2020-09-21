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

    % Create a table with the data
    ForceTable = table(ForceDataP.FP1_x,ForceDataP.FP1_y,ForceDataP.FP1_z,...
        ForceDataP.FP2_x,ForceDataP.FP2_y,ForceDataP.FP2_z);

    ForceTable.Properties.VariableNames = {'FP1_x' 'FP1_y' 'FP1_z' 'FP2_x' 'FP2_y' 'FP2_z'};

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
    suptitle(sprintf('Graph of %s', file{i}));

    %% Write the data to a .csv file
    newFilename = [ filename(1:end-4) '_1200Hz' '.csv']; 
    writetable(ForceTable,newFilename,'Delimiter',',','QuoteStrings',true)

    % Save Figure
    saveas(h,[newFilename(1:end-4) '.jpeg'])

    %% Clear out the variables 
    clearvars -except gain startRow endRow file path sampRate
    
end
