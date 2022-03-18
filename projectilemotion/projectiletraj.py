"""
Script: projectiletraj
    Create data frame containing time, x, and y position of object during flight.
    Uses equations of projectile motion.

Modules
    flighttraj: module description here
    flighttraj_pixels: module description here

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def flighttraj(x_i, y_i, vx_i, vy_i, t_flight, samp):
    """
    Function::: flighttraj
    	Description: Create data frame containing time, x, and y position of object during flight.
    	Details: Uses equations of projectile motion.

    Inputs
        x_i: FLOAT initial x position (m)
        y_i: FLOAT initial y position (m)
        vx_i: FLOAT initial x velocity (m/s)
        vy_i: FLOAT initial y velocity (m/s)
        t_flight: FLOAT flight time (s)
        samp: FLOAT sampling rate of video (Hz)

    Outputs
        pos: DATAFRAME contains array of time, x, and y position during flight

    Dependencies
        numpy
        pandas
    """
    # Dependencies
    import numpy as np
    import pandas as pd
    
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


def flighttraj_pixels(x_i, y_i, vx_i, vy_i, frame_start, frame_end, pix2m, samp,
                      thresh=0.2, flip_x='no', flip_y='yes'):
    """
    Function::: flighttraj_pixels
    	Description: Calculate flight trajectory in pixels
    	Details: Full description with details here

    Inputs
        x_i: FLOAT initial x position (m)
        y_i: FLOAT initial y position (m)
        vx_i: FLOAT initial x velocity (m/s)
        vy_i: FLOAT initial y velocity (m/s)
        frame_start: INT Frame where flight trajectory should start
        frame_end: INT Frame where flight trajectory should end
        pix2m: FLOAT Pixel to meter ratio of the video
        samp: FLOAT sampling rate of video (Hz)
        thresh: FLOAT Threshold padding for velocity (will define the trajectories above and below the projection)
            ie. 0.2 would add 0.2m/s in x and y to the calculated values
        flip_x: STR Flip x coordinates of the video
        flip_y: STR Flip y coordinates of the video

    Outputs
        pos_pix: DF x and y coordinates of the projectile motion trajectory
        pos_pix_max: DF x and y coordinates of the projectile motion trajectory minimum of the velocity range
        pos_pix_min: DF x and y coordinates of the projectile motion trajectory maximum of the velocity range

    Dependencies
        numpy
        pandas
    """

    # Dependencies
    import numpy as np
    import pandas as pd

    """ check if position is in pixel or meters """
    if x_i > 200 or y_i > 200:
        # change to meters
        x_i = x_i * pix2m
        y_i = y_i * pix2m

    """ flight time """
    t_flight = (frame_end - frame_start ) / samp
    
    """ calculate  trajectory """
    # find position during flight ACTUAL FLIGHT
    pos = flighttraj(x_i, y_i, vx_i, vy_i, t_flight, samp)
    # join with frame number and convert back to pixels
    pos_pix = pd.DataFrame({'frame': np.arange(frame_start, frame_end)}).join(pos[['x','y']] / pix2m)
    
    
    """ calculate max range trajectory """
    # find position during flight MAX RANGE
    pos_max = flighttraj(x_i, y_i, vx_i+thresh, vy_i+thresh, t_flight, samp)
    # join with frame number and convert back to pixels
    pos_pix_max = pd.DataFrame({'frame': np.arange(frame_start, frame_end)}).join(pos_max[['x','y']] / pix2m)
    
    
    """ calculate min range trajectory """
    # find position during flight MIN RANGE
    pos_min = flighttraj(x_i, y_i, vx_i-thresh, vy_i-thresh, t_flight, samp)
    # join with frame number and convert back to pixels
    pos_pix_min = pd.DataFrame({'frame': np.arange(frame_start, frame_end)}).join(pos_min[['x','y']] / pix2m)
    
    
    """ flip x """
    if flip_x == 'yes':
        pos_pix['x'] = pos_pix['x'][0] - (pos_pix['x'] - pos_pix['x'][0])
        pos_pix_max['x'] = pos_pix_max['x'][0] - (pos_pix_max['x'] - pos_pix_max['x'][0])
        pos_pix_min['x'] = pos_pix_min['x'][0] - (pos_pix_min['x'] - pos_pix_min['x'][0])
    """ flip y """
    if flip_y == 'yes':
        pos_pix['y'] = pos_pix['y'][0] - (pos_pix['y'] - pos_pix['y'][0])
        pos_pix_max['y'] = pos_pix_max['y'][0] - (pos_pix_max['y'] - pos_pix_max['y'][0])
        pos_pix_min['y'] = pos_pix_min['y'][0] - (pos_pix_min['y'] - pos_pix_min['y'][0])

    return pos_pix, pos_pix_max, pos_pix_min