# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:10:02 2020

@author: cwiens
"""

import pandas as pd
import numpy as np
import cv2

#%%
def dlc_import(file, filetype='h5', thresh=0.8, file_vid=None, flipy='yes', madlc='no', startbuffer=5, edgebuffer=10):
    import os
    
    
    if filetype == 'h5':
        # if multi-animal DLC
        if madlc == 'yes':
            """ load data """
            data_in = pd.read_hdf(file)
            
            """ add the coordinate to the location name """
            colnames = []
            colnames_og = data_in.columns
            for cnt in range(len(colnames_og)):
                colnames.append(colnames_og[cnt][2] + '_' + colnames_og[cnt][3])

            """ convert into new data frame """
            # remove header rows and set column names
            data = pd.DataFrame(data_in.values, columns=colnames)

            # """ replace positions surrounded by nans """
            # for col in data.columns:
            #     for cntl in data.index[1:-1]:
            #         if np.isnan(data.loc[cntl - 1, col]) and np.isnan(data.loc[cntl + 1, col]):
            #             data.loc[cntl, col] = np.nan

            """ flip y-axis of digitized and center of mass data """
            if flipy == 'yes':
                # find height of image (max y value)
                cap = cv2.VideoCapture(file_vid)
                frame_width = int(cap.get(3))
                frame_height = int(cap.get(4))
                cap.release()
                # subtract digitzed loction from frame height (only y columns)
                data.iloc[:,data.columns.str.contains('_y')] = frame_height - data.filter(regex = '_y')
            
            """ subset digitized location and likelihood scores """
            # likelihood scores
            data_like = data.filter(regex = 'likelihood')
            # digitized data
            data_out = data.iloc[:,~data.columns.str.contains('likelihood', regex=False)]

            """ increase DLC's auto add likelihood - sets likelihood at 0.01 """
            def increase_like(y):
                y.loc[y == 0.01] = 0.95
                return y
            data_like = data_like.apply(lambda x: increase_like(x), axis=1)

            
            """ create frame column and join with digitized data """
            data_out = pd.DataFrame({'frame': range(0,len(data_out))}).join(data_out)
        
            """ estimate when body is in view based on image size and marker location """
            # find first frame where all markers are within frame
            frame_b = max(data.filter(regex='_x').apply(lambda x: x.between(0, frame_width)).idxmax().max(),
                          data.filter(regex='_y').apply(lambda x: x.between(0, frame_height)).idxmax().max())
            # find first instance ALL markers have likelihood above threshold for at least startbuffer frames
            for cntl in data_like.index[frame_b:]:
                if (data_like.loc[cntl:cntl+startbuffer+1,:] > thresh).all().all():
                    frame_first = cntl
                    break
                else:
                    frame_first = 0
            # fill nans with 0
            data_outNAN = data_out.copy().iloc[frame_first:, 1:].fillna(0)
            # find when object first exited the image for each marker
            if data_out.iloc[frame_first, 1] < frame_width/2:
                " object started on left side of image "
                frames_exc = data_outNAN.apply(lambda x: np.argmax(x > frame_width - edgebuffer))
            else:
                " object started on right side of image "
                frames_exc = data_outNAN.apply(lambda x: np.argmax((x < edgebuffer) & (x > 0)))
            # check if all are 0
            if (frames_exc == 0).all():
                frame_last = data_out.index[-1]
            else:
                # find when object first exited the image
                frame_exc = data_outNAN.index[min(frames_exc[frames_exc > 0]) -1]
                # find last frame in which all X AND Y locations exist (are not NAN)
                frame_last = (data_out.iloc[frame_exc:frame_first:-1, :].interpolate(method='linear', limit_direction='forward')>0).all(axis=1).idxmax()

        else:
            """ load data """
            data_in = pd.read_hdf(file)
            
            """ add the coordinate to the location name """
            colnames = []
            colnames_og = data_in.columns
            for cnt in range(len(colnames_og)):
                colnames.append(colnames_og[cnt][1] + '_' + colnames_og[cnt][2])
            
            """ convert into new data frame """
            # remove header rows and set column names
            data = pd.DataFrame(data_in.values, columns=colnames)
            
            """ flip y-axis of digitized and center of mass data """
            if flipy == 'yes':
                # find height of image (max y value)
                cap = cv2.VideoCapture(file_vid)
                frame_height = int(cap.get(4))
                cap.release()
                # subtract digitzed loction from frame height (only y columns)
                data.iloc[:,data.columns.str.contains('_y')] = frame_height - data.filter(regex = '_y')
            
            """ subset digitized location and likelihood scores """
            # likelihood scores
            data_like = data.filter(regex = 'likelihood')
            # digitized data
            data_out = data.iloc[:,~data.columns.str.contains('likelihood', regex=False)]
            
            """ create frame column and join with digitized data """
            data_out = pd.DataFrame({'frame': range(0,len(data_out))}).join(data_out)
        
            """ estimate when body is in view based on likelihood scores """
            # find first frame where all data is above threshold
            frame_first = np.max((data_like > thresh).idxmax())
            # find last frame where all data is above threshold (flipped data)
            frame_last = np.min((data_like.iloc[::-1] > thresh).idxmax())
    
    elif filetype == 'csv':
        """ load data """
        data_in = pd.read_csv(file, header=None)

        """ add the coordinate to the location name """
        for cnt in range(1,len(data_in.columns)):
            data_in.loc[3,cnt] = data_in.loc[2,cnt] + '_' + data_in.loc[3,cnt]

        """ convert into new data frame """
        # remove first three rows
        data = data_in.loc[4: ,:].reset_index(drop=True)
        # rename columns
        data.columns = data_in.iloc[3, :].to_list()
        data = data.rename(columns = {'coords': 'frame'})
        # convert full path name to just frame
        for cnt in range(0,len(data)):
            data['frame'][cnt] = float(os.path.basename(data['frame'][cnt])[3:-4])
        # convert data type to float
        data = data.astype('float')
        
        """ flip y-axis of digitized and center of mass data """
        if flipy == 'yes':
            # find height of image (max y value)
            cap = cv2.VideoCapture(file_vid)
            frame_height = int(cap.get(4))
            cap.release()
            # subtract digitzed loction from frame height (only y columns)
            data.iloc[:,data.columns.str.contains('_y')] = frame_height - data.filter(regex = '_y')
        
        """ subset digitized location and likelihood scores """
        # likelihood scores
        data_like = data.filter(regex = 'likelihood')
        # digitized data
        data_out = data.iloc[:,~data.columns.str.contains('likelihood', regex=False)]
    
        """ estimate when body is in view based on likelihood scores """
        # find first frame where all data is above threshold
        frame_first = np.max((data_like > thresh).idxmax())
        # find last frame where all data is above threshold (flipped data)
        frame_last = np.min((data_like.iloc[::-1] > thresh).idxmax())
        
    
    return data_out, frame_first, frame_last


