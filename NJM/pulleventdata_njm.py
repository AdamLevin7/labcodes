"""
Script: pulleventdata_njm
    Pull the variables needed to calculate NJMs from Python structures for a specific event using the time.

Modules
    find_nearest: Function pulled from internet for finding value closest to input value
    pulleventvars: Module that extracts data for an event to calculate NJMs by hand.

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""


def find_nearest(array, value):
    """
    Function::: find_nearest
    	Description: Function pulled from internet for finding value closest to input value
    	Details: Module copied from internet for finding closest value

    Inputs
        array: ARRAY of values
        value: FLOAT Number that each value in array will be compared to find the closest one

    Outputs
        array[idx]: FLOAT Return the number closest to the value
        idx: INT Index of the value selected
    Dependencies
        numpy

    """
    # Dependencies
    import numpy as np

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def pulleventvars(time, data_raw, data_njm_py):
    """
    Function::: pulleventvars
        Description: Module that extracts data for an event to calculate NJMs by hand.
        Details:

    Inputs
        time: NUM Numerical value of the time of interest
        data_raw: OBJ Python structure with data of interest for calculating NJMs
        data_njm_py: DATAFRAME dataframe containing NJM calculations over time, can use to check values

    Outputs
        eventvars: TUPLE containing all data needed to calculate NJM

    Dependencies
        None
    """
    # Dependencies

    # Finds nearest time and index
    neartime1, ind1 = find_nearest(data_raw.data_dig_njm["time"],time)

    # Finds the endpoint loctations and COM locations
    dig_njm_event = data_raw.data_dig_njm.iloc[ind1]
    cm_njm_event = data_raw.data_cm_njm.iloc[ind1]
    
    # Find the data_force info
    force_event = data_raw.data_force.iloc[ind1]
    
    # Find the NJM variables for the event
    cm_acc_njm_event = data_raw.data_cm_acc_njm.iloc[ind1]
    njm_event = data_njm_py.iloc[ind1]
    
    # Pull the segment parameters (mass and radius of gyration parameters)
    segparams = data_raw.segments
    segang_acc_njm_event = data_raw.data_segang_acc_njm.iloc[ind1]

    # Return the dataframes/key information or combine into one output
    return dig_njm_event, cm_njm_event, force_event, segparams, segang_acc_njm_event, cm_acc_njm_event, njm_event
