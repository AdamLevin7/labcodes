"""
Script: calc_segmentangle
    Calculate segement angles using DeLeva parameters from digitized data.

Modules
    calc_angle: Calculate an individual segment angle
    segangle: Calculate the segment angles for the entire body

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def calc_angle(segname, origin, other, allpositive='no'):
    """
    Function::: calc_angle
    	Description: Calculate an individual segment angle
    	Details: Positive output values can be specified

    Inputs
        segname: STR description goes here (units)
        origin: DF x and y location of the origin
        other: DF x and y location of the other end of the line
        allpositive: STR Specify if all angles should be defined as positive numbers

    Outputs
        seg_angle: DF Contains the segment name and associated angle

    Dependencies
        pandas
        numpy
    """

    # Dependencies
    import pandas as pd
    import numpy as np

    # convert column names
    origin.columns = ['x', 'y']
    other.columns = ['x', 'y']
    # calculate segment angle
    # atan2( (y2 - y1) / (x2 - x1) )
    if 'foot' in segname:
        theta = np.arctan((origin['y'] - other['y']) / (origin['x'] - other['x']))
    else:
        theta = np.arctan2((origin['y'] - other['y']), (origin['x'] - other['x']))
    # make angle positive if instructed to do so
    if 'yes' in allpositive:
        def negative_clean_up(value):
            # convert negative value to positive
            if value<0:
                return(value + 2*np.pi)
            else:
                return(value)
        
        theta = theta.apply(negative_clean_up)
    # store as dataframe
    seg_angle = pd.DataFrame({segname: theta})

    return seg_angle


def segangle(datain, segments,allpositive='no'):
    """
    Function::: segangle
    	Description: Calculate the segment angles for the entire body
    	Details: Uses calc_angle for each segment

    Inputs
        data: DATAFRAME digitized data for each segment
            Column 0: time or frame number
            Column 1+: Coordinate of the segment
        segments: DATAFRAME segment parameters obtained from segdim_deleva.py
        allpositive: STR Specify if all angles should be defined as positive numbers

    Outputs
        dataout: DF Containing the segment angles of the body (radians)

    Dependencies
        pandas
    """

    # Dependencies
    import pandas as pd

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
            # calculate segment angle
            seg_ang = calc_angle((segments.iloc[cnt,:]).name, orig, oth, allpositive)
            # add column to data out
            dataout = dataout.join(seg_ang)
            
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
            # calculate segment angle
            seg_ang = calc_angle((segments.iloc[cnt,:]).name, orig, oth, allpositive)
            # add column to data out
            dataout = dataout.join(seg_ang)
            
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
                    # calculate segment angle
                    seg_ang_l = calc_angle((segments.iloc[cnt,:]).name + '_left', orig_l, oth_l, allpositive)
                    # add column to data out
                    dataout = dataout.join(seg_ang_l)
                # if right segment exists
                if (len(orig_r.columns)>0 or len(oth_r.columns)>0):
                    # calculate segment angle
                    seg_ang_r = calc_angle((segments.iloc[cnt,:]).name + '_right', orig_r, oth_r, allpositive)
                    # add column to data out
                    dataout = dataout.join(seg_ang_r)
                # if neither left or right exists
                if (len(orig_l.columns)==0) and (len(orig_r.columns)==0):
                    # calculate segment angle
                    seg_ang = calc_angle((segments.iloc[cnt,:]).name, orig, oth, allpositive)
                    # add column to data out
                    dataout = dataout.join(seg_ang)

    return dataout