#%%    
def intel_import(file):
    """
    Update the column names, make it 0-based, and set non-detected locations to nan

    :param file: csv file that comes from intel
    :return: dataframe modified to work with our codes
    """

    import numpy as np

    """ load data """
    df = pd.read_csv(file)
    
    """ convert name to have "left" and "right" """
    # rename "left" columns
    df.columns = df.columns.str.replace('l_', '_left_')
    # rename "right" columns
    df.columns = df.columns.str.replace('r_', '_right_')
    
    """ convert 0s to nan """
    df[df==0] = np.nan

    """ make frames 0-based """
    df.frame = df.frame - 1
    
    return df


#%%
def dltdv_import(file, file_vid=None, flipy='no'):
    """ load data """
    data_in = pd.read_csv(file)
    
    """ remove one frame (need to figure out why - 2020 Jun 23) """
    #data_out = data_in.iloc[2:,:].reset_index(drop=True)
    
    """ rename data_in columns """
    data_out = data_in.iloc[:,:40]
    data_out.columns = ["toe_right_x", "toe_right_y",
                        "heel_right_x", "heel_right_y",
                        "ankle_right_x", "ankle_right_y",
                        "knee_right_x", "knee_right_y",
                        "hip_right_x", "hip_right_y",
                        "toe_left_x", "toe_left_y",
                        "heel_left_x", "heel_left_y",
                        "ankle_left_x", "ankle_left_y",
                        "knee_left_x", "knee_left_y",
                        "hip_left_x", "hip_left_y",
                        "shoulder_right_x", "shoulder_right_y",
                        "elbow_right_x", "elbow_right_y",
                        "wrist_right_x", "wrist_right_y",
                        "finger_right_x", "finger_right_y",
                        "shoulder_left_x", "shoulder_left_y",
                        "elbow_left_x", "elbow_left_y",
                        "wrist_left_x", "wrist_left_y",
                        "finger_left_x", "finger_left_y",
                        "c7_x", "c7_y",
                        "vertex_x", "vertex_y"]
    
    """ create frame column and join with digitized data """
    data_out = pd.DataFrame({'frame': range(0,len(data_out))}).join(data_out)
    
    """ flip y-axis of digitized and center of mass data """
    if flipy == 'yes':
        # find height of image (max y value)
        cap = cv2.VideoCapture(file_vid)
        frame_height = int(cap.get(4))
        cap.release()
        # subtract digitzed loction from frame height (only y columns)
        data_out[data_out.columns[data_out.columns.str.contains('_y')]] = frame_height - data_out.filter(regex = '_y')
    
    """ estimate when body is in view based on likelihood scores """
    # find rows where all columns are nan
    temp = np.isnan(data_out).all(axis=1)
    # find first frame where all data is not all nan
    frame_first = temp.idxmin()
    # find last frame where all data is not nan
    frame_last = temp.iloc[temp.idxmin()+1:].idxmax()
    
    return data_out, frame_first, frame_last


