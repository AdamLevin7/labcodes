"""
Script: jointkinetics
    Calculate variables for joint kinetics.

Modules
    calcnjm: actual joint kinetic calculations for a single segment
    njm_full: run calcnjm for muliple segments
    convert_to_flexext_ref: Convert reference system to flexion/extension

Author:
    Casey Wiens
    cwiens32@gmail.com
"""


def calcnjm(segname, m, ax, ay, Rxd, Ryd, r_d, r_p, Icm, alpha, njm_d):
    """
    Function::: calcnjm
    	Description: actual joint kinetic calculations for a single segment
    	Details:

    Inputs
        segname: STR segment name
        m: FLOAT segment mass (kg)
        ax: DATAFRAME or FLOAT segmental horizontal acceleration (m/s^2)
        ay: DATAFRAME or FLOAT segmental vertical acceleration (m/s^2)
        Rxd: DATAFRAME or FLOAT distal horizontal force (N)
        Ryd: DATAFRAME or FLOAT distal vertical force (N)
        r_d: DATAFRAME or FLOAT distance from distal force to segment center of mass (x, y) (m)
        r_p: DATAFRAME or FLOAT distance from proximal force to segment center of mass (x, y) (m)
        I_cm: DATAFRAME or FLOAT segment moment of inertia (kg*m^2)
        alpha: DATAFRAME or FLOAT segment angular velocity (rad/s^2)
        njm_d: DATAFRAME or FLOAT distal net joint moment (N*m)

    Outputs
        dataout: DATAFRAME contains calculated variables for segment's joint kinetics
        njm_p: DATAFRAME or FLOAT proximal net joint moment (N*m)
        Rxp: DATAFRAME or FLOAT proximal horizontal net joint force (N)
        Ryp: DATAFRAME or FLOAT proximal vertical net joint force (N)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    # Dependencies
    import numpy as np
    import pandas as pd

    #%% gravity
    g = -9.81
    
    #%% proxial net joint forces
    ### horizontal
    # Fx = max
    # Rxp + Rxd = max
    # Rxp = max - Rxd
    Rxp = m*ax - Rxd
    
    ### vertical
    # Fy = may
    # Ryp + Ryd + mg = may
    # Ryp = may - Ryd - mg
    Ryp = m*ay - Ryd - m*g
    
    #%% proximal-distal net joint moments
    # distal moment
    m_d = np.cross(r_d, np.stack((Rxd, Ryd), axis=1))
    # proximal moment
    m_p = np.cross(r_p, np.stack((Rxp, Ryp), axis=1))
    
    #%% calculate net joint moment
    # M = Icma
    # M1 + M2 + M3 + M4 = Icma
    # M1 = Icma - M2 - M3 - M4
    njm_p = Icm * alpha - m_p - m_d - njm_d
    
    #%% store as dataframe
    dataout = pd.DataFrame({'rxd': Rxd,
                            'ryd': Ryd,
                            'rxp': Rxp,
                            'ryp': Ryp,
                            'max': m*ax,
                            'may': m*ay,
                            'icm': Icm,
                            'alpha': alpha,
                            'md': m_d,
                            'mp': m_p,
                            'njmd': njm_d,
                            'njmp': njm_p})
    # add segment name to begining of each column
    dataout.columns = [segname + '_' + str(col) for col in dataout.columns]
    
    
    return dataout, njm_p, Rxp, Ryp


def njm_full(dig, cm, cm_acc, icm, segang_acc, forcedata, mass, seg_sequence, segments):
    """
    Function::: njm_full
    	Description: set up data to run calcnjm for muliple segments
    	Details:

    Inputs
        dig: DATAFRAME digitized end-point data (x,y) (m)
        cm: DATAFRAME segment(s) center of mass position (x,y) (m)
        cm_acc: DATAFRAME segment(s) center of mass acceleration (x,y) (m/s^2)
        icm: DATAFRAME segment(s) moment of inertia (kg*m^2)
        segang_acc: DATAFRAME segment(s) angular acceleration (rad/s^2)
        forcedata: DATAFRAME force data (fx, fy, ax, ay) (N, N, m, m)
        mass: FLOAT mass of indiviudal/system (kg)
        seg_sequence: LIST ordered list of segments to calculate joint kinetics
        segments: DATAFRAME segment parameters obtained from segdim_deleva.py

    Outputs
        data_njm: DATAFRAME contains calculated variables for segment(s)'s joint kinetics

    Dependencies
        pandas
    """
    # Dependencies
    import pandas as pd

    # initialize data out
    dataout = pd.DataFrame(dig.iloc[:,0])
    
    for cnt in range(len(seg_sequence)):
        #%% set parameters
        # mass of segment
        m = mass * segments['massper'][segments.index == seg_sequence[cnt]].values
        # horizontal acceleration of segment
        ax = cm_acc.filter(regex = seg_sequence[cnt]).filter(regex = 'x').iloc[:,0].values
        # vertical acceleration of segment
        ay = cm_acc.filter(regex = seg_sequence[cnt]).filter(regex = 'y').iloc[:,0].values
        # segment center of mass location
        seg_cm_loc = cm.filter(regex = seg_sequence[cnt]).values
        # proximal joint location
        joint_p_loc = dig.filter(regex = segments['joint_p'][seg_sequence[cnt]]).values
        # center of mass inertia
        Icm = icm.filter(regex = seg_sequence[cnt]).iloc[:,0].values
        # segment angular rotation
        alpha = segang_acc.filter(regex = seg_sequence[cnt]).iloc[:,0].values
        
        # if it is first segment
        if cnt == 0:
            #%% set parameters
            # distal horizontal reaction force
            Rxd = forcedata['fx'].values
            # distal vertical reaction force
            Ryd = forcedata['fy'].values
            # distal joint/center of pressure location
            joint_d_loc = forcedata[['ax','ay']].values
            # distal net joint moment
            njm_d = 0
        else:
            #%% set parameters
            # distal horizontal net joint force (flip it)
            Rxd = -njf_x
            # distal vertical net joint force (flip it)
            Ryd = -njf_y
            # distal joint/center of pressure location
            joint_d_loc = dig.filter(regex = segments['joint_d'][seg_sequence[cnt]]).values
            # distal net joint moment (flip it)
            njm_d = -njm_dj
        
        #%% find r (perpendicular distances)
        # distance from center of pressure to center of mass
        r_d = joint_d_loc - seg_cm_loc
        # distance from joint to center of mass
        r_p = joint_p_loc - seg_cm_loc
        
        #%% calculate njm and other variables
        data_njm, njm_dj, njf_x, njf_y = calcnjm(seg_sequence[cnt], m, ax, ay,
                                                 Rxd, Ryd, r_d, r_p,
                                                 Icm, alpha, njm_d)
        # join with new dataframe
        dataout = dataout.join(data_njm.set_index(dataout.index))
    
    return dataout


def convert_to_flexext_ref(data_in, anterior='right'):
    """
    Function::: convert_to_flexext_ref
    	Description: Convert reference system to flexion extension for NJMs
    	Details:

    Inputs
        data_in : DATAFRAME
            contains calculated variables for segment's joint kinetics.
            THIS ASSUMES THE NJM CALCULATIONS WERE IN THE REFERENCE SYSTEM WHERE CCW IS POSITIVE
        anterior : STRING, optional (default: 'right')
            Which direction is anterior for the individual?
            This sets how positive/negative values will be determined as flexor or extensor moments.
            Possible inputs:
                'right': individual is facing right in the current reference system
                'left': individual is facing left in the current reference system

    Outputs
        dataout : DATAFRAME contains reorientated calculated variables for segment's joint kinetics.

    Dependencies
        None

    """

    """ set copy """
    dataout = data_in.copy()

    """ set extensors as positive and flexors as negative for given direction """
    ## if individual is facing right
    if anterior is 'right':
        dataout.foot_md = dataout.foot_md * -1
        dataout.foot_njmd = dataout.foot_njmd * -1
        dataout.foot_mp = dataout.foot_mp * -1
        dataout.foot_njmp = dataout.foot_njmp * -1
        dataout.thigh_md = dataout.thigh_md * -1
        dataout.thigh_njmd = dataout.thigh_njmd * -1
        dataout.thigh_mp = dataout.thigh_mp * -1
        dataout.thigh_njmp = dataout.thigh_njmp * -1

    ## if individual is facing left
    elif anterior is 'left':
        dataout.shank_md = dataout.shank_md * -1
        dataout.shank_njmd = dataout.shank_njmd * -1
        dataout.shank_mp = dataout.shank_mp * -1
        dataout.shank_njmp = dataout.shank_njmp * -1

    return dataout