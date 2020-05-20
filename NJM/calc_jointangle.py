# -*- coding: utf-8 -*-
"""
calc_jointangle
    Calculate angle for each joint.
    
Inputs
    data: DATAFRAME digitized data for each landmark
        Column 0: time or frame number
        Column 1+: location of each digitized point
    segments: DATAFRAME segment parameters obtained from segdim_deleva.py
    
Outputs
    dataout: DATAFRAME angle of each joint (radians)
    
Dependencies
    pandas
    numpy
    
Created on Mon Apr 27 10:49:53 2020

@author: cwiens
"""

import pandas as pd
import numpy as np

def calc_angle(jointname, pt_a, pt_b, pt_c):
    # convert column names
    pt_a.columns = ['x', 'y']
    pt_b.columns = ['x', 'y']
    pt_c.columns = ['x', 'y']
    # find side b length
    side_b = np.sqrt(np.sum(np.square(pt_a - pt_c), axis=1))
    # find side c length
    side_c = np.sqrt(np.sum(np.square(pt_a - pt_b), axis=1))
    # find side a length
    side_a = np.sqrt(np.sum(np.square(pt_b - pt_c), axis=1))
    # calculate joint angle using cosine rule
    # cos(A) = (b^2 + c^2 - a^2) / (2*b*c)
    theta = np.arccos((np.square(side_b) + np.square(side_c) - np.square(side_a)) / (2*side_b*side_c))
    # store as dataframe
    joint_angle = pd.DataFrame({jointname: theta})
    
    
    return joint_angle



