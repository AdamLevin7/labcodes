"""
Script: batch_vectoroverlay
    Batch create vector overlays.

Modules
    batch_vectoroverlay: Create multiple vector overlays using database

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""

def vect_ol_batch(path, colID, view, bwpermeter, plate_dim, cam_name, flip, event, engine= None):
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
    sql = '''
            SELECT forceplate_name
            FROM forceplate_list
            WHERE collection_id = {}
            '''.format(colID)

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(sql))
        forceplates = pd.DataFrame(query.fetchall())
        forceplates.columns = query.keys()

    # Force Plates
    # TODO make this more dynamic to handle multiple force plates
    # TODO make a function to account for 1 or multiple force plates
    fp1 = forceplates['forceplate_name'][0]
    fp2 = forceplates['forceplate_name'][1]

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

    ## Find Plate Corners, use first video file
    # Need a video where they aren't in blocks to get corners
    calibration_vid = cams['calibration_file'][0] + cams['extension'][0]

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

    #TODO this  needs to be saved to the camera table rather than the force plate table
    # Save plate corners to database
    for i in range(len(forceplates)):
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

        # Contact Intervals
        ci_f1 = FindContactIntervals((data_force_raw['Attila49 9286BA_Fz'] + data_force_raw['Ryan52 9286BA_Fz']), samp,
                                     thresh=16)

        # Crop Data
        data_force = {0: data_force_raw.filter(regex=fp1).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :],
                      1: data_force_raw.filter(regex=fp2).iloc[ci_f1['Start'][0]:ci_f1['End'][0], :]}

        # Pixel to meter ratios
        pix2m = pix2m_fromplate(plate_area, plate_dim)
        mag2pix = bw2pix(pix2m['x'], bw, bwpermeter=bwpermeter)

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