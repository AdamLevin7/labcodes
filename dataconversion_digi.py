# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:10:02 2020

@author: cwiens
"""

import pandas as pd
import numpy as np
import cv2

class convertdigi:
    
    def __init__(self, file, thresh=0.95, idfilt=None):
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
