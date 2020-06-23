# -*- coding: utf-8 -*-
"""
calc_segmentlength
    Calculate length for each segment.
    
Inputs
    data: DATAFRAME digitized data for each segment
        Column 0: time or frame number
        Column 1+: digitized locations with x then y
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    dataout: DATAFRAME length of each segment (in units it was provided)
    
Dependencies
    pandas
    numpy

Created on Tue Apr 21 14:27:53 2020

@author: cwiens
"""

import pandas as pd
import numpy as np

def calc_length(segname, origin, other):
    # convert column names
    origin.columns = ['x', 'y']
    other.columns = ['x', 'y']
    # calculate segment length
    # sqrt( (x2 - x1)^2 + (y2 - y1)^2 )
    seg_length = pd.DataFrame({segname: np.sqrt(np.sum(np.square(origin - other), axis=1))})
    
    
    return seg_length



def seglength(datain, segments):
    
    # initialize data out
    dataout = pd.DataFrame(datain.iloc[:,0])
    
    # loop through segments
    for cnt in range(len(segments)):
        # if it is head
        if (segments.iloc[cnt,:]).name == 'head':
            # origin
            orig = datain.filter(regex = segments['origin'][cnt])
            # other
            oth = datain.filter(regex = segments['other'][cnt])
            # calculate length of segment
            seg_len = calc_length((segments.iloc[cnt,:]).name, orig, oth)
            # add column to data out
            dataout = dataout.join(seg_len)
            
        # if it is trunk
        elif (segments.iloc[cnt,:]).name == 'trunk':
            # origin
            orig = datain.filter(regex = segments['origin'][cnt])
            # other
            oth = datain.filter(regex = segments['other'][cnt])
            # if both hips were located, use average
            if len(oth.columns) > 2:
                oth = pd.DataFrame({'x': oth.filter(regex='x').mean(axis = 1),
                                    'y': oth.filter(regex='y').mean(axis = 1)})
            # calculate length of segment
            seg_len = calc_length((segments.iloc[cnt,:]).name, orig, oth)
            # add column to data out
            dataout = dataout.join(seg_len)
            
        # if another segment
        else:
            # origin
            orig = datain.filter(regex = segments['origin'][cnt])
            # find if location exists in digitized data set
            if len(orig.columns) > 0:
                # find if left and right segments were specified
                orig_l = orig.filter(regex = 'left')
                orig_r = orig.filter(regex = 'right')
            # other
            oth = datain.filter(regex = segments['other'][cnt])
            # find if location exists in digitized data set
            if len(oth.columns) > 0:
                # find if left and right segments were specified
                oth_l = oth.filter(regex = 'left')
                oth_r = oth.filter(regex = 'right')
              
            # if both origin and other locations exist
            if (len(orig.columns)>0 and len(oth.columns)>0):
                # if left segment exists
                if (len(orig_l.columns)>0 or len(oth_l.columns)>0):
                    # calculate length of segment
                    seg_len_l = calc_length((segments.iloc[cnt,:]).name + '_left', orig_l, oth_l)
                    # add column to data out
                    dataout = dataout.join(seg_len_l)
                # if right segment exists
                if (len(orig_r.columns)>0 or len(oth_r.columns)>0):
                    # calculate length of segment
                    seg_len_r = calc_length((segments.iloc[cnt,:]).name + '_right', orig_r, oth_r)
                    # add column to data out
                    dataout = dataout.join(seg_len_r)
                # if neither left or right exists
                if (len(orig_l.columns)==0) and (len(orig_r.columns)==0):
                    # calculate length of segment
                    seg_len = calc_length((segments.iloc[cnt,:]).name, orig, oth)
                    # add column to data out
                    dataout = dataout.join(seg_len)
    
    
    return dataout
