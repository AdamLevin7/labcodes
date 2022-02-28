"""
Script: calc_segmentmomentinertia
    Calculate the moment of inertia for a segment.

Modules
    momentinertia: Calculate moment of inertia for each segment.

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def momentinertia(datain, segments, mass):
    """
    Function::: momentinertia
    	Description: brief description here (1 line)
    	Details: Full description with details here

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
    """

    # Dependencies
    import pandas as pd
    import numpy as np
    
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