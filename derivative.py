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
    
    #%% do not do calculations on frame or time column (if exists)
    cols = [c for c in d.columns if c.lower() not in ["frame", "time"]]
    fortcol = [c for c in d.columns if c.lower() in ["frame", "time"]]
    
    #%% find first and last valid index
    ind_first = d.first_valid_index()
    ind_last = d.last_valid_index()
    
    #%% foward difference for first frame
    d.loc[ind_first, cols] = (f.loc[ind_first+1, cols] - f.loc[ind_first, cols]) / dt
    
    #%% central difference for all but first and last frame
    for cnt in range(ind_first+1,ind_last):
        d.loc[cnt, cols] = (f.loc[cnt+1, cols] - f.loc[cnt-1, cols]) / (2*dt)
    
    #%% backward difference for last frame
    d.loc[ind_last, cols] = (f.loc[ind_last, cols] - f.loc[ind_last-1, cols]) / dt
    
    #%% add back frame or time column
    d[fortcol] = f[fortcol]
    
    #%% export data
    return d