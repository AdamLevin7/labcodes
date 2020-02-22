# -*- coding: utf-8 -*-
"""
strobe_findframes

Allows user to identify which frames to use for strobe creation.
This uses the function 'findframe'.
    - user can advance using the trackbar but must click button after to update
    - 'k' = -100 frames
    - 'm' = -10 frames
    - ',' = -1 frame
    - '.' = +1 frame
    - '/' = +10 frames
    - ';' = +100 frames
    - click 'q' to select frame when identified in GUI
    - click 'esc' to exit out of GUI
    
User input:
    - filename: full path file name
    - crop: if 'yes' (default), user will identify area around the object of
        interest that could be used to limit noise in strobe image

Created on Thu Feb 6 10:36:26 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

from findframe import findframe
import pandas as pd
from capture_area import findarea

def strobe_findframes(filename, crop='yes'):
    #%% initialize variables
    strobeframes = None
    frame = 0
    key = 0
    
    #%% while user has not pressed escape
    while key != 27:
        #%% if first strobe image
        # update frame and strobe frame list
        if strobeframes is None:
            frame, key = findframe(filename,
                                   label='Strobe Frames: ',
                                   framestart=frame)
            strobeframes = pd.Series(frame)
            #%% if crop was chosen
            if crop == 'yes':
                # find search area
                area = findarea(filename,frame=frame,label='Select area around object')
                searcharea = {frame: area}
        #%% if it is not first strobe image
        else:
            frame, key = findframe(filename,
                                   label='Strobe Frames: ' + ",".join("{0}".format(n) for n in strobeframes),
                                   framestart=frame)
            strobeframes = strobeframes.append(pd.Series(frame)).reset_index(drop=True)
            #%% if crop was chosen
            if crop == 'yes':
                # find search area
                area = findarea(filename,frame=frame,label='Select area around object')
                searcharea[frame] = area
            
    #%% drop duplicates
    strobeframes = strobeframes.drop_duplicates()
    
    return strobeframes, searcharea