def vama_import(file, flipy="yes", frame_height=1080):
    import json
    import pandas

    # read in json file
    with open(file, 'r') as f:
        df_json = json.load(f)
    # grab anatomical landmarks in pixel coordinate system
    df_digi_pix = df_json['processing']['views'][list(df_json['processing']['views'])[0]]['wireframes']
    # grab kinematics data
    df_digi_global = df_json['results']['kinematics']
    # grab frames
    frame_list = list(df_digi_pix.keys())
    data_digi_pix = pd.DataFrame(columns=["frame",
                                          "toe_right_x", "toe_right_y",
                                          "heel_right_x", "heel_right_y",
                                          "ankle_right_x", "ankle_right_y",
                                          "knee_right_x", "knee_right_y",
                                          "hip_right_x", "hip_right_y",
                                          "toe_left_x", "toe_left_y",
                                          "heel_left_x", "heel_left_y",
                                          "ankle_left_x", "ankle_left_y",
                                          "knee_left_x", "knee_left_y",
                                          "hip_left_x", "hip_left_y",
                                          "shoulder_right_x", "shoulder_right_y",
                                          "elbow_right_x", "elbow_right_y",
                                          "wrist_right_x", "wrist_right_y",
                                          "finger_right_x", "finger_right_y",
                                          "shoulder_left_x", "shoulder_left_y",
                                          "elbow_left_x", "elbow_left_y",
                                          "wrist_left_x", "wrist_left_y",
                                          "finger_left_x", "finger_left_y",
                                          "c7_x", "c7_y",
                                          "vertex_x", "vertex_y"])
    for cnti in frame_list:
        if len(list(df_digi_pix[cnti])) > 0:
            cur_dig = df_digi_pix[cnti][list(df_digi_pix[cnti])[0]]['dots']
            data_digi_pix = pd.concat([data_digi_pix,
                                       pd.DataFrame({'frame': [int(cnti)],
                                                     'toe_right_x': [cur_dig['toe_r']['x']],
                                                     'toe_right_y': [cur_dig['toe_r']['y']],
                                                     'heel_right_x': [cur_dig['heel_r']['x']],
                                                     'heel_right_y': [cur_dig['heel_r']['y']],
                                                     'ankle_right_x': [cur_dig['ankle_r']['x']],
                                                     'ankle_right_y': [cur_dig['ankle_r']['y']],
                                                     'knee_right_x': [cur_dig['knee_r']['x']],
                                                     'knee_right_y': [cur_dig['knee_r']['y']],
                                                     'hip_right_x': [cur_dig['hip_r']['x']],
                                                     'hip_right_y': [cur_dig['hip_r']['y']],
                                                     'toe_left_x': [cur_dig['toe_l']['x']],
                                                     'toe_left_y': [cur_dig['toe_l']['y']],
                                                     'heel_left_x': [cur_dig['heel_l']['x']],
                                                     'heel_left_y': [cur_dig['heel_l']['y']],
                                                     'ankle_left_x': [cur_dig['ankle_l']['x']],
                                                     'ankle_left_y': [cur_dig['ankle_l']['y']],
                                                     'knee_left_x': [cur_dig['knee_l']['x']],
                                                     'knee_left_y': [cur_dig['knee_l']['y']],
                                                     'hip_left_x': [cur_dig['hip_l']['x']],
                                                     'hip_left_y': [cur_dig['hip_l']['y']],
                                                     'shoulder_right_x': [cur_dig['shoulder_r']['x']],
                                                     'shoulder_right_y': [cur_dig['shoulder_r']['y']],
                                                     'elbow_right_x': [cur_dig['elbow_r']['x']],
                                                     'elbow_right_y': [cur_dig['elbow_r']['y']],
                                                     'wrist_right_x': [cur_dig['wrist_r']['x']],
                                                     'wrist_right_y': [cur_dig['wrist_r']['y']],
                                                     'finger_right_x': [cur_dig['hand_r']['x']],
                                                     'finger_right_y': [cur_dig['hand_r']['y']],
                                                     'shoulder_left_x': [cur_dig['shoulder_l']['x']],
                                                     'shoulder_left_y': [cur_dig['shoulder_l']['y']],
                                                     'elbow_left_x': [cur_dig['elbow_l']['x']],
                                                     'elbow_left_y': [cur_dig['elbow_l']['y']],
                                                     'wrist_left_x': [cur_dig['wrist_l']['x']],
                                                     'wrist_left_y': [cur_dig['wrist_l']['y']],
                                                     'finger_left_x': [cur_dig['hand_l']['x']],
                                                     'finger_left_y': [cur_dig['hand_l']['y']],
                                                     'c7_x': [cur_dig['neck']['x']],
                                                     'c7_y': [cur_dig['neck']['y']],
                                                     'vertex_x': [cur_dig['head']['x']],
                                                     'vertex_y': [cur_dig['head']['y']]})]).reset_index(drop=True)

    """ flip y-axis of digitized and center of mass data """
    if flipy == 'yes':
        # subtract digitzed loction from frame height (only y columns)
        data_digi_pix[data_digi_pix.columns[data_digi_pix.columns.str.contains('_y')]] = frame_height - data_digi_pix.filter(regex='_y')

    return data_digi_pix


