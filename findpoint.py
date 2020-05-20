# -*- coding: utf-8 -*-
"""
findpoint
    Identifies x and y locations of mouse double clicked.

Steps:
    1) Crop original image to zoom into plate(s) by click, hold and drag over area
    2) If cropped image is good, press 'c', then press 'esc' on next window
        If cropped image is not good, press 'r' with green box present, or 'o'
        if new image is up
    3) Double-click the location(s) of interest. You may inentify objects.
        
Input:
    file: STRING file name of video
    framenum: INT frame number to use as selection image (default=0)
    labelname = STRING a label to be displayed in window (default='')
    
Output:
    ix1: LIST x location of each double-click (pixels)
    iy1: LIST y location of each double-click (pixels)
        
Dependencies:
    cv2 (opencv)
    capture_area

Created on Wed May 20 10:36:16 2020

@author: cwiens@gmail.com, Casey Wiens
"""

import cv2
from capture_area import findarea

#%%
def clickpoint(file, framenum=0, labelname=''):
    global ix, iy, imgcrop
    ix = []
    iy = []
    
    #%% function for left double-click location
    def clickfun(event, x, y, flags, param):
        global ix, iy, imgcrop
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and display location
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(imgcrop,(x,y),1,(255,0,0),-1)
            ix.append(x)
            iy.append(y)
            
    #%% crop to area of interest
    # intialize variable
    zoom_area = None
    # open video file
    cap = cv2.VideoCapture(file)
    # set frame
    cap.set(1,framenum)
    ret, imgO = cap.read()
    while(1):
        while zoom_area is None:
            zoom_area = findarea(file,label='Crop to area of interest')
        imgcrop = imgO[zoom_area[0][1]:zoom_area[1][1],
                       zoom_area[0][0]:zoom_area[1][0],
                       :]
        cv2.namedWindow('Press esc to exit, o to recrop', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Press esc to exit, o to recrop',cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Press esc to exit, o to recrop',imgcrop)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == 111:
            cv2.destroyAllWindows()
            zoom_area = None
    cv2.destroyAllWindows()
            
    #%% find the object's location
    label = 'Press "esc" when finished. Identify point(s) of interest. ' + labelname
    cv2.namedWindow(label, cv2.WND_PROP_FULLSCREEN)
    cv2.setMouseCallback(label,clickfun)
    while(1):
        cv2.imshow(label,imgcrop)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    # add pixels that were cropped to location of selection
    ix1, iy1 = [zoom_area[0][0] + c for c in ix], [zoom_area[0][1] + c for c in iy]
    
    
    return ix1, iy1