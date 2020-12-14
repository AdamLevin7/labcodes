# -*- coding: utf-8 -*-
"""
projectiletraj
    Create data frame containing time, x, and y position of object during flight.
        
Inputs
    x_i: FLOAT initial x position (m)
    y_i: FLOAT initial y position (m)
    vx_i: FLOAT initial x velocity (m/s)
    vy_i: FLOAT initial y velocity (m/s)
    t_flight: FLOAT flight time (s)
    samp: FLOAT sampling rate of video (Hz)
    
Outputs
    pos: DATAFRAME contains array of time, x, and y position during flight
    
Uses equations of projectile motion.

Created on Wed May 20 10:59:52 2020

@author: cwiens
"""

import numpy as np
import pandas as pd

def flighttraj(x_i, y_i, vx_i, vy_i, t_flight, samp):
    
    ### create array of flight time
    t = np.arange(0, t_flight, 1/samp)
    
    ### horizontal position
    # x_f = x_i + vx_i * t
    x = x_i + vx_i * t
    
    ### vertical position
    # x_f = x_i + vx_i * t + 0.5 * a_x * t^2
    y = y_i + vy_i * t + 0.5 * -9.81 * np.square(t)
    
    ### save as data frame
    pos = pd.DataFrame({'t': t,
                        'x': x,
                        'y': y})
    
    
    return pos
