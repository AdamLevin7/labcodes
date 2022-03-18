"""
Script: addcentermasstraj
    Add visual representation of center of mass location and trajectory.

Modules
    addcmtraj: Add visual representation of center of mass location and trajectory.

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def addcmtraj(file_vid, data, file_vid_n='cmtrajectoryvideo.mp4', samp_vid=120,
              data_max=None, data_min=None, olimage='yes'):
    """
    Function::: addcentermasstraj
    	Description: Add visual representation of center of mass location and trajectory.
    	Details: Full description with details here

    Inputs
        file_vid: STR full file name of video
        data: DATAFRAME
            Column 0: frame
            Column 1: center of mass x location (pixels)
            Column 2: center of mass y location (pixels)
        file_vid_n: STR full file name of new video (default: cmtrajectoryvideo.mp4)
        samp_vid: INT sampling rate of video (Hz) (default: 120)
        data_max: DATAFRAME display max range on video
            Column 0: frame
            Column 1: center of mass x location (pixels)
            Column 2: center of mass y location (pixels)
        data_min: DATAFRAME display min range on video
            Column 0: frame
            Column 1: center of mass x location (pixels)
            Column 2: center of mass y location (pixels)

    Outputs
        video with body center of mass location and trajectory visually represented
        image of each frame with body center of mass location and trajectory visually represented
            location: 'SkeletonOL' folder within location of file_vid

    Dependencies
        cv2
        os
    """

    # Dependencies
    import cv2
    import os
    
    #%% set up location to store images
    if olimage == 'yes':
        # if just file name was given
        if os.path.dirname(file_vid) == '':
            savefolder = 'TrajectoryOL'
        else:
            savefolder = os.path.join(os.path.dirname(file_vid), 'TrajectoryOL')
        # if folder does not exist
        if not os.path.exists(savefolder):
            os.makedirs(savefolder)

    #%% load video file and initialize new video
    cap = cv2.VideoCapture(file_vid)
    # default resolutions of the frame are obtained.The default resolutions are system dependent.
    # we convert the resolutions from float to integer.
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    # define the codec and create VideoWriter object
    vid_out = cv2.VideoWriter(file_vid_n, cv2.VideoWriter_fourcc('M','P','4','V'),
                              samp_vid/4, (frame_width,frame_height))
    
    #%% create video
    # data index counter
    cnt = 0
    # frame number 
    framenum = 0
    while(True):
        ret, frame = cap.read()
        if ret == True:
            
            #%% apply line up to and including image
            # if current frame is in data
            if framenum in range(int(data['frame'].iloc[0]),int(data['frame'].iloc[-1])):
                
                #%% create trajectory (MAX RANGE)
                if data_max is not None:
                    for cntt in range(0,len(data)-1, 4):
                        # create tuple
                        orig_loc = tuple(data_max.iloc[cntt,1:].astype(int))
                        oth_loc = tuple(data_max.iloc[cntt+1,1:].astype(int))
                        # draw segment with red line
                        frame = cv2.line(frame, orig_loc, oth_loc, (0,255,255), thickness=2)
                    
                    #%% display center of mass
                    # create tuple
                    cm_loc = tuple(data_max.iloc[cnt,1:].astype(int))
                    # display center of mass location
                    frame = cv2.circle(frame, cm_loc, 5, (0,0,0), -1)
                
                #%% create trajectory (MIN RANGE)
                if data_min is not None:
                    for cntt in range(0, len(data)-1, 4):
                        # create tuple
                        orig_loc = tuple(data_min.iloc[cntt,1:].astype(int))
                        oth_loc = tuple(data_min.iloc[cntt+1,1:].astype(int))
                        # draw segment with red line
                        frame = cv2.line(frame, orig_loc, oth_loc, (0,255,255), thickness=2)
                    
                    #%% display center of mass
                    # create tuple
                    cm_loc = tuple(data_min.iloc[cnt,1:].astype(int))
                    # display center of mass location
                    frame = cv2.circle(frame, cm_loc, 5, (0,0,0), -1)
                
                #%% create trajectory
                for cntt in range(len(data)-1):
                    # create tuple
                    orig_loc = tuple(data.iloc[cntt,1:].astype(int))
                    oth_loc = tuple(data.iloc[cntt+1,1:].astype(int))
                    # draw segment with red line
                    frame = cv2.line(frame, orig_loc, oth_loc, (0,255,255), thickness=3)
                
                #%% display center of mass
                # create tuple
                cm_loc = tuple(data.iloc[cnt,1:].astype(int))
                # display center of mass location
                frame = cv2.circle(frame, cm_loc, 8, (0,0,0), -1)
                # iterate data index counter
                cnt += 1
            
            #%% save frame and add to video
            if olimage == 'yes':
                # create frame name
                framename = os.path.join(savefolder,
                                         os.path.basename(file_vid)[ :-4] + '_' + str(framenum) + '.png')
                cv2.imwrite(framename, frame)
            # write the frame into the file
            vid_out.write(frame)
            # iterate frame number
            framenum += 1
        else:
            break
            
    #%% when everything done, release the video capture and video write objects
    cap.release()
    vid_out.release()
    # closes all the frames
    cv2.destroyAllWindows()