# -*- coding: utf-8 -*-
"""
dig2jointkinetics
    Modules to go from digitized data to joint kinetics calculations.
    
Modules
    filtdata: filters all but first column of dataframe
    interpdatasig: interpolates all but first column of dataframe
    datainterp: filter and interpolates CM and digitized data to match force data
    cm_angularimpulse: calculate angular impulse about body center of mass
    cm_velocityacceleration: calculate center of mass velocity and acceleration
    segmentangle_vel_acc: calculate segment angle, angular velocity, and angular acceleration
    jointangle_vel: calculate joint angle and angular velocity
    selectdata: select only data to be used in joint kinetics calculations
    main: run through all modules in specified order to calculate joint kinetics
    
Dependencies
    scipy    
    pandas
    numpy
    seglength from calc_segmentlength.py
    centraldiff from derivative.py
    segangle from calc_segmentangle.py
    jointangle from calc_jointangle.py
    momentinertia from calc_segmentmomentinertia.py
    njm_setup from jointkinetics
    
Created on Tue Apr 21 14:26:27 2020

@author: cwiens
"""


from scipy import signal
from scipy.interpolate import splev, splrep
import pandas as pd
import numpy as np
from calc_segmentlength import seglength
from derivative import centraldiff
from calc_segmentangle import segangle
from calc_jointangle import jointangle
from calc_segmentmomentinertia import momentinertia
from jointkinetics import njm_full

#%%    
"""
filtdata
    filters all but first column of dataframe
    
Inputs
    df: DATAFRAME data with columns to be filtered (first column will not be)
    b: ARRAY_LIKE numerator coefficient vector of the filter
    a: ARRAY_LIKE denominator coefficient vector of the filter
    
Outputs
    DATAFRAME same as df but filtered columns
"""
# function to filter data
def filtdata(df, b, a):
    # replace any missing values
    sig = df.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill'))
    # filter data
    return sig.apply(lambda x: signal.filtfilt(b, a, x))

#%%    
"""
interpdatasig
    interpolates all but first column of dataframe
    
Inputs
    df: DATAFRAME data with columns to be filtered (first column will not be)
    xvals: 1-D FLOATS x-coordinates of new data series
    samp: INT sampling rate of signal
    
Outputs
    DATAFRAME same as df but interpolated columns
"""
# function to interpolate data
def interpdatasig(df, xvals, samp):
    # create original time seires
    xp = df['time']
    # interpolate data
    return df.iloc[:,1:].apply(lambda y: splev(xvals, splrep(xp, y)))


#%%    
"""
datainterp
    filter and interpolates CM and digitized data to match force data
    
Inputs
    data_dig: DATAFRAME digitized data (m)
    data_cm: DATAFRAME center of mass data for segments and body (m)
    xvals: 1-D FLOATS x-coordinates for new data series
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    mass: FLOAT individual/system's mass (kg)
    contact_seg: STR name of segment that is in contact with force sensor.
        Denote of it is left or right (ex. 'right foot')
    samp: INT sampling rate of signal
    
Outputs
    data_dig_interp: DATAFRAME filtered and interpolated digitized data (m)
    data_cm_interp: DATAFRAME filtered and interpolated center of mass data (m)
    data_seglength_interp: DATAFRAME filtered and interpolated segment length data (m)
"""
def datainterp(data_dig, data_cm, xvals, segments, mass, contact_seg, samp=240):
    ### calculate segmental distances
    # find segment lengths of each frame
    data_seglength = seglength(data_dig, segments)
    
    ### filter position and segment length data
    # 4th order butterworth filter
    N = 4
    # cut-off frequency of the filter
    fc = 10
    # normalize the frequency
    w = fc / (samp / 2)
    b, a = signal.butter(N/2, w, 'low')
    # digitized data
    data_dig_filt = pd.DataFrame({'time': data_dig.iloc[:,0]}).join(filtdata(data_dig, b, a))
    # center of mass data
    data_cm_filt = pd.DataFrame({'time': data_cm.iloc[:,0]}).join(filtdata(data_cm, b, a))
    # segment length
    data_seglength_filt = pd.DataFrame({'time': data_seglength.iloc[:,0]}).join(filtdata(data_seglength, b, a))
    
    ### interpolate kinematic data
    # digitized data
    data_dig_interp = pd.DataFrame({'time': xvals}).join(interpdatasig(data_dig_filt, xvals, samp).set_index(xvals.index))
    # center of mass data
    data_cm_interp = pd.DataFrame({'time': xvals}).join(interpdatasig(data_cm_filt, xvals, samp).set_index(xvals.index))
    # segment length data
    data_seglength_interp = pd.DataFrame({'time': xvals}).join(interpdatasig(data_seglength_filt, xvals, samp).set_index(xvals.index))
    
    
    return data_dig_interp, data_cm_interp, data_seglength_interp



