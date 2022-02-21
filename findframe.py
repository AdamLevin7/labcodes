# -*- coding: utf-8 -*-
"""
findframe
    Exports frame number of last frame identified. User manually moves through video
    searching for frame of interest. When frame is found, click 'q' or 'esc' to exit.
        
Inputs
    file: STR full file name of video
    label: STR text to be displayed in window (default: Find Frame)
    framestart: INT start search at this frame (default: 0)
    
Outputs
    cnt: INT frame number when video was closed
    key: INT key identifier for last selected key

Dependencies:
    cv2 (opencv)

The following buttons shift the current frame by:
    k : -100
    m : -10
    , : -1
    . : +1
    / : +10
    ; : +100
    
If the trackbar was manually moved, user must press a key before it will update.
    

Created on Fri Dec 27 11:10:54 2019

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""


def findframe(file, label='Find Frame', framestart=0):

    import cv2
    import wx
    import os
    import matplotlib.pyplot as plt
    
    # idenify screen resolution
    app = wx.App(False)
    width, height = wx.GetDisplaySize()
    app.Destroy()

    #%% set call back for trackbar
    def nothing(x):
        pass

    """ create figure to use as hotkey help and strobe frame info """
    # set string for hotkey help
    hotkey_text = ("you can advance using the trackbar but must click button after to update\n"
                   "'k' = -100 | 'm' = -10 | ',' = -1 | '.' = +1 | '/' = +10 | ';' = +100\n"
                   "click 'q' to select frame when identified in GUI\n"
                   "click 'esc' to exit out of GUI")
    # turn off toolbar
    plt.rcParams['toolbar'] = 'None'
    # create figure
    plt.figure("Find Frame - Hot Key Info", figsize=(10.75, 1.25), dpi=80)
    # turn axes off
    plt.axis('off')
    # set up the fig manager to set location
    mngr = plt.get_current_fig_manager()
    # set location in upper left corner
    mngr.window.setGeometry(25, 50, mngr.window.geometry().getRect()[2], mngr.window.geometry().getRect()[3])
    # display help info text
    plt.text(0, 0, hotkey_text, size=16)
    # show image
    plt.show()
    
    #%% initialize window
    cv2.namedWindow(label, cv2.WINDOW_NORMAL)
    cnt = framestart
    cap = cv2.VideoCapture(file)
    ret, im1 = cap.read()
    cap.set(1,cnt)
    ret, im1 = cap.read()
    
    #%% resize window
    (h, w) = im1.shape[:2]
    r = height*0.75 / float(h)
    dim = (int(w*r), int(height*0.75))
    cv2.resizeWindow(label, dim)
    cv2.moveWindow(label, 25, 50+mngr.window.geometry().getRect()[3])
    
    #%% create and set trackbar
    cv2.createTrackbar('Frame', label, framestart, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), nothing)

    #%%
    key = 0
    while cap.isOpened():
        #%% display current frame
        cap.set(1,cnt)
        ret, im1 = cap.read()
        if not ret:
            break
        cv2.imshow(label, im1)
        key = cv2.waitKey(0)

        # user clicks the window's X to close window
        if cv2.getWindowProperty(label,cv2.WND_PROP_VISIBLE) < 1:
            break

        #%% get trackbar location
        while cv2.getTrackbarPos('Frame', label) != cnt:
            cnt = cv2.getTrackbarPos('Frame', label)
            cap.set(1,cnt)
            ret, im1 = cap.read()
        
        #%% increase/decrease frame number
        if key == ord('q'):
            # press q to quit
            break
        elif key == 27:
            # press esc to quit
            break
        elif key == 107:
            # press K button to go back 100 frames
            cnt -= 100
        elif key == 109:
            # press M button to go back 10 frames
            cnt -= 10
        elif key == 44:
            # press , button to go back 1 frame
            cnt -= 1
        elif key == 46:
            # press . button to go forward 1 frame
            cnt += 1
        elif key == 47:
            # press / button to go forward 10 frames
            cnt += 10
        elif key == 59:
            # press ; button to go forward 100 frames
            cnt += 100
        elif cv2.getWindowProperty(label,cv2.WND_PROP_VISIBLE) < 1:
            # user clicks the window's X to close window
            break
        cnt = max([0, cnt])
        
        #%% set trackbar
        cv2.setTrackbarPos('Frame', label, cnt)
        
    #%% close windows
    plt.close("Find Frame - Hot Key Info")
    cap.release()
    if cv2.getWindowProperty(label,cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyWindow(label)
    
    return cnt, key