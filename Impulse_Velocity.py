"""
Script: Impulse_Velocity
    Calculate impulse and change in velocity throughout duration.

Modules
    imp_vel: Calculate impulse and change in velocity throughout duration.
Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def imp_vel(data, bw, samp=1200):
    """
    Function::: imp_vel
    	Description: Calculate impulse and change in velocity throughout duration.
    	Details:

    Inputs
        data: DATAFRAME Mx3 dataframe of force data (includes X, Y, and Z !)
        bw: FLOAT participant's body weight in Newtons
        samp: INT sampling rate of force plate (default: 1200)

    Outputs
        imp: DATAFRAME net impulse of X, Y, Z, and positive impulse Z (Ns)
        velD: DATAFRAME change in velocity of X, Y, and Z (m/s)

    Dependencies
        pandas
    """

    # Dependencies
    import pandas as pd
    
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