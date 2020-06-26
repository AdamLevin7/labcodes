# -*- coding: utf-8 -*-
"""
capture_area

Outputs the area of the image that is selected.

Steps:
    1) Click-drag over the area you want selected.
    2) If area selection is good, press 'c' to view cropped image
        If area selection is poor, press 'r' to recrop, and repeat Step 2
    
Input:
    video: STRING file name of video
    frame: INTEGER frame number of the video to use a selection imgage (default=0)
    label: STRING a label to be displayed in window (default='')
    
Output:
    ref_point: LIST contains two tuple with x,y location of top-left and bottom-right
        location of the selected area
    
Dependencies:
    cv2 (opencv)

Created on Wed Oct 30 10:06:19 2019

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

# import the necessary packages 
import cv2

def findarea(video,frame=0,label='frame'):
    
    global ref_point
    
    # now let's initialize the list of reference point 
    ref_point = [] 
        
    def shape_selection(event, x, y, flags, param):
    	# grab references to the global variables
    	global ref_point
        
    	# if the left mouse button was clicked, record the starting
    	# (x, y) coordinates and indicate that cropping is being performed
    	if event == cv2.EVENT_LBUTTONDOWN:
    		ref_point = [(x, y)]
    
    	# check to see if the left mouse button was released 
    	elif event == cv2.EVENT_LBUTTONUP:
    		# record the ending (x, y) coordinates and indicate that 
    		# the cropping operation is finished 
    		ref_point.append((x, y))
    
    		# draw a rectangle around the region of interest 
    		cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)
    		cv2.imshow(label, frame)
             
    
    # load the image, clone it, and setup the mouse callback function    
    cap = cv2.VideoCapture(video)
    cap.set(1,frame)
    ret, frame = cap.read()
    clone = frame.copy()
    cv2.namedWindow(label, cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback(label, shape_selection)
    
    
    # keep looping until the 'q' key is pressed 
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        # press 'w' to reset the window
        if key == ord("w"):
            frame = clone.copy()
            
        # if the 'a' key is pressed, break from the loop
        elif key == ord("a"):
            break
        
    # close all open windows
    cv2.destroyAllWindows()

    return ref_point