#%%
"""
cm_angularimpulse
    calculate angular impulse about body center of mass
    
Inputs
    data_force: DATAFRAME force data (fx, fy, ax, ay) (N, N, m, m)
    data_cm: DATAFRAME center of mass data for segments and body (m).
        Dataframe obtained from calc_centermass.py
        Data should be same length as force data.
    
Outputs
    cm_moment: ARRAY moment about center of mass (N*m)
    cm_theta: ARRAY angle between center of mass and reaction force (rad)
"""
def cm_angularimpulse(data_force, data_cm):
    ### calculate angular impulse about body center of mass
    # create vector from center of mass to center of pressure
    cm_r = pd.DataFrame({'x': data_force['ax'].values - data_cm['body_x'].values,
                         'y': data_force['ay'].values - data_cm['body_y'].values})
    # calculate moment about center of mass
    cm_moment = np.cross(cm_r, data_force[['fx','fy']])
    # calculate center of mass theta
    cm_theta = np.arctan2(-cm_r['y'], -cm_r['x'])
    
    
    return cm_moment, cm_theta



#%%    
"""
cm_velocityacceleration
    calculate center of mass velocity and acceleration
    
Inputs
    data_cm: DATAFRAME center of mass data for segments and body (m).
        Dataframe obtained from calc_centermass.py
        Data should be same length as force data.
    xvals: 1-D FLOATS x-coordinates for new data series
    samp: INT sampling rate of signal
    
Outputs
    data_cm_vel_filt: DATAFRAME filtered center of mass velocity data for segments and body (m/s)
    data_cm_acc_filt: DATAFRAME filtered center of mass acceleration data for segments and body (m/s^2)
"""
def cm_velocityacceleration(data_cm, xvals, samp):
    #%% calculate center of mass velocities and accelerations
    # 4th order butterworth filter
    N = 4
    # cut-off frequency of the filter
    fc = 6
    # normalize the frequency
    w = fc / (samp / 2)
    b, a = signal.butter(N/2, w, 'low')
    # center of mass velocities
    data_cm_vel = centraldiff(data_cm, (1/samp))
    # replace time series
    data_cm_vel['time'] = xvals
    # filter center of mass velocities
    data_cm_vel_filt = pd.DataFrame({'time': xvals}).join(filtdata(data_cm_vel, b, a))
    # center of mass accelerations
    data_cm_acc = centraldiff(data_cm_vel_filt, np.mean(np.diff(data_cm_vel_filt['time'])))
    # replace time series
    data_cm_acc['time'] = xvals
    # filter center of mass accelerations
    data_cm_acc_filt = pd.DataFrame({'time': xvals}).join(filtdata(data_cm_acc, b, a))
    
    
    return data_cm_vel_filt, data_cm_acc_filt



