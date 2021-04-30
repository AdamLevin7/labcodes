# -*- coding: utf-8 -*-
"""
strobe

Generates a strobe image and/or video.

User input:
    - filename: STRING full path file name
    - filesave: STRING full path file name that is to be saved
        - image: jpeg
        - video: mp4
    - frames: SERIES list of strobe frames
    - searcharea (optional): DICTIONARY list of searcha area for each strobe frame
        - key: frame number
        - value: search area from capture_area.py's 'find_area
    - samp: INT sampling rate of video
    - thresh: INT absolute difference threshold to find which pixels changed
    - bgint: INT number of frame difference from current image to use as subtraction image

Created on Thu Feb  6 12:35:18 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import cv2
import numpy as np
from scipy import ndimage


def strobe(filename, filesave, frames, searcharea=None, samp=240, thresh=60, bgint=5):
    
    #%% load file
    cap = cv2.VideoCapture(filename)
    
    #%% initalize video
    # remove extension if included in filename
    if filesave[-4] == '.':
        filesave = filesave[:-4]
    # default resolutions of the frame are obtained.The default resolutions are system dependent.
    # we convert the resolutions from float to integer.
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # define the codec and create VideoWriter object
    out = cv2.VideoWriter(filesave+'.mp4', cv2.VideoWriter_fourcc('M','P','4','V'),
                          samp/4, (frame_width,frame_height))
    
    #%% iterate through frames
    for cnt in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        #%% set bgint if too large for video
        if cnt+bgint >= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            bgint -= 1
        #%% if this is the first frame
        if cnt == frames.iloc[0]:
            # set counter for strobe frame number
            strobeframe = 0
            # set frame and create copy
            cap.set(1,cnt)
            ret, img = cap.read()
            img_c1 = img.copy()
            img_c1_blur = cv2.medianBlur(img_c1, 7)
            # set background (subtraction frame) and copy image
            cap.set(1,cnt+bgint)
            ret, img_bg = cap.read()
            img_bg_c1 = img_bg.copy()
            img_bg_blur = cv2.medianBlur(img_bg_c1, 7)
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img1 = np.zeros(img.shape,'uint8')
                img1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1_blur[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_blur[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # find absolute difference between frames and then sum along BGR axis
            diff = np.sum(cv2.absdiff(img_bg, img1),axis=2)
            # dilate image to fill holes
            keeppixels = ndimage.binary_dilation(diff>thresh, iterations=3)
            # set base black image, then store image
            img_new = np.zeros(img_c1.shape,'uint8')
            img_new[keeppixels,:] = img_c1[keeppixels,:]
            # set strobe image
            img_strobe = img_c1
            
        #%% if a strobe frame that wasn't first
        elif (cnt == frames).any():
            # iterate counter of strobe frame number
            strobeframe += 1
            # set frame and create copy
            cap.set(1,cnt)
            ret, img = cap.read()
            img_c1 = img.copy()
            img_c1_blur = cv2.medianBlur(img_c1, 7)
            # set background (subtraction frame)
            cap.set(1,cnt+bgint)
            ret, img_bg = cap.read()
            img_bg_c1 = img_bg.copy()
            img_bg_blur = cv2.medianBlur(img_bg_c1, 7)
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img1 = np.zeros(img.shape,'uint8')
                img1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1_blur[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_blur[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # find absolute difference between frames and then sum along BGR axis
            diff = np.sum(cv2.absdiff(img_bg, img1),axis=2)
            # dilate image to fill holes
            keeppixels = ndimage.binary_dilation(diff>thresh, iterations=3)
            # set base black image, then store image
            img_new[keeppixels,:] = img_c1[keeppixels,:]
            # update strobe image
            img_strobe[keeppixels,:] = img_c1[keeppixels,:]
            
        #%% if not a strobe frame
        if (cnt < frames.iloc[0]):
            # set current frame
            cap.set(1, cnt)
            ret, img = cap.read()
            if ret == True:
                # write the frame into the file
                out.write(img)
            else:
                break
        else:
            # set current frame
            cap.set(1, cnt)
            ret, img = cap.read()
            img_c1 = img.copy()
            # set background (subtraction frame)
            cap.set(1,cnt+bgint)
            ret, img_bg = cap.read()
            img_bg_c1 = img_bg.copy()
            # if frame is not after the last strobe
            if (searcharea is not None) and (cnt < frames.iloc[-1]):
                # identify previous search area
                crop1 = searcharea[frames.iloc[strobeframe]]
                # identify next search area
                crop2 = searcharea[frames.iloc[strobeframe+1]]
                # create the widest search area from the two given search areas
                left = np.min([crop1[0][0],crop1[1][0],crop2[0][0],crop2[1][0]])
                right = np.max([crop1[0][0],crop1[1][0],crop2[0][0],crop2[1][0]])
                top = np.min([crop1[0][1],crop1[1][1],crop2[0][1],crop2[1][1]])
                bottom = np.max([crop1[0][1],crop1[1][1],crop2[0][1],crop2[1][1]])
                crop = [(left,top),(right,bottom)]
                # set base black image, then store image
                img1 = np.zeros(img.shape,'uint8')
                img1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            else: # if frame is after last strobe frame
                # if object is moving left
                if searcharea[frames.iloc[strobeframe]][0][0] - searcharea[frames.iloc[strobeframe-1]][0][0] < 0:
                    # identify last search area
                    crop1 = searcharea[frames.iloc[strobeframe]]
                    # create the widest search area from the two given search areas
                    crop = [(1,crop1[0][1]-50),(crop1[1][0],crop1[1][1]+50)]
                else: # if object is moving right
                    # identify last search area
                    crop1 = searcharea[frames.iloc[strobeframe]]
                    # create the widest search area from the two given search areas
                    crop = [(crop1[0][0],crop1[0][1]-50),(frame_width,crop1[1][1]+50)]
                # set base black image, then store image
                img1 = np.zeros(img.shape,'uint8')
                img1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # find absolute difference between frames and then sum along BGR axis
            diff = np.sum(cv2.absdiff(img_bg, img1),axis=2)
            # dilate image to fill holes
            keeppixels = ndimage.binary_dilation(diff>thresh, iterations=3)
            # set base black image, then store image
            img_cur = np.zeros(img.shape,'uint8')
            img_cur[keeppixels,:] = img_c1[keeppixels,:]
            # place current strobe image on top of video image
            img[np.sum(img_new,axis=2)>0,:] = img_new[np.sum(img_new,axis=2)>0,:]
            # place current strobe image on top of video image
            img[np.sum(img_cur,axis=2)>0,:] = img_cur[np.sum(img_cur,axis=2)>0,:]
            if ret == True:
                # write the frame into the file
                out.write(img)
            else:
                break
            
    #%% close image file and windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    #%% write out image
    cv2.imwrite(filesave + '.jpg', img_strobe)


#%% function for only strobe image
def strobe_image(filename, filesave, frames, searcharea=None, samp=240, thresh=60, bgint=5):

    #%% load file
    cap = cv2.VideoCapture(filename)
    
    #%% iterate through frames
    for cnt in frames:
        #%% set bgint if too large for video
        if cnt+bgint >= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            bgint -= 1
        #%% if this is the first frame
        if cnt == frames.iloc[0]:
            # set frame and create copy
            cap.set(1,cnt)
            ret, img = cap.read()
            img_c1 = img.copy()
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img = np.zeros(img.shape,'uint8')
                img[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # set background (subtraction frame) and copy image
            cap.set(1,cnt+bgint)
            ret, img_bg = cap.read()
            img_bg_c1 = img_bg.copy()
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # find absolute difference between frames and then sum along BGR axis
            diff = np.sum(cv2.absdiff(img_bg, img),axis=2)
            # dilate image to fill holes
            keeppixels = ndimage.binary_dilation(diff>thresh, iterations=3)
            # set base black image, then store image
            img_new = np.zeros(img_c1.shape,'uint8')
            img_new[keeppixels,:] = img_c1[keeppixels,:]
            # set strobe image
            img_strobe = img_c1
            # set current strobe image on
            
        #%% if a strobe frame that wasn't first
        elif (cnt == frames).any():
            # set frame and create copy
            cap.set(1,cnt)
            ret, img = cap.read()
            img_c1 = img.copy()
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img = np.zeros(img.shape,'uint8')
                img[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # set background (subtraction frame)
            cap.set(1,cnt+bgint)
            ret, img_bg = cap.read()
            img_bg_c1 = img_bg.copy()
            # if only searching within specified area
            if searcharea is not None:
                # identify current search area
                crop = searcharea[cnt]
                # set base black image, then store image
                img_bg = np.zeros(img.shape,'uint8')
                img_bg[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]] = img_bg_c1[crop[0][1]:crop[1][1],crop[0][0]:crop[1][0]]
            # find absolute difference between frames and then sum along BGR axis
            diff = np.sum(cv2.absdiff(img_bg, img),axis=2)
            # dilate image to fill holes
            keeppixels = ndimage.binary_dilation(diff>thresh, iterations=3)
            # set base black image, then store image
            img_new[keeppixels,:] = img_c1[keeppixels,:]
            # update strobe image
            img_strobe[keeppixels,:] = img_c1[keeppixels,:]
            
    #%% close image file and windows
    cap.release()
    cv2.destroyAllWindows()
    
    #%% write out image
    if filesave[-4] == '.':
        filesave = filesave[:-4]
    cv2.imwrite(filesave + '.jpg', img_strobe)
    
    
    
#%%
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
    - autoid_thresh: OPTIONAL default: None, minimum number of frames between manually 
        identified strobe frames before auto id occurs (will find apex and two
        additional frames before and after apex)
    - autoid_num: OPTIONAL default None, number of frames to automatically find
        when autoid_thresh is triggered (ex: when two manual frames are spaced
                                         greater than autoid_thresh, it will find
                                         autoid_num of frames -including the
                                         original two frames- between the
                                         chosen frames)

Created on Thu Feb 6 10:36:26 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

from findframe import findframe
import pandas as pd
from capture_area import findarea
import numpy as np

def strobe_findframes(filename, crop='yes', autoid_thresh=None, autoid_num=None):
    ### initialize variables
    strobeframes = None
    frame = 0
    key = 0
    
    ### while user has not pressed escape
    while key != 27:
        ### if first strobe image
        # update frame and strobe frame list
        if strobeframes is None:
            frame, key = findframe(filename,
                                   label='Strobe Frames: ',
                                   framestart=frame)
            strobeframes = pd.Series(frame)
            ### if crop was chosen
            if crop == 'yes':
                # find search area
                area = findarea(filename,frame=frame,label='Select area around object')
                searcharea = {frame: area}
        ### if it is not first strobe image
        else:
            frame, key = findframe(filename,
                                   label='Strobe Frames: ' + ",".join("{0}".format(n) for n in strobeframes),
                                   framestart=frame)
            strobeframes = strobeframes.append(pd.Series(frame)).reset_index(drop=True)
            ### if crop was chosen
            if crop == 'yes':
                # find search area
                area = findarea(filename,frame=frame,label='Select area around object')
                searcharea[frame] = area
            
    ### drop duplicates
    strobeframes = strobeframes.drop_duplicates()
    
    ### if auto-find frames was selected
    if autoid_thresh is not None:
        # store strobeframes as another variable to use as search
        sframestemp = strobeframes
        # find difference between selected frames
        diffframes = np.diff(strobeframes)
        # auto select evenly spaced frames
        for cntdf in range(len(diffframes)):
            if diffframes[cntdf] >= autoid_thresh:
                frames = np.linspace(sframestemp.iloc[cntdf],
                                     sframestemp.iloc[cntdf+1], autoid_num, dtype=int)
                strobeframes = (strobeframes.append(pd.Series(frames)).reset_index(drop=True)).sort_values(ignore_index=True).drop_duplicates()
                # if crop was selected, crop area for each new frame
                if crop == 'yes':
                    for cntf in frames[1:-1]:
                        area = findarea(filename,frame=cntf,label='Select area around object')
                        searcharea[cntf] = area
    
    ###
    return strobeframes, searcharea


"""
strobe_autofindframes

