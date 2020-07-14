# -*- coding: utf-8 -*-
"""
runningreorient
    Reorients FP data to "running" reference system.
    Ie. Vertical force (+)
        Anterior force (+)
        Medial force (+)
    
    
Dependencies
    matplotlib
    pandas
    ImportForce_TXT, combine_forces
    FindContactIntervals 
    
Created on Mon Jun 15 20:47:51 2020

@author: hestewar
"""
#%% Packages/Modules
from ImportForce_TXT import ImportForce_TXT, combine_force
from FindContactIntervals import FindContactIntervals
import matplotlib.pyplot as plt
import pandas as pd

#%% 
"""
runningorient
    Orient force data in "running reference frame."
    
Use function line: fpDataReorient = RunReorient(filepath, rezero = 'b', foot = 'R')
    
Inputs
    file: STR file name (.txt) of force data
    rezero: STR ability to rezero force data (default: None)
        options:    b - subtracted based on beginning 200 frames
                    e - subtracted bassed on ending 200 frames
    foot: STR R or L to indicate if medial lateral force should be flipped
    
Outputs
    fpDataReorient : DATAFRAME force data with forces reoriented

"""
def RunReorient(file, rezero, foot):
    # Threshold for contact and QC check
    thresh = 20
    
    #%% Read in file
    fpData, fpSampRate, bw = ImportForce_TXT(file, rezero)
    
    #%% Combine force data
    fpDataComb = combine_force(fpData)
    
    #%% Find Contact Interval
    # Find the contact interval to make decisions about flipping data
    contIntv = FindContactIntervals(fpDataComb['fz'],fpSampRate,thresh)
    
    #%%  Crop data 
    fpDataCrop = fpDataComb.iloc[contIntv['Start'][0]:contIntv['End'][0],:]
    #%% Reset time
    fpDataCrop['time'] = fpDataCrop['time'] - fpDataCrop['time'].iloc[0]
    
    #%% Reorient Forces into new dataframe
    fpDataReorient = pd.DataFrame(fpDataComb['time'])
    
    # Medial Lateral Force
    if foot == 'L':
            fpDataReorient['MedLat']= -fpDataComb['fx']
    else:
        fpDataReorient['MedLat'] = fpDataComb['fx']
    
        
    # Anterior Posterior Force
    # If the max value index is less than min value index than flip AP force
    if fpDataCrop['fy'].idxmax() < fpDataCrop['fy'].idxmin():
            fpDataReorient['AntPost'] = -fpDataComb['fy']
    else:
        fpDataReorient['AntPost'] = fpDataComb['fy']
        
    # Vertical Force 
    if fpDataCrop['fz'].mean() < 0:
        fpDataReorient['Vert'] = -fpDataComb['fz']
    else:
        fpDataReorient['Vert'] = fpDataComb['fz']
        
    #%% Keep COP data
    fpDataReorient['FP1_Ax'] = fpData['Attila49 9286BA_Ax']
    fpDataReorient['FP1_Ay'] = fpData['Attila49 9286BA_Ay']
    fpDataReorient['FP2_Ax'] = fpData['Ryan52 9286BA_Ax']
    fpDataReorient['FP2_Ay'] = fpData['Ryan52 9286BA_Ay']
        
    #%% Quality Control Check
    # Make sure that the force data is oriented relative to running GRF convention
    """ Crop check """
    contIntv2 = FindContactIntervals(fpDataReorient['Vert'],fpSampRate,thresh)
    
    """ crop data """
    forceData_crop2 = fpDataReorient.iloc[contIntv2['Start'][0]:contIntv2['End'][0],:]
    
    """ reset time """
    forceData_crop2['time'] = fpDataReorient['time'] - fpDataReorient['time'].iloc[0]
    
    """ plot data """
    # file 1
    plt.figure()
    plt.plot(forceData_crop2['time'], forceData_crop2['MedLat'], 'b-', label='Med-Lat')
    plt.plot(forceData_crop2['time'], forceData_crop2['AntPost'], 'b--', label='Ant-Post')
    plt.plot(forceData_crop2['time'], forceData_crop2['Vert'], 'b-.', label='Vert')
    plt.axis([0, 0.25, -500, 2000])
    plt.legend()
    plt.title('Quality Control Check: Ensure Force Orientation is Correct')

    #%% Return Dataframe
    return fpDataReorient




