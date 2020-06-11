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
    - autoid: OPTIONAL default: None, minimum number of frames between manually 
        identified strobe frames before auto id occurs (will find apex and two
        additional frames before and after apex)

Created on Thu Feb 6 10:36:26 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

from findframe import findframe
import pandas as pd
from capture_area import findarea
import numpy as np

def strobe_findframes(filename, crop='yes', autoid=None):
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
    
    #%% if auto-find frames was selected
    if autoid is not None:
        # store strobeframes as another variable to use as search
        sframestemp = strobeframes
        # find difference between selected frames
        diffframes = np.diff(strobeframes)
        # auto select evenly spaced frames
        for cntdf in range(len(diffframes)):
            if diffframes[cntdf] >= autoid:
                frames = np.linspace(sframestemp.iloc[cntdf],
                                     sframestemp.iloc[cntdf+1], 7, dtype=int)
                strobeframes = (strobeframes.append(pd.Series(frames)).reset_index(drop=True)).sort_values(ignore_index=True).drop_duplicates()
                # if crop was selected, crop area for each new frame
                if crop == 'yes':
                    for cntf in frames[1:-1]:
                        area = findarea(filename,frame=cntf,label='Select area around object')
                        searcharea[cntf] = area
    
    #%%
    return strobeframes, searcharea