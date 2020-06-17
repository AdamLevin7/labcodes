# -*- coding: utf-8 -*-
"""
Vector Overlay
    Add a vector to the video to represent the ground reaction force.

Inputs 
    file: STRING file name of video
    file_out: STRING file name for new video
    data_vid: DICT force and cop data, prefer that output from data2pix.
        format (0: {fx, fy, ax, ay},
                1: {fx, fy, ax, ay},
                ...)
    frame_con: LIST contact frame of video
        format [INT, INT, ...]
    samp_video: INT sampling rate of video
    samp_force: INT sampling rate of force
    dispthresh: INT display threshold, amount of force needed to display
        vector (unit=Newtons, default=60)

Created on Thu Jan  2 16:14:15 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import cv2
import numpy as np

def vectoroverlay(file, file_out, data_vid, frame_con,
                  samp_force=1200, samp_video=240, dispthresh=60):
    
    #%% reformat frame_con if not list
    if not isinstance(frame_con, list):
        frame_con = [frame_con]
    
    #%% initialize video
    cap = cv2.VideoCapture(file)
    # default resolutions of the frame are obtained. The default resolutions are system dependent.
    # we convert the resolutions from float to integer.
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # define the codec and create VideoWriter object
    out = cv2.VideoWriter(file_out, cv2.VideoWriter_fourcc('M','P','4','V'),
                          samp_video/4, (frame_width,frame_height))
    
    #%% initialize variables
    # first video frame number
    framenumV = 0
    # initialize variables
    framenumF = {}
    frameendF = {}
    # loop through plates
    for cntp in range(len(data_vid)):
        # find first force frame number
        framenumF[cntp] = (data_vid[cntp]['ax'] != 0).idxmax()
        # find last force frame number
        frameendF[cntp] = int(framenumF[cntp] + len(data_vid[cntp]['ax']) - 1)
    # find sampling rate factor
    samp_fact = samp_force/samp_video
    
    #%% create video
    while(True):
        ret, frame = cap.read()
        if ret == True:
            # loop through force plates
            for cntp in range(len(data_vid)):
                # if frame number is greater than contact frame..
                if (framenumV >= frame_con[cntp]) and (framenumF[cntp] <= frameendF[cntp] - samp_fact):
                    for i in range(int(samp_fact)):
                        if framenumF[cntp] <= frameendF[cntp]:
                            # if resultant force is above display threshold
                            if np.sqrt(np.sum(np.square(data_vid[cntp][['fx','fy']]),axis=1)).loc[framenumF[cntp]] >= dispthresh:
                                # start coordinate
                                start_point = (int(data_vid[cntp]['ax'][framenumF[cntp]]),
                                               int(data_vid[cntp]['ay'][framenumF[cntp]]))
                                # end coordinate
                                end_point = (int(data_vid[cntp]['ax'][framenumF[cntp]]+data_vid[cntp]['fx'][framenumF[cntp]]),
                                             int(data_vid[cntp]['ay'][framenumF[cntp]]+data_vid[cntp]['fy'][framenumF[cntp]]))
                                # set parameters
                                color = (0, int(255*((i+1)/samp_fact)), 0)
                                thickness = 2
                                tipLength = 1
                                # draw a arrowed line
                                cv2.arrowedLine(frame, start_point, end_point, color, thickness, tipLength)
                            # iterate counter
                            framenumF[cntp] += 1
            # Displaying the image
            cv2.imshow('frame', frame)
            # write the frame into the file
            out.write(frame)
            # iterate video frame number
            framenumV += 1
            # press q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # when everything done, release the video capture and video write objects
    cap.release()
    out.release()
    # closes all the frames
    cv2.destroyAllWindows()
    