# -*- coding: utf-8 -*-
"""
ImportForce_TXT
    Modules to import force data from text file and combine data.

Dependencies:
    pandas
    scipy

Created on Mon Oct  7 10:58:39 2019

@author: Casey Wiens, cwiens32@gmail.com
"""
import pandas as pd
from scipy import stats


#%%
"""
ImportForce_TXT
    Import force data from text file.
    
Inputs
    file: STR file name (.txt) of force data
    rezero: STR ability to rezero force data (default: None)
        options:    b - subtracted based on beginning 200 frames
                    e - subtracted bassed on ending 200 frames
    
Outputs
    data: DATAFRAME force data with plate names and components
    samp: FLOAT64 sampling rate of collection
    weight: FLOAT64 weight (N) that was stored with collection (MAY OR MAY NOT BE
        ACTUAL WEIGHT OF INDIVIDUAL/SYSTEM - COULD BE FROM A PREVIOUS SESSION)
"""
def ImportForce_TXT(file, rezero=None):
    
    ### load data and format variables
    data = pd.read_csv(file,
                       sep = "\t",
                       skiprows = 1,
                       header = None)
    # format sampling rate and weight variables
    samp = float(data.iloc[2,1])
    weight = float(data.iloc[8,1])

    ### add the device name to the signal name
    for x in range(1,len(data.columns)):
        data.loc[16,x] = data.loc[0,x] + '_' + data.loc[16,x]
        
    ### format data table
    """
    rename the column headers
    crop the top of the file
    reset the index
    set the first column header to "Time"
    convert data to numeric
    """
    data = data.rename(columns=data.iloc[16]).loc[18: ,].reset_index(drop=True).rename(columns={"abs time (s)" :"Time"}).apply(pd.to_numeric)
    
    """ rezero """
    # if rezeroing option was provided...
    if rezero is not None:
        # if rezero based on begining frames...
        if rezero == 'b':
            data.iloc[:, 1:] = data.iloc[:, 1: ] - stats.trim_mean(data.iloc[0:200, 1:], 0.2)
        elif rezero == 'e':
            data.iloc[:, 1:] = data.iloc[:, 1: ] - stats.trim_mean(data.iloc[-200: , 1:], 0.2)
    
    return data, samp, weight



#%%
"""
combine_force
    Combine all force plates to time, fx, fy, fz
    
Inputs
    file: DATAFRAME force data from ImportForce_TXT module
    
Outputs
    data_combined: DATAFRAME combined force data (time, fx, fy, fz)
"""
def combine_force(data):
    
    ### find time
    t = data.iloc[:,0]
    # filter to fx, fy, fz
    fx = data.filter(regex = 'Fx').sum(axis=1)
    fy = data.filter(regex = 'Fy').sum(axis=1)
    fz = data.filter(regex = 'Fz').sum(axis=1)
    
    ### combine to dataframe
    data_combined = pd.DataFrame({'time': t,
                                  'fx': fx,
                                  'fy': fy,
                                  'fz': fz})
    
    
    return data_combined
    