#%%    
"""
segmentangle_vel_acc
    calculate segment angle, angular velocity, and angular acceleration
    
Inputs
    data_dig: DATAFRAME digitized data (m)
    xvals: 1-D FLOATS x-coordinates for new data series
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    data_segang: DATAFRAME segment angle data (rad)
    data_segang_vel: DATAFRAME segment angular velocity data (rad/s)
    data_segang_acc: DATAFRAME segment angular acceleration data (rad/s^2)
"""
def segmentangle_vel_acc(data_dig, xvals, segments):
    ### calculate segmental angles
    data_segang = segangle(data_dig, segments, allpositive='yes')
    
    ### calculate segmental angular velocities
    # segmental angular velocities
    data_segang_vel = centraldiff(data_segang, np.mean(np.diff(data_segang['time'])))
    # replace time series
    data_segang_vel['time'] = xvals
    
    ### calculate segmental angular accelerations
    # segmental angular velocities
    data_segang_acc = centraldiff(data_segang_vel, np.mean(np.diff(data_segang_vel['time'])))
    # replace time series
    data_segang_acc['time'] = xvals
    
    
    return data_segang, data_segang_vel, data_segang_acc



#%%    
"""
jointangle_vel
    calculate joint angle and angular velocity
    
Inputs
    data_dig: DATAFRAME digitized data (m)
    xvals: 1-D FLOATS x-coordinates for new data series
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    data_jointang: DATAFRAME joint angle data (rad)
    data_jointang_vel: DATAFRAME joint angular velocity data (rad/s)
"""
def jointangle_vel(data_dig, xvals, segments):
    ### calculate joint angles and angular velocities
    # calculate joint angles
    data_jointang = jointangle(data_dig, segments)
    # calculate joint angular velocities
    data_jointang_vel = centraldiff(data_jointang, np.mean(np.diff(data_jointang['time'])))
    # replace time series
    data_jointang_vel['time'] = xvals
    
    
    return data_jointang, data_jointang_vel



#%%
"""
selectdata
    select only data to be used in joint kinetics calculations
    
Inputs
    data_dig: DATAFRAME digitized data (m)
    data_cm: DATAFRAME center of mass data for segments and body (m).
        Dataframe originally obtained from calc_centermass.py
    data_cm_acc: DATAFRAME center of mass acceleration data (m/s^2)
    data_i: DATAFRAME moment of inertia of each segment (obtained from calc_segmentmomentinertia.py)
    data_segang_acc: DATAFRAME segment angular acceleration data (rad/s^2)
    contact_seg: STR name of segment that is in contact with force sensor.
        Denote of it is left or right (ex. 'right foot')
    
Outputs
    data_dig_njm: DATAFRAME subset of digitized data to use in joint kinetics (m)
    data_cm_njm: DATAFRAME subset of center of mass data to use in joint kinetics (m)
    data_cm_acc_njm: DATAFRAME subset of center of mass acceleration data to use in joint kinetics (m/s^2)
    data_i_njm: DATAFRAME subset of moment of inertia data to use in joint kinetics
    data_segang_acc_njm: DATAFRAME subset of segment angular acceleration data to use in joint kinetics (rad/s^2)
    seg_sequence: LIST segment sequence for order to calculate joint kinetics
"""
def selectdata(data_dig, data_cm, data_cm_acc, data_i, data_segang_acc, contact_seg):
    ### identify segment sequence 
    if 'foot' in contact_seg:
        seg_sequence = ['foot', 'shank', 'thigh', 'trunk']
    elif 'hand' in contact_seg:
        pass
    
    ### identify left, right, or not specified side
    if 'left' in contact_seg:
        seg_side = 'left'
    elif 'right' in contact_seg:
        seg_side = 'right'
    else:
        seg_side = None
        
    ### create dataframe of only segments in seg_sequence list
    data_cm_njm = data_cm[[s for s in data_cm.columns if any(xs in s for xs in seg_sequence)]]
    data_cm_acc_njm = data_cm_acc[[s for s in data_cm_acc.columns if any(xs in s for xs in seg_sequence)]]
    data_i_njm = data_i[[s for s in data_i.columns if any(xs in s for xs in seg_sequence)]]
    data_segang_acc_njm = data_segang_acc[[s for s in data_segang_acc.columns if any(xs in s for xs in seg_sequence)]]
    
    ### filter by side
    if seg_side == 'left':
        # remove columns with 'right'
        data_dig_njm = data_dig.iloc[:,~data_dig.columns.str.contains('right')]
        data_cm_njm = data_cm_njm.iloc[:,~data_cm_njm.columns.str.contains('right')]
        data_cm_acc_njm = data_cm_acc_njm.iloc[:,~data_cm_acc_njm.columns.str.contains('right')]
        data_i_njm = data_i_njm.iloc[:,~data_i_njm.columns.str.contains('right')]
        data_segang_acc_njm = data_segang_acc_njm.iloc[:,~data_segang_acc_njm.columns.str.contains('right')]
    elif seg_side == 'right':
        # remove columns with 'left'
        data_dig_njm = data_dig.iloc[:,~data_dig.columns.str.contains('left')]
        data_cm_njm = data_cm_njm.iloc[:,~data_cm_njm.columns.str.contains('left')]
        data_cm_acc_njm = data_cm_acc_njm.iloc[:,~data_cm_acc_njm.columns.str.contains('left')]
        data_i_njm = data_i_njm.iloc[:,~data_i_njm.columns.str.contains('left')]
        data_segang_acc_njm = data_segang_acc_njm.iloc[:,~data_segang_acc_njm.columns.str.contains('left')]
    else:
        data_dig_njm = data_dig
    
    
    return data_dig_njm, data_cm_njm, data_cm_acc_njm, data_i_njm, data_segang_acc_njm, seg_sequence