#%% OLD VERSION - WILL BE REMOVED IN FUTURE
class convertdigi:
    
    def __init__(self, file, thresh=0.95, idfilt=None):
        """ give user notice that it will be removed in future """
        print("WARNING: This is using an old version. Please see dataconversion_digi.py's docs to see how to use updated version.")
        """ initialize variables """
        self.file = file
        self.thresh = thresh
        self.idfilt = idfilt
    
    
    def dlc_reformat(self, file_vid=None, flipy='yes'):
        """ load data """
        data_in = pd.read_csv(self.file, header=None)
        
        """ add the coordinate to the location name """
        for cnt in range(1,len(data_in.columns)):
            data_in.loc[2,cnt] = data_in.loc[1,cnt] + '_' + data_in.loc[2,cnt]
        
        """ convert into new data frame """
        # remove first three rows
        data = data_in.loc[3: ,:].reset_index(drop=True)
        # rename columns
        data.columns = data_in.iloc[2, :].to_list()
        data = data.rename(columns = {'coords': 'frame'})
        # convert data type to float
        data = data.astype('float')
        
        """ flip y-axis of digitized and center of mass data """
        if flipy == 'yes':
            # find height of image (max y value)
            cap = cv2.VideoCapture(file_vid)
            frame_height = int(cap.get(4))
            cap.release()
            # subtract digitzed loction from frame height (only y columns)
            data.iloc[:,data.columns.str.contains('_y')] = frame_height - data.filter(regex = '_y')
        
        """ subset digitized location and likelihood scores """
        # likelihood scores
        data_like = data.filter(regex = 'likelihood')
        # digitized data
        self.data_out = data.iloc[:,~data.columns.str.contains('likelihood', regex=False)]
        
        """ estimate when body is in view based on likelihood scores """
        # find first frame where all data is above threshold
        self.frame_first = np.max((data_like > self.thresh).idxmax())
        # find last frame where all data is above threshold (flipped data)
        self.frame_last = np.min((data_like.iloc[::-1] > self.thresh).idxmax())
        
        return self.data_out, self.frame_first, self.frame_last
    
    
