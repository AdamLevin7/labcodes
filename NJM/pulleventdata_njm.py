# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 23:04:16 2020

pulleventdata_njm
    Pull the variables needed to calculate NJMs from Python structures for a specific event using the time.
    
Modules:
    find_nearest: Function pulled from internet for finding value closest to input value
    pulleventvars: Module that extracts data for an event to calculate NJMs by hand. 
    
Inputs
    time: NUM Numerical value of the time of interest
    data: OBJ Python structure with data of interest for calculating NJMs
        
Outputs
    eventvars: OBJ containing all data needed to calculate NJM
    
Dependencies
    pandas
    numpy
    
Syntax
    eventvarstest = pulleventvars(time=0.053, data= jk_obj)

@author: hestewar, Harper Stewart, hestewar@usc.edu
"""
import numpy as np
import pandas as pd

# Module copied from internet for finding closest value
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def pulleventvars(time, data):
    # Finds nearest time and index
    neartime1, ind1 = find_nearest(data.data_dig_njm["time"],time)

    # Finds the endpoint loctations and COM locations
    endptlocs_event = data.data_dig_njm.iloc[ind1]
    cmlocs_event = data.data_cm_njm.iloc[ind1]
    
    # Find the data_force info
    force_event = data.data_force.iloc[ind1]
    
    # Find the NJM variables for the event
    njm_event = data.iloc[ind1]
    
    # Pull the segment parameters (mass and radius of gyration parameters)
    segparams = data.segments

    # Return the dataframes/key information or combine into one output
    return endptlocs_event, cmlocs_event, force_event, njm_event, segparams
