#TODO should packages go within the functions individually or the class overall?
"""
Script: dig2jointkinetics
    Modules to go from digitized data to joint kinetics calculations..

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

Author:
    Casey Wiens
    cwiens32@gmail.com
"""

"""
  
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
    
"""

from scipy import signal
from scipy.interpolate import splev, splrep
import pandas as pd
import numpy as np
from kinematics.calc_segmentlength import seglength
from derivative import centraldiff
from kinematics.calc_segmentangle import segangle
from kinematics.calc_jointangle import jointangle
from kinematics.calc_segmentmomentinertia import momentinertia
from NJM.jointkinetics import njm_full
from FindContactIntervals import FindContactIntervals
from findplate import findplate
from pixelratios import pix2m_fromplate, bw2pix
from dataconversion_force import convertdata
import cv2
from CalcCOM.segdim_deleva import segmentdim


class dig2jk:
    
    def __init__(self, data_dig, data_cm, data_force, segments, xvals,
                 contact_seg=None, mass=None, samp_dig=240, samp_force=1200):
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


    def datainterp(self):
        """
        Function::: datainterp
        	Description: filter and interpolates CM and digitized data to match force data
        	Details:

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

        Dependencies
            scipy
            pandas
        """

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
        self.data_dig_filt = pd.DataFrame({'time': self.data_dig.iloc[:,0]}).join(self.data_dig.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # center of mass data
        self.data_cm_filt = pd.DataFrame({'time': self.data_cm.iloc[:,0]}).join(self.data_cm.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # segment length
        self.data_seglength_filt = pd.DataFrame({'time': data_seglength.iloc[:,0]}).join(data_seglength.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        
        ### interpolate kinematic data
        # digitized data
        self.data_dig_interp = pd.DataFrame({'time': self.xvals}).join(self.data_dig_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(self.data_dig_filt['time'], y))).set_index(self.xvals.index))
        # center of mass data
        self.data_cm_interp = pd.DataFrame({'time': self.xvals}).join(self.data_cm_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(self.data_cm_filt['time'], y))).set_index(self.xvals.index))
        # segment length data
        self.data_seglength_interp = pd.DataFrame({'time': self.xvals}).join(self.data_seglength_filt.iloc[:,1:].apply(lambda y: splev(self.xvals, splrep(self.data_seglength_filt['time'], y))).set_index(self.xvals.index))
    

    def cm_angularimpulse(self):
        """
        Function::: cm_angularimpulse
        	Description: calculate angular impulse about body center of mass
        	Details:

        Inputs
            data_force: DATAFRAME force data (fx, fy, ax, ay) (N, N, m, m)
            data_cm: DATAFRAME center of mass data for segments and body (m).
                Dataframe obtained from calc_centermass.py
                Data should be same length as force data.

        Outputs
            cm_moment: ARRAY moment about center of mass (N*m)
            cm_theta: ARRAY angle between center of mass and reaction force (rad)

        Dependencies
            pandas
            numpy
        """
        ### filter and interpoloate data
        dig2jk.datainterp(self)
        
        ### calculate angular impulse about body center of mass
        # create vector from center of mass to center of pressure
        cm_r = pd.DataFrame({'x': self.data_force['ax'].values - self.data_cm_interp['body_x'].values,
                             'y': self.data_force['ay'].values - self.data_cm_interp['body_y'].values})
        # calculate moment about center of mass
        self.cm_moment = np.cross(cm_r, self.data_force[['fx','fy']])
        # calculate angular impulse
        self.ang_imp = sum(self.cm_moment) / self.samp_force
        # calculate center of mass theta (FROM RIGHT HORIZONTAL)
        self.cm_theta = np.arctan2(-cm_r['y'], -cm_r['x'])
        # calculate reaction force theta (FROM RIGHT HORIZONTAL)
        self.rf_theta = np.arctan2(self.data_force['fy'].reset_index(drop=True),
                                   self.data_force['fx'].reset_index(drop=True))
        
        
        return self.ang_imp, self.cm_moment, self.cm_theta, self.rf_theta
    


    def cm_velocityacceleration(self):
        """
        Function::: cm_velocityacceleration
        	Description: calculate center of mass velocity and acceleration
        	Details:

        Inputs
            data_cm: DATAFRAME center of mass data for segments and body (m).
                Dataframe obtained from calc_centermass.py
                Data should be same length as force data.
            xvals: 1-D FLOATS x-coordinates for new data series
            samp: INT sampling rate of signal

        Outputs
            data_cm_vel_filt: DATAFRAME filtered center of mass velocity data for segments and body (m/s)
            data_cm_acc_filt: DATAFRAME filtered center of mass acceleration data for segments and body (m/s^2)

        Dependencies
            dig2jk
            scipy
            pandas
        """

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
        # filter center of mass velocities
        self.data_cm_vel_filt = pd.DataFrame({'time': self.xvals}).join(data_cm_vel.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
        # center of mass accelerations
        data_cm_acc = centraldiff(self.data_cm_vel_filt, (1/self.samp_force))
        # filter center of mass accelerations
        self.data_cm_acc_filt = pd.DataFrame({'time': self.xvals}).join(data_cm_acc.iloc[:, 1:].apply(lambda x: x.interpolate(method='spline', order=3).fillna(method='bfill')).apply(lambda x: signal.filtfilt(b, a, x)))
    

    def segmentangle_vel_acc(self):
        """
        Function::: segmentangle_vel_acc
        	Description: calculate segment angle, angular velocity, and angular acceleration
        	Details:

        Inputs
            data_dig: DATAFRAME digitized data (m)
            xvals: 1-D FLOATS x-coordinates for new data series
            segments: DATAFRAME segment parameters obtained from segdim_deleva.py

        Outputs
            data_segang: DATAFRAME segment angle data (rad)
            data_segang_vel: DATAFRAME segment angular velocity data (rad/s)
            data_segang_acc: DATAFRAME segment angular acceleration data (rad/s^2)

        Dependencies
            dig2jk
            segangle
            centraldiff
            numpy
        """

        ### filter and interpoloate data
        dig2jk.datainterp(self)
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        
        ### calculate segmental angles
        self.data_segang = segangle(self.data_dig_interp, self.segments, allpositive='no')
        
        ### calculate segmental angular velocities
        # segmental angular velocities
        self.data_segang_vel = centraldiff(self.data_segang, np.mean(np.diff(self.data_segang['time'])))
        
        ### calculate segmental angular accelerations
        # segmental angular velocities
        self.data_segang_acc = centraldiff(self.data_segang_vel, np.mean(np.diff(self.data_segang_vel['time'])))


    def jointangle_vel(self):
        """
        Function::: jointangle_vel
        	Description: calculate joint angle and angular velocity
        	Details:

        Inputs
            data_dig: DATAFRAME digitized data (m)
            xvals: 1-D FLOATS x-coordinates for new data series
            segments: DATAFRAME segment parameters obtained from segdim_deleva.py

        Outputs
            data_jointang: DATAFRAME joint angle data (rad)
            data_jointang_vel: DATAFRAME joint angular velocity data (rad/s)

        Dependencies
            dig2jk
            numpy
            centraldiff
        """

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
        """
        Function::: name_of_function
        	Description: brief description here (1 line)
        	Details: Full description with details here

        Inputs
            input1: DATATYPE description goes here (units)
            input2: DATATYPE description goes here (units)
            input3: DATATYPE description goes here (units)
            input4: DATATYPE description goes here (units)

        Outputs
            output1: DATATYPE description goes here (units)
            output2: DATATYPE description goes here (units)
            output3: DATATYPE description goes here (units)
            output4: DATATYPE description goes here (units)

        Dependencies
            dep1
            dep2
            dep3 from uscbrl_script.py (USCBRL repo)
        """

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
        """
        Function::: name_of_function
        	Description: brief description here (1 line)
        	Details: Full description with details here

        Inputs
            input1: DATATYPE description goes here (units)
            input2: DATATYPE description goes here (units)
            input3: DATATYPE description goes here (units)
            input4: DATATYPE description goes here (units)

        Outputs
            output1: DATATYPE description goes here (units)
            output2: DATATYPE description goes here (units)
            output3: DATATYPE description goes here (units)
            output4: DATATYPE description goes here (units)

        Dependencies
            dep1
            dep2
            dep3 from uscbrl_script.py (USCBRL repo)
        """

        ### filter and interpoloate data
        dig2jk.datainterp(self)
        print('Completed datainterp')
        
        ### calculate center of mass velocity and acceleration
        dig2jk.cm_velocityacceleration(self)
        print('Completed cm_velocityacceleration')
        
        ### calculate segment angle, angular velocity, and angular acceleration
        dig2jk.segmentangle_vel_acc(self)
        print('Completed segmentangle_vel_acc')
        
        ### calculate joint angle and angular velocity
        dig2jk.jointangle_vel(self)
        print('Completed jointangle_vel')
        
        ### calculate segment moment of inertia
        data_i = momentinertia(self.data_seglength_interp, self.segments, self.mass)
        print('Completed momentinertia')
        
        ### select data to be used in joint kinetics calculations
        dig2jk.selectdata(self)
        print('Completed selectdata')
        
        ### calculate joint kinetics
        data_njm = njm_full(self.data_dig_njm, self.data_cm_njm, self.data_cm_acc_njm, self.data_i_njm, self.data_segang_acc_njm, self.data_force, self.mass, self.seg_sequence, self.segments)
        print('Completed njm_full')
        
        
        return data_njm


#%%
class dig2jk_format:

    def __init__(self, data_digi, data_cm, data_force, bw, sex,
                 con_plate, con_frame, flip, file_vid=None):
        # initialize variables
        self.data_digi = data_digi
        self.data_cm = data_cm
        self.data_force = data_force
        self.bw = bw
        self.sex = sex
        self.con_plate = con_plate
        self.con_frame = con_frame
        self.flip = flip
        self.file_vid = file_vid
        
        
    def data_reformat(self, view="fy", mode="combined", flipy_digi='no',
                      con_num=0, zero_thresh=16, plate_area=None, ci_thresh=16,
                      plate_dim=(0.6, 0.4), bwpermeter=2, samp_vid=240, samp_force=1200):
        """
        Function::: name_of_function
        	Description: brief description here (1 line)
        	Details: Full description with details here

        Inputs
            input1: DATATYPE description goes here (units)
            input2: DATATYPE description goes here (units)
            input3: DATATYPE description goes here (units)
            input4: DATATYPE description goes here (units)

        Outputs
            output1: DATATYPE description goes here (units)
            output2: DATATYPE description goes here (units)
            output3: DATATYPE description goes here (units)
            output4: DATATYPE description goes here (units)

        Dependencies
            dep1
            dep2
            dep3 from uscbrl_script.py (USCBRL repo)
        """


        """ find contact interval for force and digitized data """
        con_plate_fz = [s + '_Fz' for s in self.con_plate]
        # contact interval for force data
        ci_force = FindContactIntervals(self.data_force[con_plate_fz].sum(axis=1), samp_force, thresh=ci_thresh)
        # find contact duration in digitized data
        frame_finalcont = self.con_frame + int((ci_force['End'][con_num] - ci_force['Start'][con_num]) / (samp_force / samp_vid)) + 1
        # set contact interval for digitized data
        ci_digi = pd.DataFrame({'Start': [np.where(self.data_digi['frame'] == self.con_frame)[0][0]],
                                'End': [np.where(self.data_digi['frame'] == frame_finalcont)[0][0]]})
        
        
        """ crop data """
        ### force data
        # find time for cropped section
        t = self.data_force.iloc[ci_force['Start'][con_num]:ci_force['End'][con_num]].filter(regex = 'Time')
        # crop force data
        # loop through plates
        data_force_crop = {}
        for cntp in range(len(self.con_plate)):
            data_force_crop[cntp] = t.join(self.data_force.iloc[ci_force['Start'][con_num]:ci_force['End'][con_num]].filter(regex = self.con_plate[cntp]+'.*'))
        
        
        ### digitized data
        # crop digitized data
        # plus one to match force data length - need to double check why
        data_digi_crop = self.data_digi.iloc[ci_digi['Start'][0]:ci_digi['End'][0]+1]
        data_cm_crop = self.data_cm.iloc[ci_digi['Start'][0]:ci_digi['End'][0]+1]
        
        
        """ truly zero force plates """
        # set values below 16 to 0
        for cntfp in range(len(data_force_crop)):
            for cntf in range(len(data_force_crop[0])):
                if (data_force_crop[cntfp].iloc[cntf,3] < zero_thresh):
                    data_force_crop[cntfp].iloc[cntf,1:] = 0
        
        
        """ find plates """
        if plate_area == None:
            # identify force plate location in image
            plate_area = findplate(self.file_vid, label="Select all plates in order in force file")
        # save to object
        self.plate_area = plate_area
        
        
        """ calculate pix2m and mag2pix """
        self.pix2m = pix2m_fromplate(self.plate_area, plate_dim)
        self.mag2pix = bw2pix(self.pix2m['x'], self.bw, bwpermeter=bwpermeter)
        
        
        """ convert force data to video reference system """
        # create object
        transform_data = convertdata(data_force_crop, self.mag2pix, self.pix2m, view=view, mode=mode,
                                     platelocs=self.plate_area, flip=self.flip)
        # run function to convert to meters in video reference system
        transform_data.data2meter(file_vid=self.file_vid)
        # [0] is selecting the first contact interval
        self.data_force_vidref_m = transform_data.data_fp[0]
        
        
        """ flip y-axis of digitized and center of mass data """
        if flipy_digi == 'yes':
            # find height of image (max y value)
            cap = cv2.VideoCapture(self.file_vid)
            frame_height = int(cap.get(4))
            cap.release()
            # subtract digitzed loction from frame height (only y columns)
            data_digi_crop.iloc[:,data_digi_crop.columns.str.contains('_y')] = frame_height - data_digi_crop.filter(regex = '_y')
            # subtract center of mass location from frame height (only y columns)
            data_cm_crop.iloc[:,data_cm_crop.columns.str.contains('_y')] = frame_height - data_cm_crop.filter(regex = '_y')
        
        
        """ convert to meters """
        # convert digitized data to meters
        self.data_digi_crop_m = pd.DataFrame(data_digi_crop.iloc[:,0]).join(data_digi_crop.iloc[:,1:] * self.pix2m['x'])
        # convert center of mass data to meters
        self.data_cm_crop_m = pd.DataFrame(data_cm_crop.iloc[:,0]).join(data_cm_crop.iloc[:,1:] * self.pix2m['x'])
        
        
        """ format data """
        # create time series (reset to start at 0)
        t = data_force_crop[0]['Time'] - data_force_crop[0]['Time'].iloc[0]
        # convert frame to time
        self.data_digi_crop_m['frame'] = self.data_digi_crop_m['frame'] / samp_vid
        self.data_cm_crop_m['frame'] = self.data_cm_crop_m['frame'] / samp_vid
        # rename frame column
        self.data_digi_crop_m = self.data_digi_crop_m.rename(columns={'frame': 'time'})
        self.data_cm_crop_m = self.data_cm_crop_m.rename(columns={'frame': 'time'})
        # reset time series (reset to start at 0)
        self.data_digi_crop_m['time'] = self.data_digi_crop_m['time'] - self.data_digi_crop_m['time'].iloc[0]
        self.data_cm_crop_m['time'] = self.data_cm_crop_m['time'] - self.data_cm_crop_m['time'].iloc[0]
        
        
        """ create object """
        # find segment parameters
        segments = segmentdim(self.sex)
        # create object
        jk_obj = dig2jk(self.data_digi_crop_m, self.data_cm_crop_m, self.data_force_vidref_m,
                        segments, t, mass=self.bw/9.81, samp_dig=samp_vid, samp_force=samp_force)

        return jk_obj