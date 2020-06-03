# -*- coding: utf-8 -*-
"""
Impulse_Velocity
    Calculate impulse and change in velocity throughout duration.

Input
    data: DATAFRAME Mx3 dataframe of force data (includes X, Y, and Z !)
    bw: FLOAT participant's body weight in Newtons
    samp: INT sampling rate of force plate (default: 1200)
    
Output
    imp: DATAFRAME net impulse of X, Y, Z, and positive impulse Z (Ns)
    velD: DATAFRAME change in velocity of X, Y, and Z (m/s)
    
Dependencies
    pandas

Created on Fri Nov  8 20:06:55 2019

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import pandas as pd

def imp_vel(data, bw, samp=1200):
    
    # column names
    col = data.columns
    
    ### calculate impulse
    imp = pd.DataFrame({col[0]: data[col[0]].cumsum()/samp,
                        col[1]: data[col[1]].cumsum()/samp,
                        col[2]: (data[col[2]]-bw).cumsum()/samp,
                        col[2] + '_positive': data[col[2]].cumsum()/samp})
    
    ### calculate change in velocity
    velD = imp[col[0:3]] / (bw / 9.81)
    
    return imp, velD