#%%    
    def intel_reformat(self):
        """ load data """
        data_in = pd.read_csv(self.file)
        
        """ filter which person id in video """
        if not self.idfilt == None:
            data_in = data_in[data_in['id'] == self.idfilt]
        
        """ remove id and bounding box columns """
        self.data = data_in.drop(['id','bounding_box_corner_left','bounding_box_corner_right',
                                  'bounding_box_corner_top', 'bounding_box_corner_bottom'],
                                 axis = 1)
        
        """ convert path to frame number """
        # rename columns
        self.data = self.data.rename(columns = {'path': 'frame'})
        # rename frame to actual number
        self.data['frame'] = self.data['frame'].str[-7:-4]
        # convert data type to float
        self.data = self.data.astype('float').reset_index(drop=True)
        
        """ convert negative numbers to nan """
        self.data[self.data<0] = np.nan
        
        return self.data


#%%
    def dltdv_reformat(self, file_vid=None, flipy='no'):
        """ load data """
        data_in = pd.read_csv(self.file)
        
        """ remove one frame (need to figure out why - 2020 Jun 23) """
        data_out = data_in.iloc[1:,:].reset_index(drop=True)
        
        """ rename data_in columns """
        data_out = data_out.iloc[:,:40]
        data_out.columns = ["toe_right_x", "toe_right_y",
                            "heel_right_x", "heel_right_y",
                            "ankle_right_x", "ankle_right_y",
                            "knee_right_x", "knee_right_y",
                            "hip_right_x", "hip_right_y",
                            "toe_left_x", "toe_left_y",
                            "heel_left_x", "heel_left_y",
                            "ankle_left_x", "ankle_left_y",
                            "knee_left_x", "knee_left_y",
                            "hip_left_x", "hip_left_y",
                            "shoulder_right_x", "shoulder_right_y",
                            "elbow_right_x", "elbow_right_y",
                            "wrist_right_x", "wrist_right_y",
                            "finger_right_x", "finger_right_y",
                            "shoulder_left_x", "shoulder_left_y",
                            "elbow_left_x", "elbow_left_y",
                            "wrist_left_x", "wrist_left_y",
                            "finger_left_x", "finger_left_y",
                            "c7_x", "c7_y",
                            "vertex_x", "vertex_y"]
        
        """ create frame column and join with digitized data """
        self.data_out = pd.DataFrame({'frame': range(0,len(data_out))}).join(data_out)
        
        """ flip y-axis of digitized and center of mass data """
        if flipy == 'yes':
            # find height of image (max y value)
            cap = cv2.VideoCapture(file_vid)
            frame_height = int(cap.get(4))
            cap.release()
            # subtract digitzed loction from frame height (only y columns)
            self.data_out.iloc[:,self.data_out.columns.str.contains('_y')] = frame_height - self.data_out.filter(regex = '_y')
        
        """ estimate when body is in view based on likelihood scores """
        # find rows where all columns are nan
        temp = np.isnan(data_out).all(axis=1)
        # find first frame where all data is not all nan
        self.frame_first = temp.idxmin()
        # find last frame where all data is not nan
        self.frame_last = temp.iloc[temp.idxmin()+1:].idxmax()
        
        return self.data_out, self.frame_first, self.frame_last


