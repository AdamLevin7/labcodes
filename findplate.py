# -*- coding: utf-8 -*-
"""
findplate

Identifies the four corners of the plate(s) in the image.

Steps:
    1) Crop original image to zoom into plate(s) by click, hold and drag over area
    2) If cropped image is good, press 'c', then press 'esc' on next window
        If cropped image is not good, press 'r' with green box present, or 'o'
        if new image is up
    3) Double-click the corners of the plate in counter-clockwise motion, starting
        with the upper left corner. You may inentify multiple plates.
        
Input:
    file: STRING file name of video
    framenum: INT frame number to use as selection image (default=0)
    labelname = STRING a label to be displayed in window (default='')
    
Output:
    plate: DICT containing 2x4 dataframe with rows x and y.
        Column order is dependent on the selection order.
        Size of DICT dependent on number of plates.
        
Dependencies:
    cv2 (opencv)
    pandas
    capture_area

Created on Thu Jan  2 15:10:57 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""
import cv2
import pandas as pd
from capture_area import findarea

#%%
def findplate(file, framenum=0, labelname=''):
    global ix, iy, imgcrop
    ix = []
    iy = []
    
    def clickfun(event, x, y, flags, param):
        global ix, iy, imgcrop
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(imgcrop,(x,y),1,(255,0,0),-1)
            ix.append(x)
            iy.append(y)
            
    #%% crop area to plate
    plate_area = None
    cap = cv2.VideoCapture(file)
    cap.set(1,framenum)
    ret, imgO = cap.read()
    while(1):
        while plate_area is None:
            plate_area = findarea(file,label='Crop to area of force plate(s)')
        imgcrop = imgO[plate_area[0][1]:plate_area[1][1],
                       plate_area[0][0]:plate_area[1][0],
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
            plate_area = None
    cv2.destroyAllWindows()
            
    #%% find the corners of the plate
    label = 'Press "esc" when finished. Identify corners in counterclockwise starting with top left. ' + labelname
    cv2.namedWindow(label, cv2.WND_PROP_FULLSCREEN)
    cv2.setMouseCallback(label,clickfun)
    while(1):
        cv2.imshow(label,imgcrop)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    ix1, iy1 = [plate_area[0][0] + c for c in ix], [plate_area[0][1] + c for c in iy]
    plate_temp = pd.DataFrame((ix1,iy1)).rename(index={0: 'x', 1: 'y'})
    
    #%% convert plate to dictionary
    # initialize plate
    plate = {}
    # loop through number of plates
    for cnt in range(int(len(plate_temp.columns)/4)):
        plate[cnt] = plate_temp.iloc[:, (cnt*4):4*(cnt+1)]
    
    
    return plate