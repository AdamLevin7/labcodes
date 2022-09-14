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


def findarea(video, frame=0, label='frame', method="boundingbox"):
    
    #import wx
    import sys
    import cv2
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RectangleSelector, Button
    import tkinter as tk


    root = tk.Tk()
    height = root.winfo_screenheight()
    
    # identify screen resolution
    #app = wx.App(False)
    #width, height = wx.GetDisplaySize()
    #app.Destroy()
    
    # set label to show
    labelshow = 'a: advance, w: recrop. ' + label

    # load in video and set to specific frame
    cap = cv2.VideoCapture(video)
    cap.set(1,frame)
    ret, frame = cap.read()

    # resize window
    (h, w) = frame.shape[:2]
    r = height * 0.75 / float(h)
    dim = (int(w * r), int(height * 0.75))
    
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
    		cv2.imshow(labelshow, frame)

    def line_select_callback(eclick, erelease):
        # grab references to the global variables
        global ref_point

        ref_point = [(int(eclick.xdata), int(eclick.ydata))] # x1, y1
        ref_point.append((int(erelease.xdata), int(erelease.ydata))) # x2, y2

    def validate_crop(*args):
        fig.canvas.stop_event_loop()

    def display_help(*args):
        print(
            "1. Use left click to select the region of interest. A green box will be drawn around the selected region.\n\n"
            "2. Use the corner points to expand the box and center to move the box around the image.\n\n"
            "3. Click"
        )

    """ select area methods """
    if method == "boundingbox":
        " bounding box version - modified from DeepLabCut auxfun_videos.py from DLC 2.2b7 "
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        fig = plt.figure(figsize=(dim[0]*px, dim[1]*px))
        ax = fig.add_subplot(111)
        ax.imshow(frame[:, :, ::-1])
        ax.axis('off')
        plt.title('Click and drag to select area. Modify if needed. Then click the "Crop" button')
        ax_help = fig.add_axes([0.9, 0.2, 0.1, 0.1])
        ax_save = fig.add_axes([0.9, 0.1, 0.1, 0.1])
        crop_button = Button(ax_save, "Crop")
        crop_button.on_clicked(validate_crop)
        help_button = Button(ax_help, "Help")
        help_button.on_clicked(display_help)

        # create rectangular selection
        rs = RectangleSelector(
            ax,
            line_select_callback,
            drawtype="box",
            minspanx=5,
            minspany=5,
            interactive=True,
            spancoords="pixels",
            rectprops=dict(facecolor="green", edgecolor="black", alpha=0.3, fill=True),
        )
        plt.show()

        fig.canvas.start_event_loop(timeout=-1)

        plt.close(fig)

    elif method == "clickdrag":
        " old version - click and drag with redo option"
        # load the image, clone it, and setup the mouse callback function
        clone = frame.copy()
        cv2.namedWindow(labelshow, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(labelshow, shape_selection)
        cv2.resizeWindow(labelshow, dim)

        # keep looping until the 'q' key is pressed
        while True:
            cv2.imshow(labelshow, frame)
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


#%%
"""
draw_bbox

Copied from DeepLabCut auxfun_videos.py from DLC 2.2b7
"""
def draw_bbox(video, frame):

    import cv2
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RectangleSelector, Button

    clip = cv2.VideoCapture(video)
    if not clip.isOpened():
        print("Video could not be opened. Skipping...")
        return

    success = False
    # Read the video until a frame is successfully read
    while not success:
        #%% display current frame
        clip.set(1,frame)
        success, frame = clip.read()

    bbox = [0, 0, frame.shape[1], frame.shape[0]]

    def line_select_callback(eclick, erelease):
        #bbox[:2] = int(eclick.xdata), int(eclick.ydata)  # x1, y1
        #bbox[2:] = int(erelease.xdata), int(erelease.ydata)  # x2, y2
        bbox = [(int(eclick.xdata), int(eclick.ydata))] # x1, y1
        bbox.append((int(erelease.xdata), int(erelease.ydata))) # x2, y2

    def validate_crop(*args):
        fig.canvas.stop_event_loop()

    def display_help(*args):
        print(
            "1. Use left click to select the region of interest. A green box will be drawn around the selected region.\n\n"
            "2. Use the corner points to expand the box and center to move the box around the image.\n\n"
            "3. Click"
        )

    #
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(frame[:, :, ::-1])
    ax.axis('off')
    ax_help = fig.add_axes([0.9, 0.2, 0.1, 0.1])
    ax_save = fig.add_axes([0.9, 0.1, 0.1, 0.1])
    crop_button = Button(ax_save, "Crop")
    crop_button.on_clicked(validate_crop)
    help_button = Button(ax_help, "Help")
    help_button.on_clicked(display_help)

    # create rectangular selection
    rs = RectangleSelector(
        ax,
        line_select_callback,
        drawtype="box",
        minspanx=5,
        minspany=5,
        interactive=True,
        spancoords="pixels",
        rectprops=dict(facecolor="green", edgecolor="black", alpha=0.3, fill=True),
    )
    plt.show()

    fig.canvas.start_event_loop(timeout=-1)

    plt.close(fig)
    return bbox
