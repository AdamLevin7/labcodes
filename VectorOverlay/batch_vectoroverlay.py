"""
Script: batch_vectoroverlay
    Batch create vector overlays.

Modules
    vect_ol_batch: Create multiple vector overlays using database
    vect_ol_batch_ls: Create multiple vector overlays using the logsheet

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""

def vect_ol_batch_ls(path, cam_name,
                     logsheet_name,
                     plate_dim = (0.6, 0.4),
                     flip = {0: ['fy', 'ax'], 1: ['fx', 'fy', 'ay']}):
    #TODO remove plate_dim from inputs and read from the logsheet**
    #TODO remove flip from inputs and read from the logsheet**
    """
    Function::: vect_ol_batch_ls
        Description: Create multiple vector overlays without using the database, only logsheet
        Details:

    Inputs
        path: STRING path to collection folder
        view: STRING view of plate (fx or fy)
        bwpermeter: INT number of pixels per meter
        plate_dim: TUPLE plate dimensions in meters
        cam_name: STRING camera name
        flip: DICT flip axes for vector orientation
        event: STRING event name
        engine: SQLALCHEMY engine
        fthresh: INT force threshold for contact detection
        feedback: STR Path with logsheet name which specifies the collection is immediate feedback,
            will use logsheet data instead of queries

    Outputs
        output1: vector overlay video to the current path

    Dependencies
        os
        labcodes
        USATF processing codes
        sqlalchemy
        pandas
    """

    # Dependencies
    import os
    from ImportForce_TXT import ImportForce_TXT
    from FindContactIntervals import FindContactIntervals
    from findplate import findplate
    from pixelratios import pix2m_fromplate, bw2pix
    from dataconversion_force import convertdata
    from VectorOverlay.vectoroverlay import vectoroverlay
    from USATF_batch_db_processing import connect_to_server
    from sqlalchemy.sql import text
    import pandas as pd
    import openpyxl
    from VectorOverlay.vectoroverlay import vector_overlay_single


    # Create additional needed paths
    path_force = os.path.join(path, 'force')
    path_video_crop = os.path.join(path, 'video', cam_name + '_cropped')
    path_video = os.path.join(path, 'video', cam_name)
    path_logsheet = os.path.join(path, logsheet_name)

    # Queries: camera info, force plate info, and logsheet info


    '''Get the logsheet info'''
    ls_workbook = openpyxl.load_workbook(os.path.join(path, logsheet_name))

    ## Info Tab
    # get the collection_id from the Info tab
    colID = ls_workbook['Info']['D2'].value
    # get the calibration_file from Info where camera_name == cam_name
    # find the row of the camera_name
    for row in range(1, 100):
        if ls_workbook['Info'][f'A{row}'].value == cam_name:
            cal_file = ls_workbook['Info'][f'D{row}'].value
            cam_extension = ls_workbook['Info'][f'C{row}'].value
            samp_vid = ls_workbook['Info'][f'B{row}'].value

            break

    ## Overlay Tab
    # get the view from the overlay tab
    view = ls_workbook['overlay']['A2'].value
    # get the bwpermeter from the overlay tab
    bwpermeter = ls_workbook['overlay']['B2'].value
    #TODO: get the flip parameters from the overlay tab

    # get fthresh from the overlay tab
    fthresh = ls_workbook['overlay']['D2'].value
    #TODO: get the plate_area from the overlay tab

    # get the mode from the overlay tab
    mode = ls_workbook['overlay']['F2'].value
    # get the disp_thresh from the overlay tab
    disp_thresh = ls_workbook['overlay']['G2'].value
    # get the pix2mdir from the overlay tab
    pix2mdir = ls_workbook['overlay']['H2'].value

    # find rows filled with data in Logsheet tab
    for row in range(1, 1000):
        if ls_workbook['Logsheet'][f'A{row}'].value == None:
            end_row = row
            break

    for i in range(2, end_row):
        # get the force file name
        file_force = ls_workbook['Logsheet'][f'K{i}'].value
        path_file_force = os.path.join(path_force, file_force + '.txt')

        # get the video file name
        #TODO: use the camera name to find the letter of the row in the Logsheet tab
        file_vid = ls_workbook['Logsheet'][f'L{i}'].value
        path_file_vid = os.path.join(path_video, file_vid + cam_extension)
        print(path_file_vid)

        # get the contact frame for that video
        #TODO make this dynamic so if the column moves it still gets the right value
        contact_frame = ls_workbook['Logsheet'][f'Q{i}'].value

        # get the athlete name for that video
        #TODO make this dynamic so if the column moves it still gets the right value
        athlete_name = ls_workbook['Logsheet'][f'A{i}'].value

        # find the bw associated with that athlete name from Info tab
        for row in range(1, 100):
            if ls_workbook['Info'][f'A{row}'].value == athlete_name:
                bw = ls_workbook['Info'][f'G{row}'].value
                break

    vector_overlay_single(file_force = path_file_force,
                          file_vid= path_file_vid,
                          flip = flip,
                          samp_vid = samp_vid,
                          bw= bw,
                          contact_frame = contact_frame,
                          plate_dim = plate_dim,
                          view = view,
                          mode = mode,
                          disp_thresh = disp_thresh,
                          force_thresh = fthresh,
                          bwpermeter = bwpermeter,
                          pix2mdir = pix2mdir,
                          platearea = None)


def vect_ol_batch(path, colID, view, bwpermeter, plate_dim, cam_name, flip, event, engine= None, fthresh=50):
    """
    Function::: vect_ol_batch
        Description: Create multiple vector overlays using database
        Details:

    Inputs
        path: STRING path to collection
        colID: INT collection ID
        view: STRING view of plate (fx or fy)
        bwpermeter: INT number of pixels per meter
        plate_dim: TUPLE plate dimensions in meters
        cam_name: STRING camera name
        flip: DICT flip axes for vector orientation
        event: STRING event name
        engine: SQLALCHEMY engine
        fthresh: INT force threshold for contact detection
        feedback: STR Path with logsheet name which specifies the collection is immediate feedback,
            will use logsheet data instead of queries

    Outputs
        output1: vector overlay video to the current path

    Dependencies
        os
        labcodes
        USATF processing codes
        sqlalchemy
        pandas
    """

    # Dependencies
    import os
    from ImportForce_TXT import ImportForce_TXT
    from FindContactIntervals import FindContactIntervals
    from findplate import findplate
    from pixelratios import pix2m_fromplate, bw2pix
    from dataconversion_force import convertdata
    from VectorOverlay.vectoroverlay import vectoroverlay
    from USATF_batch_db_processing import connect_to_server
    from sqlalchemy.sql import text
    import pandas as pd

    # Connect to Server
    if engine is None:
        engine = connect_to_server()

    # Create additional needed paths
    path_force = os.path.join(path, 'force')
    path_video_crop = os.path.join(path, 'video', cam_name + '_cropped')
    path_video = os.path.join(path, 'video', cam_name)

    # Queries: camera info, force plate info, and logsheet info


    # Camera List
    sql_cam = '''
            SELECT camera_name, sampling_rate, extension, collection_id, calibration_file
            FROM camera_list
            WHERE collection_id = {} AND camera_name = '{}'
            '''.format(colID, cam_name)

    with engine.connect().execution_options(autocommit=True) as conn:
        query_cam = conn.execute(text(sql_cam))
        cams = pd.DataFrame(query_cam.fetchall())
        cams.columns = query_cam.keys()

        # Get sampling rate
        sampvid = cams.loc[cams['camera_name'] == cam_name, 'sampling_rate'].values[0]

    # Force Plate Data
    # Check if camera_ol value exists
    sql_ol = '''
            SELECT forceplate_name
            FROM forceplate_list
            WHERE collection_id = {} AND camera_ol = '{}'
            '''.format(colID, cam_name)

    with engine.connect().execution_options(autocommit=True) as conn:
        query_ol = conn.execute(text(sql_ol))
        forceplates = pd.DataFrame(query_ol.fetchall())
        forceplates.columns = query_ol.keys()

    # if that value is null choose all FPs from that collection
    if forceplates.empty:
        sql_fp = '''
                SELECT forceplate_name
                FROM forceplate_list
                WHERE collection_id = {}
                '''.format(colID)

        with engine.connect().execution_options(autocommit=True) as conn:
            query_fp = conn.execute(text(sql_fp))
            forceplates = pd.DataFrame(query_fp.fetchall())
            forceplates.columns = query_fp.keys()


    # Force Plates
    # TODO make this more dynamic to handle multiple force plates
    # TODO make a function to account for 1 or multiple force plates
    num_plates = len(forceplates)
    if num_plates == 1:
        fp1 = forceplates['forceplate_name'][0]

    elif num_plates == 2:
        fp1 = forceplates['forceplate_name'][0]
        fp2 = forceplates['forceplate_name'][1]

    else:
        print('Error: Too many force plates')


    # Log Sheet Information
    sql_ls = '''
            SELECT collection_id, athlete_id, jump_id, athlete_name, jump_num, force_file, {}
            FROM jump_list
            WHERE collection_id = {}
            '''.format(cam_name, colID)

    with engine.connect().execution_options(autocommit=True) as conn:
        query_ls = conn.execute(text(sql_ls))
        df_ls = pd.DataFrame(query_ls.fetchall())
        df_ls.columns = query_ls.keys()

    # Filter down the logsheet to only the trials which have forceplate data, contact ID, and video available
    df_ls = df_ls[df_ls[cam_name].notna()]
    df_ls = df_ls[df_ls['force_file'].notna()]

    sql_event_id = '''
            SELECT *
            FROM eventid_list
            WHERE camera = '{}'
            '''.format(cam_name)

    with engine.connect().execution_options(autocommit=True) as conn:
        query_event_id = conn.execute(text(sql_event_id))
        df_event_id = pd.DataFrame(query_event_id.fetchall())
        df_event_id.columns = query_event_id.keys()

    # Get rid of the rows that aren't from the collection
    # Merge df_ls and df_event_id
    df_trials = df_event_id.merge(df_ls, how='left', on=['jump_id'])
    df_trials = df_trials[df_trials['collection_id'] == colID]


    # Get BW for athletes in the collection
    sql_ath_bw = '''
            SELECT *
            FROM athinfo_list
            WHERE collection_id = {}
            '''.format(colID)

    with engine.connect().execution_options(autocommit=True) as conn:
        query_bw = conn.execute(text(sql_ath_bw))
        df_bw = pd.DataFrame(query_bw.fetchall())
        df_bw.columns = query_bw.keys()

    #TODO this  needs to be saved to the camera table rather than the force plate table
    # Save plate corners to database
    for i in range(len(forceplates)):
        ## Find Plate Corners, use first video file
        # Need a video where they aren't in blocks to get corners
        calibration_vid = cams['calibration_file'][i] + cams['extension'][i]

        # Find Plate Corners
        # Check database to see if plate corners are already in the database
        # This should be put in a separate processing code because it would be used for multiple codes
        # TODO this isn't working to read back in plate_area dataframe from the database
        # for i in range(len(forceplates)):
        #
        #     sql_corners = '''
        #             SELECT fp_coordinates
        #             FROM forceplate_list
        #             WHERE collection_id = {} AND forceplate_name = '{}'
        #             '''.format(colID, forceplates['forceplate_name'][i])
        #
        #     with engine.connect().execution_options(autocommit=True) as conn:
        #         query_corners = conn.execute(text(sql_corners))
        #         plate_area[i] = pd.DataFrame(query_corners.fetchall())
        #         plate_area[i].columns = query_corners.keys()
        #
        #         # Convert the dataframe to a dict
        #         plate_area = plate_area.to_dict('records')

        # If corners are not in the database, find them
        # if plate_area[0] is None:
        # Find Plate Corners
        plate_area = findplate(os.path.join(path_video, calibration_vid), framestart=0,
                               label='Insert image here')

        # Sql query to write coordinates to DB
        sql_update_corners = '''
                UPDATE forceplate_list
                SET fp_coordinates = '{}'
                WHERE collection_id = {} AND forceplate_name = '{}'
                '''.format(str(plate_area[i]), colID, forceplates['forceplate_name'][i])

        with engine.connect().execution_options(autocommit=True) as conn:
            conn.execute(text(sql_update_corners))

    for i in range(len(df_trials)):
        # Load Force Data
        data_force_raw, samp, _ = ImportForce_TXT(os.path.join(path_force, df_trials['force_file'].iloc[i] + '.txt'))

        # Get bodyweight for that trial
        bw = df_bw.loc[df_bw['athlete_id'] == df_trials['athlete_id'].iloc[i], fp1].values[0]

        # Check which force plate is used
        if  'Attila' in fp1 or 'Ryan' in fp1:

            # Contact Intervals
            ci_f1 = FindContactIntervals((data_force_raw['Attila49 9286BA_Fz'] + data_force_raw['Ryan52 9286BA_Fz']), samp,
                                         thresh=fthresh)
        else:
            # USATF collection
            # Contact Intervals
            ci_f1 = FindContactIntervals(data_force_raw[fp1[:-2] +' '+fp1[-2:] +' 9287A_Fz'], samp, thresh=fthresh)

        # Crop Data
        # Check how many force plate are used
        if num_plates == 1:
            data_force = {0: data_force_raw.filter(regex=fp1[:-2] +' '+fp1[-2:] ).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :]}
        else:

            data_force = {0: data_force_raw.filter(regex=fp1[:-2] +' '+fp1[-2:] ).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :],
                          1: data_force_raw.filter(regex=fp2[:-2] +' '+fp2[-2:] ).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :]}

        # Pixel to meter ratios
        pix2m = pix2m_fromplate(plate_area, plate_dim)
        mag2pix = bw2pix(pix2m['x'], bw, bwpermeter=bwpermeter)

        # If there is one plate
        if num_plates == 1:
            transform_data = convertdata(data_force, mag2pix, pix2m, view=view,
                                         mode="ind", platelocs=plate_area, flip=flip)
        else:
            transform_data = convertdata(data_force, mag2pix, pix2m, view=view,
                                         mode="combine", platelocs=plate_area, flip=flip)

        transform_data.data2pix()

        data_pix_f1 = transform_data.data_fp

        file_vid = df_trials['file'].iloc[i] + '.mp4'
        file_vid_new = df_trials['file'].iloc[i] + '_OL.mp4'

        # Get the sync frame
        sync_frame = df_trials[event].iloc[i]

        # Change system path so videos go to the correct folder
        os.chdir(path_video_crop)

        vectoroverlay(os.path.join(path_video_crop, file_vid),
                      file_vid_new, data_pix_f1,
                      sync_frame, samp_force=samp, samp_video=sampvid,
                      dispthresh=2)