def jointangle(datain, segments):
    
    #%% create joint dictionary
    # create joint dict
    joints = pd.DataFrame(index={'neck', 'shoulder', 'elbow', 'wrist',
                                 'hip', 'knee', 'ankle'},
                          columns={'origin', 'other'},
                          dtype=str)
    
    # store origin
    joints['origin']['neck'] = 'head'
    joints['origin']['shoulder'] = 'trunk'
    joints['origin']['elbow'] = 'upperarm'
    joints['origin']['wrist'] = 'forearm'
    joints['origin']['hip'] = 'trunk'
    joints['origin']['knee'] = 'thigh'
    joints['origin']['ankle'] = 'shank'
    # store other
    joints['other']['neck'] = 'trunk'
    joints['other']['shoulder'] = 'upperarm'
    joints['other']['elbow'] = 'forearm'
    joints['other']['wrist'] = 'hand'
    joints['other']['hip'] = 'thigh'
    joints['other']['knee'] = 'shank'
    joints['other']['ankle'] = 'foot'
    
    
    #%% initialize data out
    dataout = pd.DataFrame(datain.iloc[:,0])
    
    #%% loop through joints
    for cnt in range(len(joints)):
        # if it is neck
        if (joints.iloc[cnt,:]).name == 'neck':
            # find point b (most proximal point)
            point_b = datain.filter(regex = segments.loc[joints['origin'][cnt]]['origin'])
            # find point c (most distal point)
            point_c = datain.filter(regex = segments.loc[joints['other'][cnt]]['other'])
            # find point a (joint intersection)
            point_a = datain.filter(regex = segments.loc[joints['origin'][cnt]]['other'])
            # if both hips were located, use average
            if len(point_c.columns) > 2:
                point_c = pd.DataFrame({'x': point_c.filter(regex='x').mean(axis = 1),
                                        'y': point_c.filter(regex='y').mean(axis = 1)})
            # calculate joint angle
            joint_ang = calc_angle((joints.iloc[cnt,:]).name,
                                   point_a, point_b, point_c)
            # add column to data out
            dataout = dataout.join(joint_ang)
            
        # if it is hip
        elif (joints.iloc[cnt,:]).name == 'hip':
            # find point b (most proximal point)
            point_b = datain.filter(regex = segments.loc[joints['origin'][cnt]]['origin'])
            # find point c (most distal point)
            point_c = datain.filter(regex = segments.loc[joints['other'][cnt]]['other'])
            # find point a (joint intersection)
            point_a = datain.filter(regex = segments.loc[joints['origin'][cnt]]['other'])
            # if both hips were located, use average
            if len(point_a.columns) > 2:
                # find if left and right joints were specified
                point_a_l = point_a.filter(regex = 'left')
                point_a_r = point_a.filter(regex = 'right')
                point_c_l = point_c.filter(regex = 'left')
                point_c_r = point_c.filter(regex = 'right')
            
            # if all point locations exist
            if ((len(point_b.columns)>0 and len(point_c.columns)>0) and
                (len(point_a.columns)>0)):
                # if left joint exists
                if len(point_a_l.columns)>0:
                    # calculate joint angle
                    joint_ang_l = calc_angle((joints.iloc[cnt,:]).name + '_left',
                                             point_a_l, point_b, point_c_l)
                    # add column to data out
                    dataout = dataout.join(joint_ang_l)
                # if right joint exists
                if len(point_a_r.columns)>0:
                    # calculate joint angle
                    joint_ang_r = calc_angle((joints.iloc[cnt,:]).name + '_right',
                                             point_a_r, point_b, point_c_r)
                    # add column to data out
                    dataout = dataout.join(joint_ang_r)
                # if neither left or right joints exists
                if (len(point_a_l.columns)==0) and (len(point_a_r.columns)==0):
                    # calculate joint angle
                    joint_ang = calc_angle((joints.iloc[cnt,:]).name,
                                           point_a, point_b, point_c)
                    # add column to data out
                    dataout = dataout.join(joint_ang)
            
        # if another joint
        else:
            # find point b (most proximal point)
            point_b = datain.filter(regex = segments.loc[joints['origin'][cnt]]['origin'])
            # find point c (most distal point)
            point_c = datain.filter(regex = segments.loc[joints['other'][cnt]]['other'])
            # find point a (joint intersection)
            point_a = datain.filter(regex = segments.loc[joints['origin'][cnt]]['other'])
            # find if location exists in digitized data set
            if ((len(point_a.columns) > 0) and (len(point_b.columns) > 0) and
                (len(point_c.columns) > 0)):
                # find if left and right joints were specified
                point_a_l = point_a.filter(regex = 'left')
                point_a_r = point_a.filter(regex = 'right')
                point_b_l = point_b.filter(regex = 'left')
                point_b_r = point_b.filter(regex = 'right')
                point_c_l = point_c.filter(regex = 'left')
                point_c_r = point_c.filter(regex = 'right')
                
                # if left joint exists
                if ((len(point_a_l.columns) > 0) and (len(point_b_l.columns) > 0) and
                    (len(point_c_l.columns) > 0)):
                    # calculate joint angle
                    joint_ang_l = calc_angle((joints.iloc[cnt,:]).name + '_left',
                                             point_a_l, point_b_l, point_c_l)
                    # add column to data out
                    dataout = dataout.join(joint_ang_l)
                # if right joint exists
                if ((len(point_a_r.columns) > 0) and (len(point_b_r.columns) > 0) and
                    (len(point_c_r.columns) > 0)):
                    # calculate joint angle
                    joint_ang_r = calc_angle((joints.iloc[cnt,:]).name + '_right',
                                             point_a_r, point_b_r, point_c_r)
                    # add column to data out
                    dataout = dataout.join(joint_ang_r)
                # if neither left or right joint exists
                if ((len(point_a_l.columns)==0) and (len(point_a_r.columns)==0) and
                    (len(point_b_l.columns)==0) and (len(point_b_r.columns)==0) and
                    (len(point_c_l.columns)==0) and (len(point_c_r.columns)==0)):
                    # calculate joint angle
                    joint_ang = calc_angle((joints.iloc[cnt,:]).name,
                                           point_a, point_b, point_c)
                    # add column to data out
                    dataout = dataout.join(joint_ang)
    
    
    return dataout