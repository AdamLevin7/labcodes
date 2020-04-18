# -*- coding: utf-8 -*-
"""
displayskeleton
    Add visual representation of segments and center of mass of body and segments.
    
Inputs
    file_vid: STR full file name of video
    data: DATAFRAME digitized data for each segment
        Row 0: frame
        Row 1+: digitized locations with x then y
    data_cm: DATAFRAME body and segment CM locations (prefe)
        Row 0: frame
        Row 1+: center of mass locations with x then y
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    image of each digitized frame with body cm, segment cm, and segment visually represented
        loaction: 'SkeletonOL' folder within location of file_vid
    
Dependencies
    cv2 (opencv)
    pandas
    numpy
    
Created on Fri Apr 17 15:27:11 2020

@author: cwiens
"""

import cv2
import pandas as pd
import numpy as np
import os


def addskeleton(file_vid, data, data_cm, segments):
    
    #%% set up location to store images
    # if just file name was given
    if os.path.dirname(file_vid) == '':
        savefolder = 'SkeletonOL'
    else:
        savefolder = os.path.join(os.path.dirname(file_vid), 'SkeletonOL')
    # if folder does not exist
    if not os.path.exists(savefolder):
        os.makedirs(savefolder)
                
    
    #%% load video file
    cap = cv2.VideoCapture(file_vid)
    
    #%% apply skeleton on each image
    # loop through frames
    for cnt in range(len(data)):
        # frame number 
        framenum = int(data['frame'].iloc[cnt])
        # set current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, framenum)
        # read current frame
        ret, frame = cap.read()
        
        #%% loop through digitized points
        for cnts in range(len(segments)):
            # if segment doesn't contain nans
            if (any(np.isnan(data.filter(regex = segments['origin'][cnts]).loc[cnt,:])) or
                any(np.isnan(data.filter(regex = segments['other'][cnts]).loc[cnt,:]))):
                pass
            else:
                # if it is head
                if (segments.iloc[cnts,:]).name == 'head':
                    # origin
                    orig_loc = tuple(data.filter(regex = segments['origin'][cnts]).loc[cnt,:].astype(int))
                    # other
                    oth_loc = tuple(data.filter(regex = segments['other'][cnts]).loc[cnt,:].astype(int))
                    # draw segment with red line
                    frame = cv2.line(frame, orig_loc, oth_loc, (0,0,255), thickness=3)
                    # segment center of mass
                    segcm = data_cm.filter(regex = (segments.iloc[cnts,:]).name)
                    # display segment center of mass location
                    segcm_loc = tuple(segcm.loc[cnt,:].astype(int))
                    frame = cv2.circle(frame, segcm_loc, 3, (0,0,0), -1)
                    
                # if it is trunk
                elif (segments.iloc[cnts,:]).name == 'trunk':
                    # origin
                    orig_loc = tuple(data.filter(regex = segments['origin'][cnts]).loc[cnt,:].astype(int))
                    # other
                    oth = data.filter(regex = segments['other'][cnts])
                    # if both hips were located, use average
                    if len(oth.columns) > 2:
                        oth = pd.DataFrame({'x': oth.filter(regex='x').mean(axis = 1),
                                            'y': oth.filter(regex='y').mean(axis = 1)})
                    # create tuple for other
                    oth_loc = tuple(oth.loc[cnt,:].astype(int))
                    # draw segment with red line
                    frame = cv2.line(frame, orig_loc, oth_loc, (0,0,255), thickness=3)
                    # segment center of mass
                    segcm = data_cm.filter(regex = (segments.iloc[cnts,:]).name)
                    # display segment center of mass location
                    segcm_loc = tuple(segcm.loc[cnt,:].astype(int))
                    frame = cv2.circle(frame, segcm_loc, 3, (0,0,0), -1)
            
                # if another segment
                else:
                    # origin
                    orig = data.filter(regex = segments['origin'][cnts])
                    # segment center of mass
                    segcm = data_cm.filter(regex = (segments.iloc[cnts,:]).name)
                    # find if location exists in digitized data set
                    if len(orig.columns) > 0:
                        # find if left and right segments were specified
                        orig_l = orig.filter(regex = 'left')
                        orig_r = orig.filter(regex = 'right')
                        # find left and right segments
                        segcm_l = tuple(segcm.filter(regex = 'left').loc[cnt,:].astype(int))
                        segcm_r = tuple(segcm.filter(regex = 'right').loc[cnt,:].astype(int))
                    # other
                    oth = data.filter(regex = segments['other'][cnts])
                    # find if location exists in digitized data set
                    if len(oth.columns) > 0:
                        # find if left and right segments were specified
                        oth_l = oth.filter(regex = 'left')
                        oth_r = oth.filter(regex = 'right')
                        
                    # if both origin and other locations exist
                    if (len(orig.columns)>0 and len(oth.columns)>0):
                        # if left segment exists
                        if (len(orig_l.columns)>0 or len(oth_l.columns)>0):
                            # create tuple
                            orig_loc = tuple(orig_l.loc[cnt,:].astype(int))
                            oth_loc = tuple(oth_l.loc[cnt,:].astype(int))
                            # draw segment with red line
                            frame = cv2.line(frame, orig_loc, oth_loc, (0,0,255), thickness=3)
                            # display segment center of mass location
                            frame = cv2.circle(frame, segcm_l, 3, (0,0,0), -1)
                        # if right segment exists
                        if (len(orig_r.columns)>0 or len(oth_r.columns)>0):
                            # create tuple
                            orig_loc = tuple(orig_r.loc[cnt,:].astype(int))
                            oth_loc = tuple(oth_r.loc[cnt,:].astype(int))
                            # draw segment with red line
                            frame = cv2.line(frame, orig_loc, oth_loc, (0,0,255), thickness=3)
                            # display segment center of mass location
                            frame = cv2.circle(frame, segcm_r, 3, (0,0,0), -1)
                        # if neither left or right exists
                        if (len(orig_l.columns)==0) and (len(orig_r.columns)==0):
                            # create tuple
                            orig_loc = tuple(orig.loc[cnt,:].astype(int))
                            oth_loc = tuple(orig.loc[cnt,:].astype(int))
                            # draw segment with red line
                            frame = cv2.line(frame, orig_loc, oth_loc, (0,0,255), thickness=3)
                            # display segment center of mass location
                            segcm_loc = tuple(segcm.loc[cnt,:].astype(int))
                            frame = cv2.circle(frame, segcm_loc, 3, (0,0,0), -1)
                
                
        #%% display center of mass
        # if center of mass is not nan (from missing segment)
        if not any(np.isnan(data_cm[['body_x','body_y']].loc[cnt])):
            # create tuple
            bodycm_loc = tuple(data_cm.filter(regex = 'body').loc[cnt,:].astype(int))
            # display center of mass location
            frame = cv2.circle(frame, bodycm_loc, 8, (0,255,255), -1)
        
        
        #%% save frame
        # create frame name
        framename = os.path.join(savefolder,
                                 os.path.basename(file_vid)[ :-4] + '_' + str(framenum) + '.png')
        cv2.imwrite(framename, frame)
        
        
    #%% when everything done, release the video capture and video write objects
    cap.release()
    # closes all the frames
    cv2.destroyAllWindows()
