# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 23:04:16 2020

pulleventdata_njm
    Pull the variables needed to calculate NJMs from Python structures for a specific event using the time.
    
Inputs
    time: NUM Numerical value of the time of interest
    data_reformat_obj: OBJ Python structure with data of interest
    data_njm: DATAFRAME pandas dataframe with njm variables
        
Outputs
    ** TBD 
    eventvars: ?? Probably an object with all the values in it?
    
Dependencies
    pandas
    numpy
    ** TBD
    
Syntax
    eventvarstest = pulleventvars(time=0.053, data_reformat_obj=data_reformat_obj, data_njm=data_njm)

Things to Improve:
     Could be good to create a smaller module that pulls all needed info for specified segment
# Then repeatedly use it for whatever segments are needed

@author: hestewar, Harper Stewart, hestewar@usc.edu
"""
import numpy as np
import pandas as pd

# Module copied from internet for finding closest value
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def pulleventvars(time, data_reformat_obj, data_njm):
    # Finds nearest time and index for digitized data
    neartime1, ind1 = find_nearest(data_reformat_obj.data_dig["time"],time)
    # Find nearest time and index for njm/force data
    neartime2, ind2 = find_nearest(data_njm["time"],time)
    
    # Finds the endpoint loctations and COM locations
    endptlocs_event = data_reformat_obj.data_dig.iloc[ind1]
    cmlocs_event = data_reformat_obj.data_cm.iloc[ind1]
    
    # Find the data_force info
    force_event = data_reformat_obj.data_force.iloc[ind2]
    
    # Find the NJM variables for the event
    njm_event = data_njm.iloc[ind2]
    
    # Create object that contains all necessary variables
    ## Should definitely create a class and fix this but feeling lazy for now*
    
    eventvars = [endptlocs_event, cmlocs_event, force_event, njm_event]
        
    return eventvars




 