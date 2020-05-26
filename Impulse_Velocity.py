# -*- coding: utf-8 -*-
"""
Impulse_Velocity
    Calculate impulse and change in velocity.

Input
    data: DATAFRAME Mx3 dataframe of force data (includes X, Y, and Z !)
    BW: FLOAT participant's body weight in Newtons
    samp: INT sampling rate of force plate
    
Output
    imp: DATAFRAME net impulse of X, Y, Z, and positive impulse Z (Ns)
    velD: DATAFRAME change in velocity of X, Y, and Z (m/s)
    
Dependencies
    pandas

Created on Fri Nov  8 20:06:55 2019

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import pandas as pd

def imp_vel(data, BW, samp):
    
    # column names
    col = data.columns
    
    ### calculate impulse
    imp = pd.DataFrame({col[0]: [data[col[0]].sum()/samp],
                        col[1]: [data[col[1]].sum()/samp],
                        col[2]: [(data[col[2]]-BW).sum()/samp],
                        col[2] + '_positive': [data[col[2]].sum()/samp]})
    
    ### calculate change in velocity
    velD = imp[col[0:3]] / (BW / 9.81)
    
    return imp, velD