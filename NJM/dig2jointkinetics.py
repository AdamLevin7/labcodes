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


class dig2jk:
    
    def __init__(self, data_dig, data_cm, data_force, segments, mass,
                 contact_seg, xvals, samp_dig=240, samp_force=1200):
        # initialize variables
        self.data_dig = data_dig
        self.data_cm = data_cm
        self.data_force = data_force
        self.segments = segments
        self.mass = mass
        self.contact_seg = contact_seg
        self.xvals = xvals
        self.samp_dig = samp_dig
        self.samp_force = samp_force
    
    
    #%%    
    """
    datainterp
        filter and interpolates CM and digitized data to match force data
        
    Inputs
        data_dig: DATAFRAME digitized data (m)
        data_cm: DATAFRAME center of mass data for segments and body (m)
        xvals: 1-D FLOATS x-coordinates for new data series
        segments: DATAFRAME segment parameters obtained from segdim_deleva.py
        samp_dig: INT sampling rate of digitized data
        
    Outputs
        data_dig_interp: DATAFRAME filtered and interpolated digitized data (m)
        data_cm_interp: DATAFRAME filtered and interpolated center of mass data (m)
        data_seglength_interp: DATAFRAME filtered and interpolated segment length data (m)
    """
    def datainterp(self):
        ### calculate segmental distances
        # find segment lengths of each frame
        data_seglength = seglength(self.data_dig, self.segments)
        
        ### filter position and segment length data
        # 4th order butterworth filter
        N = 4
        # cut-off frequency of the filter
        fc = 10
        # normalize the frequency
        w = fc / (self.samp_dig / 2)
        b, a = signal.butter(N/2, w, 'low')
        # digitized data
        data_dig_filt = pd.DataFrame({'time': self.data_dig.iloc[:,0]}).join(self.data_dig.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # center of mass data
        data_cm_filt = pd.DataFrame({'time': self.data_cm.iloc[:,0]}).join(self.data_cm.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # segment length
        data_seglength_filt = pd.DataFrame({'time': data_seglength.iloc[:,0]}).join(data_seglength.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        
        ### interpolate kinematic data
        # digitized data
        self.data_dig_interp = pd.DataFrame({'time': self.xvals}).join(data_dig_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(data_dig_filt['time'], y))).set_index(self.xvals.index))
        # center of mass data
        self.data_cm_interp = pd.DataFrame({'time': self.xvals}).join(data_cm_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(data_cm_filt['time'], y))).set_index(self.xvals.index))
        # segment length data
        self.data_seglength_interp = pd.DataFrame({'time': self.xvals}).join(data_seglength_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(data_seglength_filt['time'], y))).set_index(self.xvals.index))
    
    
    
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
    def cm_angularimpulse(self):
        ### calculate angular impulse about body center of mass
        # create vector from center of mass to center of pressure
        cm_r = pd.DataFrame({'x': self.data_force['ax'].values - self.data_cm['body_x'].values,
                             'y': self.data_force['ay'].values - self.data_cm['body_y'].values})
        # calculate moment about center of mass
        self.cm_moment = np.cross(cm_r, self.data_force[['fx','fy']])
        # calculate center of mass theta
        self.cm_theta = np.arctan2(-cm_r['y'], -cm_r['x'])
    
    
    
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
    def cm_velocityacceleration(self):
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        
        ### calculate center of mass velocities and accelerations
        # 4th order butterworth filter
        N = 4
        # cut-off frequency of the filter
        fc = 6
        # normalize the frequency
        w = fc / (self.samp_force / 2)
        b, a = signal.butter(N/2, w, 'low')
        # center of mass velocities
        data_cm_vel = centraldiff(self.data_cm_interp, (1/self.samp_force))
        # replace time series
        data_cm_vel['time'] = self.xvals
        # filter center of mass velocities
        self.data_cm_vel_filt = pd.DataFrame({'time': self.xvals}).join(data_cm_vel.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # center of mass accelerations
        data_cm_acc = centraldiff(self.data_cm_vel_filt, (1/self.samp_force))
        # replace time series
        data_cm_acc['time'] = self.xvals
        # filter center of mass accelerations
        self.data_cm_acc_filt = pd.DataFrame({'time': self.xvals}).join(data_cm_acc.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
    
    
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
    def segmentangle_vel_acc(self):
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        
        ### calculate segmental angles
        self.data_segang = segangle(self.data_dig_interp, self.segments, allpositive='yes')
        
        ### calculate segmental angular velocities
        # segmental angular velocities
        self.data_segang_vel = centraldiff(self.data_segang, np.mean(np.diff(self.data_segang['time'])))
        # replace time series
        self.data_segang_vel['time'] = self.xvals
        
        ### calculate segmental angular accelerations
        # segmental angular velocities
        self.data_segang_acc = centraldiff(self.data_segang_vel, np.mean(np.diff(self.data_segang_vel['time'])))
        # replace time series
        self.data_segang_acc['time'] = self.xvals
    
    
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
    def jointangle_vel(self):
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        ### calculate segment angle, angular velocity, and angular acceleration
        dig2jk.segmentangle_vel_acc(self)
        
        ### calculate joint angles and angular velocities
        # calculate joint angles
        self.data_jointang = jointangle(self.data_dig_interp, self.segments)
        # calculate joint angular velocities
        self.data_jointang_vel = centraldiff(self.data_jointang, np.mean(np.diff(self.data_jointang['time'])))
        # replace time series
        self.data_jointang_vel['time'] = self.xvals
    
    
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
    def selectdata(self):
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        ### calculate segment angle, angular velocity, and angular acceleration
        dig2jk.segmentangle_vel_acc(self)
        ### calculate joint angle and angular velocity
        dig2jk.jointangle_vel(self)
        ### calculate segment moment of inertia
        data_i = momentinertia(self.data_seglength_interp, self.segments, self.mass)
        
        ### identify segment sequence 
        if 'foot' in self.contact_seg:
            self.seg_sequence = ['foot', 'shank', 'thigh', 'trunk']
        elif 'hand' in self.contact_seg:
            pass
        
        ### identify left, right, or not specified side
        if 'left' in self.contact_seg:
            seg_side = 'left'
        elif 'right' in self.contact_seg:
            seg_side = 'right'
        else:
            seg_side = None
            
        ### create dataframe of only segments in seg_sequence list
        self.data_cm_njm = self.data_cm_interp[[s for s in self.data_cm_interp.columns if any(xs in s for xs in self.seg_sequence)]]
        self.data_cm_acc_njm = self.data_cm_acc_filt[[s for s in self.data_cm_acc_filt.columns if any(xs in s for xs in self.seg_sequence)]]
        self.data_i_njm = data_i[[s for s in data_i.columns if any(xs in s for xs in self.seg_sequence)]]
        self.data_segang_acc_njm = self.data_segang_acc[[s for s in self.data_segang_acc.columns if any(xs in s for xs in self.seg_sequence)]]
        
        ### filter by side
        if seg_side == 'left':
            # remove columns with 'right'
            self.data_dig_njm = self.data_dig_interp.iloc[:,~self.data_dig_interp.columns.str.contains('right')]
            self.data_cm_njm = self.data_cm_njm.iloc[:,~self.data_cm_njm.columns.str.contains('right')]
            self.data_cm_acc_njm = self.data_cm_acc_njm.iloc[:,~self.data_cm_acc_njm.columns.str.contains('right')]
            self.data_i_njm = self.data_i_njm.iloc[:,~self.data_i_njm.columns.str.contains('right')]
            self.data_segang_acc_njm = self.data_segang_acc_njm.iloc[:,~self.data_segang_acc_njm.columns.str.contains('right')]
        elif seg_side == 'right':
            # remove columns with 'left'
            self.data_dig_njm = self.data_dig_interp.iloc[:,~self.data_dig_interp.columns.str.contains('left')]
            self.data_cm_njm = self.data_cm_njm.iloc[:,~self.data_cm_njm.columns.str.contains('left')]
            self.data_cm_acc_njm = self.data_cm_acc_njm.iloc[:,~self.data_cm_acc_njm.columns.str.contains('left')]
            self.data_i_njm = self.data_i_njm.iloc[:,~self.data_i_njm.columns.str.contains('left')]
            self.data_segang_acc_njm = self.data_segang_acc_njm.iloc[:,~self.data_segang_acc_njm.columns.str.contains('left')]
        else:
            self.data_dig_njm = self.data_dig_interp
    
    
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
    def main(self):
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        
        ### calculate segment angle, angular velocity, and angular acceleration
        dig2jk.segmentangle_vel_acc(self)
        
        ### calculate joint angle and angular velocity
        dig2jk.jointangle_vel(self)
        
        ### calculate segment moment of inertia
        data_i = momentinertia(self.data_seglength_interp, self.segments, self.mass)
        
        ### select data to be used in joint kinetics calculations
        dig2jk.selectdata(self)
        
        ### calculate joint kinetics
        data_njm = njm_full(self.data_dig_njm, self.data_cm_njm, self.data_cm_acc_njm, self.data_i_njm, self.data_segang_acc_njm, self.data_force, self.mass, self.seg_sequence, self.segments)
        
        
        return data_njm