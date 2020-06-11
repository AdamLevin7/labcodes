# -*- coding: utf-8 -*-
"""
ImportForce_TXT
    Import force data from text file.
    
Inputs
    file: STR file name (.txt) of force data
    
Outputs
    data: DATAFRAME force data with plate names and components
    samp: FLOAT64 sampling rate of collection
    weight: FLOAT64 weight (N) that was stored with collection (MAY OR MAY NOT BE
        ACTUAL WEIGHT OF INDIVIDUAL/SYSTEM - COULD BE FROM A PREVIOUS SESSION)

Created on Mon Oct  7 10:58:39 2019

@author: Casey Wiens, cwiens32@gmail.com
"""


import pandas as pd
    
def ImportForce_TXT(file):
    
    #%% load data and format variables
    data = pd.read_csv(file,
                       sep = "\t",
                       skiprows = 1,
                       header = None)
    # format sampling rate and weight variables
    samp = float(data.iloc[2,1])
    weight = float(data.iloc[8,1])

    #%% add the device name to the signal name
    for x in range(1,len(data.columns)):
        data.loc[16,x] = data.loc[0,x] + '_' + data.loc[16,x]
        
    #%% format data table
    """
    rename the column headers
    crop the top of the file
    reset the index
    set the first column header to "Time"
    convert data to numeric
    """
    data = data.rename(columns=data.iloc[16]).loc[18: ,].reset_index(drop=True).rename(columns={"abs time (s)" :"Time"}).apply(pd.to_numeric)
    
    return data, samp, weight