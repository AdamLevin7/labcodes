"""
Script: vectoroverlay
    Create force-vector overlays for videos .

Modules
    vectoroverlay: Add a vector to the video to represent the ground reaction force
    vector_overlay_single: Create a single vector overlay

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def vector_overlay_single(file_force = None,
                          file_vid= None,
        flip = {0: ['fy', 'ax'], 1: ['fx', 'fy', 'ay']},
                          samp_vid = 240,
                          bw= 871,
                          contact_frame = 193,
                          plate_dim = (0.6, 0.4),
                          view = 'fy',
                          mode = 'combine',
                          disp_thresh = 2,
                          force_thresh = 20,
                          bwpermeter = 2,
                          pix2mdir = 'x',
                          platearea = 'hardcoded'):

    """
    Function::: vector_overlay_single
        Description: Create a single vector overlay
        Details:

    Inputs
    """

    # Packages
    import os
    from ImportForce_TXT import ImportForce_TXT
    from FindContactIntervals import FindContactIntervals
    from findplate import findplate
    from pixelratios import pix2m_fromplate, bw2pix
    from dataconversion_force import convertdata
    from VectorOverlay.vectoroverlay import vectoroverlay
    from tkinter import filedialog as fd
    import pandas as pd


    # Input files

    if file_force == None:
        file_force = fd.askopenfilename()
    if file_vid == None:
        file_vid = fd.askopenfilename()
    file_vid_new = file_vid[:-4] + '_OL.mp4'

    #TODO fix this hard coding, Force plates
    fp1 = 'Attila49'
    fp2 = 'Ryan52'

    data_f1_raw, samp_force, _ = ImportForce_TXT(file_force)

    ci_f1 = FindContactIntervals((data_f1_raw['Attila49 9286BA_Fz'] + data_f1_raw['Ryan52 9286BA_Fz']), samp_force,
                                 thresh=force_thresh)

    # TODO this will become an input from an Excel logsheet
    # Hardcoding the values for now... this is terrible
    # Delete this section ASAP
    if platearea == 'hardcoded':
        df1 = pd.DataFrame({'x': [931,938,1351,1283],
                           'y': [889,940,939,885]
                           })
        df1_transposed = df1.T  # or df1.transpose()

        df2 = pd.DataFrame({'x':[561,508,932,924],
                            'y':[887,941,939,889]})
        df2_transposed = df2.T

        # list of data frames
        dataframes = [df1_transposed, df2_transposed]

        # dictionary to save data frames
        plate_area = {}

        for key, value in enumerate(dataframes):
            plate_area[key] = value  # assigning data frame from list to key in dictionary

    elif platearea == None:
        plate_area = findplate(file_vid, framestart=0, label='Insert image here')

    ### Crop Data
    data_f1 = {0: data_f1_raw.filter(regex=fp1).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :],
               1: data_f1_raw.filter(regex=fp2).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :]}

    pix2m = pix2m_fromplate(plate_area, plate_dim)
    mag2pix = bw2pix(pix2m[pix2mdir], bw, bwpermeter=bwpermeter)

    transform_data = convertdata(data_f1, mag2pix, pix2m, view=view,
                                 mode=mode,
                                 platelocs=plate_area, flip=flip)

    transform_data.data2pix()

    data_pix = transform_data.data_fp

    vectoroverlay(file_vid, file_vid_new, data_pix,
                  contact_frame, samp_force=samp_force, samp_video=samp_vid,
                  dispthresh=disp_thresh)



def vectoroverlay(file, file_out, data_vid, frame_con, vect_color='g',
                  samp_force=1200, samp_video=240, dispthresh=60):
    """
    Function::: vectoroverlay
    	Description: Add a vector to the video to represent the ground reaction force
    	Details:

    Inputs
        file: STRING file name of video
        file_out: STRING file name for new video
        data_vid: DICT force and cop data, prefer that output from data2pix.
            format (0: {fx, fy, ax, ay},
                    1: {fx, fy, ax, ay},
                    ...)
        frame_con: LIST contact frame of video
            format [INT, INT, ...]
        vect_color: LIST color of vector
            format ['x', 'y', ...] for how many plates
            ex: FP1 as green and FP2 as blue: ['g', 'b']
            ex: both FPs as green: ['g', 'g']
        samp_video: INT sampling rate of video
        samp_force: INT sampling rate of force
        dispthresh: INT display threshold, amount of force needed to display
            vector (unit=Newtons, default=60)

    Outputs
        output1: None

    Dependencies
        cv2
        numpy
    """

    # Dependencies
    import cv2
    import numpy as np

    #%% reformat vect_color and frame_con if not list
    if not isinstance(vect_color, list):
        # assumes the input argument is just one letter/color, so this will make
            # it a list and as many as there are plates
        vect_color = [vect_color] * len(data_vid)
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
                                if vect_color[cntp] in ('g', 'green'):
                                    color = (0, int(255*((i+1)/samp_fact)), 0)
                                elif vect_color[cntp] in ('b', 'blue'):
                                    color = (int(255*((i+1)/samp_fact)), 0, 0)
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