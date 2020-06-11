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
    
    