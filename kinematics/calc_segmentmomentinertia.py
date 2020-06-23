# -*- coding: utf-8 -*-
"""
calc_segmentmomentinertia
    Calculate moment of inertia for each segment.
    
Inputs
    data: DATAFRAME digitized data for each segment
        Column 0: time or frame number
        Column 1+: length of the segment
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    dataout: DATAFRAME moment of inertia of each segment
    
Dependencies
    pandas
    numpy
    
Created on Sat Apr 25 13:06:44 2020

@author: cwiens
"""

import pandas as pd
import numpy as np

def momentinertia(datain, segments, mass):
    
    # initialize data out
    dataout = pd.DataFrame(datain.iloc[:,0])
    
    # loop through segments
    for cnt in range(len(segments)):
        # find segment column(s)
        seg = datain.filter(regex = segments.iloc[cnt,:].name)
        # calculate segments moment of inertia
        # segment_mass * (segment_length * %radius_gyration)^2
        i = (segments['massper'].iloc[cnt]*mass) * np.square((seg * segments['r_gyr'].iloc[cnt]))
        # join with new dataframe
        dataout = dataout.join(i)
            
    
    
    return dataout
