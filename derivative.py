# -*- coding: utf-8 -*-
"""
derivative
    Calculate the derivative of the signal.
    
centraldiff:
    Uses the central difference method for all frames except the first and last
        frame. It uses the foward and backward difference method for the first
        and last frame, respectively.
    
Inputs
    f: DATAFRAME data signal to be derived
    dt: FLOAT time step
    
Outputs
    d: DATAFRAME derived data signal
    
Dependencies
    pandas
    numpy

Created on Wed Feb 12 09:54:29 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import pandas as pd
import numpy as np

def centraldiff(f, dt):
    
    #%% initialize derived data
    d = pd.DataFrame(np.zeros(f.shape, dtype=float), columns=f.columns, index=f.index)
    
    #%% foward difference for first frame
    d.iloc[0,:] = (f.iloc[1,:] - f.iloc[0,:]) / dt
    
    #%% central difference for all but first and last frame
    for cnt in range(1,len(f)-1):
        d.iloc[cnt,:] = (f.iloc[cnt+1,:] - f.iloc[cnt-1,:]) / (2*dt)
    
    #%% backward difference for last frame
    d.iloc[len(f)-1,:] = (f.iloc[-1,:] - f.iloc[-2,:]) / dt
    
    
    
    #%% export data
    return d