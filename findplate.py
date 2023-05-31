# -*- coding: utf-8 -*-
"""
Script: findplate
    Find the coordinates of force plates used in a collection, then write them out to a logsheet or database
Modules
    findplate: Identifies the four corners of the plate(s) in the image.
    writeplate: Writes out the plate coordinates to a logsheet or database
    readplate: Read in the plate coordinates from a logsheet or database to findplate dictionary format

Author:
    Casey Wiens and Harper Stewart
    cwiens32@gmail.com, harperestewart7@gmail.com
"""


#%%
def findplate(file, framestart=0, label=''):
    """
    Function:::
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
        framestart: INT frame number to use as selection image (default=0)
        label: STRING a label to be displayed in window (default='')

    Output:
        plate: DICT containing 2x4 dataframe with rows x and y.
            Column order is dependent on the selection order.
            Size of DICT dependent on number of plates.

    Dependencies:
        cv2 (opencv)
        pandas
        capture_area

    Created on Thu Jan 2 15:10:57 2020

    @author: cwiens, Casey Wiens, cwiens32@gmail.com
    """
    # Dependencies
    import cv2
    import pandas as pd
    from capture_area import findarea


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
    cap.set(1,framestart)
    ret, imgO = cap.read()
    while(1):
        while plate_area is None:
            plate_area = findarea(file,label='Crop to area of force plate(s)')
        imgcrop = imgO[plate_area[0][1]:plate_area[1][1],
                       plate_area[0][0]:plate_area[1][0],
                       :]
        cv2.imshow('Press esc to exit, w to recrop',imgcrop)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        elif k == ord("w"):
            cv2.destroyAllWindows()
            plate_area = None
    cv2.destroyAllWindows()
            
    #%% find the corners of the plate
    label = 'Press "esc" when finished. Identify corners in counterclockwise starting with top left. ' + label
    cv2.namedWindow(label)
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

def write_plate(plate_area, path_logsheet = None, engine = None, camera_name = None, colID = None):
    """
    Function:::
    write_plate
        Writes out the plate coordinates to a logsheet or database

    Inputs:
        plate_area: DICT containing 2x4 dataframe with rows x and y.
            Column order is dependent on the selection order.
            Size of DICT dependent on number of plates.
        path_logsheet: STRING path to logsheet (default=None)
        engine: SQLalchemy engine (default=None)
        camera_name: STRING name of camera (default=None)

    Output:
        None

    Dependencies:
        pandas
        SQLalchemy
    """
    #TODO need to be able to loop through and add multiple cameras to the database

    # Dependencies
    import pandas as pd
    from sqlalchemy import create_engine

    #%% create dataframe# Merge dataframes in the dictionary
    # Loop can handle any number of force plates
    for i in range(len(plate_area)):
        if i == 0:
            df_plate_area = plate_area[i]
        else:
            df_plate_area = pd.concat([df_plate_area, plate_area[i]], axis=1)

    # Transpose the dataframe
    df_plate_area = df_plate_area.T

    # Make the index into a column called pt_number
    df_plate_area['pt_number'] = df_plate_area.index

    # Add the camera name to the dataframe as the first column
    df_plate_area.insert(0, 'camera_name', camera_name)


    #%% write to logsheet
    if path_logsheet != None:

        # Write the plate area information out to the logsheet
        with pd.ExcelWriter(path_logsheet, engine='openpyxl', mode='a',
                            if_sheet_exists='replace') as writer:
            df_plate_area.to_excel(writer, sheet_name='plate_area', index=False, startrow=0)

    #%% write information to database
    if engine != None:

        # Add the collection id to the dataframe
        df_plate_area.insert(0, 'collection_id', colID)

        # Delete the rows where the collection id already exists
        engine.execute('DELETE FROM plate_coordinates WHERE collection_id = ' + str(colID))

        # Write the plate area information out to the database
        df_plate_area.to_sql('plate_coordinates', engine, if_exists='append', index=False)


def read_plate(path_logsheet=None, engine=None, colID = None, camera_name = None):
    """

    Function:::
    read_plate
        Reads in the plate coordinates from a logsheet or database

    Inputs:
        path_logsheet: STRING path to logsheet (default=None)
        engine: SQLalchemy engine (default=None)
        colID: INT collection id (default=None)
        camera_name: STRING name of camera (default=None)

    Output:
        plate_area: DICT containing 2x4 dataframe with rows x and y.
            Column order is dependent on the selection order.
            Size of DICT dependent on number of plates.

    Dependencies:
        pandas
        SQLalchemy
    """
    # Dependencies
    import pandas as pd
    from sqlalchemy import create_engine

    #%% read in plate coordinates from logsheet
    if path_logsheet != None:
        # Read in the plate area information from the logsheet
        df_plate_area = pd.read_excel(path_logsheet, sheet_name='plate_area', index_col=None)

        # Filter the dataframe for the camera name
        df_plate_area = df_plate_area[df_plate_area['camera_name'] == camera_name]

        # Reset the index
        df_plate_area.reset_index(inplace=True, drop=True)

    #%% read in plate coordinates from database
    if engine != None:
        # Read in the plate area information from the database
        df_plate_area = pd.read_sql_query('SELECT * FROM plate_coordinates WHERE collection_id = ' + str(colID) + ' AND camera_name = "' + camera_name + '"', engine)

    # TODO need to convert the dataframe back into the dictionary shape

    # Transpose the dataframe only including x and y columns which become the row names
    # Filter down to the x and y columns
    df_plate_area = df_plate_area[['x', 'y']]

    df_plate_area = df_plate_area.T

    # Dictionary needs to have a dataframe for each set of 4 columns in the dataframe
    # Loop through the number of plates
    plate_area = {}
    for i in range(int(len(df_plate_area.columns)/4)):
        # Add the dataframe to the dictionary with x and y as the row names
        plate_area[i] = df_plate_area.iloc[:, (i*4):4*(i+1)]

    return plate_area








    plate_area = df_plate_area

    return p