"""
remove_switches
    Removes potential marker switches

Input:
    data_in: DATAFRAME data to be checked for possible switching
        FIRST COLUMN SHOULD BE FRAME/TIME
        Must contain left and right sets
    thresh: FLOAT threshold to check if markers are within set distance (default: 0.1) [m]
    factor: INT factor to multiply the 25% trimmed mean of the marker acceleration for thresholding (default: 8)
        (i.e., trim_mean(acceleration, 0.25) * 8)
    pix2m: FLOAT pixel to meter ratio, if given it will multiply the dataset to convert to meters (default: None)

Output:
    df: DATAFRAME data with any marker's within threshold removed
        units are the same are original dataframe (data_in)

Dependencies:
    numpy
"""
def remove_switches(data_in, factor=10, pix2m=None):
    import numpy as np
    from scipy.stats import trim_mean

    df = data_in.copy()

    " set in meters to keep constant comparison "
    if pix2m is not None:
        df.iloc[:, 1:] = df.iloc[:, 1:] * pix2m


    " loop through markers "
    for mar in pd.Index(map(lambda x : str(x)[:-2], df.columns[1:])).unique():

        df_c = df.filter(regex=mar).copy().interpolate(method='linear', limit_direction='both')

        acc_loc = pd.Index([])
        stopper = 0

        while stopper == 0:
            """ find indices when markers have acceleration greater than sdfactor times the standard deviation """
            acc_loc_t = df_c.index[np.where((abs(df_c[mar + '_x'].diff().diff()) > (trim_mean(abs(df_c[mar + '_x'].diff().diff()), 0.25) * factor)) |
                                            (abs(df_c[mar + '_y'].diff().diff()) > (trim_mean(abs(df_c[mar + '_y'].diff().diff()), 0.25) * factor)))]

            # append new indices
            #acc_loc = acc_loc.append(acc_loc_r).append(acc_loc_l)

            if len(acc_loc_t) > 0:
                if np.isin(acc_loc_t, acc_loc).all():
                    df.loc[acc_loc, mar + '_x'] = np.nan
                    df.loc[acc_loc, mar + '_y'] = np.nan
                    stopper = 1
                else:
                    # set appendices to nan
                    df_c.loc[acc_loc_t, mar + '_x'] = np.nan
                    df_c.loc[acc_loc_t, mar + '_y'] = np.nan
                    df_c = df_c.interpolate(method='linear', limit_direction='both')
                    acc_loc = acc_loc.append(acc_loc_t)
            else:
                df.loc[acc_loc, mar + '_x'] = np.nan
                df.loc[acc_loc, mar + '_y'] = np.nan
                stopper = 1



        # """ loop through number of "overlapping" occurances """
        # for cnts in df.index[np.where((abs(df[mar + '_left_x'] - df[mar + '_right_x']) < thresh) &
        #                               (abs(df[mar + '_left_y'] - df[mar + '_right_y']) < thresh))]:
        #     """ if the acceleration index is within one frame of the overlapping
        #         this makes it so there has to be a large acceleration that occured near by AND the markers are near
        #     """
        #     if len(acc_loc_l) > 1 and (abs(acc_loc_l - cnts) <= 1).any():
        #         df.loc[acc_loc_r[abs(acc_loc_r - cnts) <= 1], mar + '_left_x'] = np.nan
        #         df.loc[acc_loc_r[abs(acc_loc_r - cnts) <= 1], mar + '_left_y'] = np.nan
        #     if len(acc_loc_r) > 1 and (abs(acc_loc_r - cnts) <= 1).any():
        #         df.loc[acc_loc_r[abs(acc_loc_r - cnts) <= 1], mar + '_right_x'] = np.nan
        #         df.loc[acc_loc_r[abs(acc_loc_r - cnts) <= 1], mar + '_right_y'] = np.nan

    """ remove last frames skip if present """
    # for col in range(1, len(df.columns)):
    #     # fill any possible nans and find difference
    #     tempdiff = np.diff((df.iloc[:,col]).interpolate(method='spline', order=3))
    #     # find std of difference
    #     sdthresh = np.std(tempdiff) * sdfactor
    #     with np.errstate(invalid='ignore'):
    #         if abs(tempdiff[-1]) > sdthresh:
    #             # add previous change in location to previous point (estimating where it would be)
    #             df.iloc[len(df)-1, col] = df.iloc[-2, col] + tempdiff[-2]

    " reset to pixels if it was originally "
    if pix2m is not None:
        df.iloc[:, 1:] = df.iloc[:, 1:].copy() / pix2m

    return df