"""
Script: apdm_load
    Load APDM data.

Modules
    apdm_import: Reads in APDM's h5 file and creates dataframes

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def apdm_import(filename):
    """
    Function::: apdm_import
    	Description: Reads in APDM's h5 file and creates dataframes.
    	Details: For accelerometer, gyroscope, magnetometer, and quaternions. Uses the sampling rate of the sensors
    to set the time.

    Inputs
        filename: STR filename of the h5 file to be loaded

    Outputs
        acc_df: DATAFRAME accelerometer data from all sensors (x, y, z)
        gyro_df: DATAFRAME gyroscope data from all sensors (x, y, z)
        mag_df: DATAFRAME magnetometer data from all sensors (x, y, z)
        orient_df: DATAFRAME quaternion data from all sensors (r, x, y, z)
            [real (scalar), x (complex), y (complex), z (complex)]
        temp: FLOAT Temperature of the sensor during collection

    Dependencies
        pandas
        numpy
        h5py
    """

    """ import packages """
    import pandas as pd
    import numpy as np
    import h5py

    """ load h5 file """
    f = h5py.File(filename, 'r')

    """ set sensor counter """
    i = 0

    """ loop through sensors """
    for s in f['Sensors']:
        """ iterate sensor counter """
        i += 1

        """ load data """
        label = f['Sensors'][s]['Configuration'].attrs['Label 0']
        acc = f['Sensors'][s]['Accelerometer'][:]
        gyro = f['Sensors'][s]['Gyroscope'][:]
        mag = f['Sensors'][s]['Magnetometer'][:]
        orient = f['Processed'][s]['Orientation'][:]
        samp = f['Sensors'][s]['Configuration'].attrs['Sample Rate']
        
        # Not sure why this isn't working 
        #t['time'] = f['Sensors'][s]['Time'][:]
        #pressure = f['Sensors'][s]['Barometer'][:]
        
        """ reformat label name so it could be a part of column name """
        label = label.decode("utf-8").replace(" ", "")
        
        """ create time data frame """
        t = pd.DataFrame(np.arange(0, len(acc)) / samp, columns=['time'])

        """ convert data to data frame """
        if i == 1:
            acc_df = t.join(pd.DataFrame(acc, columns=[label + x for x in ['_x', '_y', '_z']]))
            gyro_df = t.join(pd.DataFrame(gyro, columns=[label + x for x in ['_x', '_y', '_z']]))
            mag_df = t.join(pd.DataFrame(mag, columns=[label + x for x in ['_x', '_y', '_z']]))
            orient_df = t.join(pd.DataFrame(orient, columns=[label + x for x in ['_r', '_x', '_y', '_z']]))
        else:
            acc_df = acc_df.join(pd.DataFrame(acc, columns=[label + x for x in ['_x', '_y', '_z']]))
            gyro_df = gyro_df.join(pd.DataFrame(gyro, columns=[label + x for x in ['_x', '_y', '_z']]))
            mag_df = mag_df.join(pd.DataFrame(mag, columns=[label + x for x in ['_x', '_y', '_z']]))
            orient_df = orient_df.join(pd.DataFrame(orient, columns=[label + x for x in ['_r', '_x', '_y', '_z']]))
            
    """ get temp and sampling rate from last sensor in collection"""        
    temp = f['Sensors'][s]['Temperature'][:][0] 
    

    return acc_df, gyro_df, mag_df, orient_df, temp, samp