# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:02:11 2020

@author: cwiens
"""

from Strobe.strobe import strobe, strobe_findframes

""" steps
* PLEASE READ the documentation for the above codes
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
i) modify the vidlist and other variables to match your project
ii) when selecting the frames to use as strobe, click 'q' to select frame and 'esc' when selecting FINAL frame
"""
    
""" set variables """
# creat list of videos (for more than one video: ['ChBr75_190728_LJ1_349.mp4', 'ChBr75_190728_LJ2_361.mp4'])
vidlist = ['ChBr75_190728_LJ1_349.mp4']
# do you want to crop the "search" area to only keep pixels within selected area?
crop = 'yes'
# if there are more than autoid_thresh number, it will auto select autoid_num number of frame(s) within that range
autoid_thresh = None
autoid_num = None
# sampling rate
samp = 240
# absolute difference threshold to find which pixels changed
thresh = 60
# number of frame difference from current image to use as subtraction image
bgint = 5


""" initialize variables """
frameALL = {}
searchALL = {}
i = 0

""" identify frames to use as strobe """
#%% loop through videos to find frames and search areas
for filename in vidlist:
    # find strobe frames
    frames, searcharea = strobe_findframes(filename, crop=crop, autoid_thresh=autoid_thresh, autoid_num=autoid_num)
    # add to list
    frameALL[i] = frames
    searchALL[i] = searcharea
    # iterate counter
    i += 1
    
""" create strobe video and/or image """
#%% loop through videos to create strobe
# reset counter
i = 0
for filename in vidlist:
    # load frame numbers and search area
    frames = frameALL[i]
    searcharea = searchALL[i]
    # create strobe
    filesave = filename[:-4] + '_strobe'
    strobe(filename, filesave, frames, searcharea, samp, thresh, bgint)
    # iterate counter
    i += 1