Auto identifies which frames to use for strobe creation.
    - Usefully to find consistent number of strobe frames with consistent spacing between two events
        - example, flight phase in the long jump 

User input:
    - frames: current series of already identified frames
    - autoid_thresh: OPTIONAL default: 25, minimum number of frames between manually 
        identified strobe frames before auto id occurs (will find apex and two
        additional frames before and after apex)
    - autoid_num: OPTIONAL default: 7, number of frames to automatically find
        when autoid_thresh is triggered (ex: when two manual frames are spaced
                                         greater than autoid_thresh, it will find
                                         autoid_num of frames -including the
                                         original two frames- between the
                                         chosen frames)

Created on Tue Apr 27 4:45:26 2021

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""


def strobe_autofindframes(frames, autoid_thresh=25, autoid_num=7):
    import pandas as pd
    import numpy as np

    """ initialize parameters """
    strobeframes = frames.copy()

    # store strobeframes as another variable to use as search
    sframestemp = strobeframes
    # find difference between selected frames
    diffframes = np.diff(frames)
    # auto select evenly spaced frames
    for cntdf in range(len(diffframes)):
        if diffframes[cntdf] >= autoid_thresh:
            tempframes = np.linspace(frames.iloc[cntdf],
                                     frames.iloc[cntdf + 1], autoid_num, dtype=int)
            strobeframes = (strobeframes.append(pd.Series(tempframes)).reset_index(drop=True)).sort_values(
                ignore_index=True).drop_duplicates()

    return strobeframes


"""
strobe_findarea

Allows user to identify the search area for the create of strobes.
    - Note: this can only be used if the frames have already been identified

User input:
    - filename: full path file name
    - frames: current series of identified frames

Created on Tue Apr 27 4:45:26 2021

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

def strobe_findarea(filename, frames):
    import pandas as pd
    from capture_area import findarea
    import numpy as np

    """ initialize variables """
    searcharea = None

    """ loop through frames to identify search area """
    for frame in frames:
        # update frame and strobe frame list
        if searcharea is None:
            area = findarea(filename,frame=frame,label='Select area around object')
            searcharea = {frame: area}
        # if it is not first strobe image
        else:
            # find search area
            area = findarea(filename,frame=frame,label='Select area around object')
            searcharea[frame] = area

    return searcharea