#%%
"""
main
    run through all modules in specified order to calculate joint kinetics
    
Inputs
    data_dig: DATAFRAME digitized data (m)
    data_cm: DATAFRAME center of mass data for segments and body (m).
        Dataframe originally obtained from calc_centermass.py
    data_force: DATAFRAME force data (fx, fy, ax, ay) (N, N, m, m)
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    mass: FLOAT individual/system's mass (kg)
    contact_seg: STR name of segment that is in contact with force sensor.
        Denote of it is left or right (ex. 'right foot')
    xvals: 1-D FLOATS x-coordinates for new data series
    samp_dig: INT sampling rate of digitized data (default=240)
    samp_force: INT sampling rate of force data (default=1200)
    
Outputs
    data_njm: DATAFRAME calculated joint kinetics variables from jointkinetics.py
"""
def main(data_dig, data_cm, data_force, segments, mass, contact_seg, xvals, samp_dig=240, samp_force=1200):
    ### filter and interpoloate data
    data_dig_interp, data_cm_interp, data_seglength_interp = datainterp(data_dig, data_cm, xvals, segments, mass, contact_seg, samp_dig)
    
    ### calculate center of mass velocity and acceleration
    data_cm_vel, data_cm_acc = cm_velocityacceleration(data_cm_interp, xvals, samp_force)
    
    ### calculate segment angle, angular velocity, and angular acceleration
    data_segang, data_segang_vel, data_segang_acc = segmentangle_vel_acc(data_dig_interp, xvals, segments)
    
    ### calculate joint angle and angular velocity
    data_jointang, data_jointang_vel = jointangle_vel(data_dig_interp, xvals, segments)
    
    ### calculate segment moment of inertia
    data_i = momentinertia(data_seglength_interp, segments, mass)
    
    ### select data to be used in joint kinetics calculations
    data_dig_njm, data_cm_njm, data_cm_acc_njm, data_i_njm, data_segang_acc_njm, seg_sequence = selectdata(data_dig_interp, data_cm_interp, data_cm_acc, data_i, data_segang_acc, contact_seg)
    
    ### calculate joint kinetics
    data_njm = njm_full(data_dig_njm, data_cm_njm, data_cm_acc_njm, data_i_njm, data_segang_acc_njm, data_force, mass, seg_sequence, segments)
    
    
    return data_njm