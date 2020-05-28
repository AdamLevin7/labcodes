# -*- coding: utf-8 -*-
"""
data2pix

Series of modules to tranform force data into video reference system.
Run 'main' to use all modules.

Inputs:
    data: DATAFRAME force data read in from Bioware (preferred from ImportForce_TXT.py)
    mag2pix: FLOAT64 magnitudeBW:pixel ratio obtained from forcemagpixel.py
    pix2m: DICT pixel:meter ratio separated into x and y
    view: STRING which dimension is parallel to image X (defalt='fy')
    mode: STRING keep plates separate or join into single vecotr (default='ind')
    platelocs = DICT plate corner locations obtained from findplate.py (default=None)

Output:
    data_out: DICT force data in video reference system (fx, fy, ax, ay).
        Size dependent on number of plates/vectors.

Created on Mon Jan  6 09:02:02 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""
import pandas as pd
import numpy as np

def selectdata(data, view='fy'):
    # initialize variables
    fx = {}
    fy = {}
    ax = {}
    ay = {}
    # loop through force plates
    for cntf in range(len(data)):
        if view == 'fx':
            # select Fx as video Fx | select Fz as video Fy
            fx[cntf] = data[cntf].filter(regex='Fx', axis=1)
            fy[cntf] = data[cntf].filter(regex='Fz', axis=1)
            # select Ax as video Ax | select Ay as video Ay
            ax[cntf] = data[cntf].filter(regex='Ax', axis=1)
            ay[cntf] = data[cntf].filter(regex='Ay', axis=1)
        elif view == 'fy':
            # select Fy as video Fx | select Fz as video Fy
            fx[cntf] = data[cntf].filter(regex='Fy', axis=1)
            fy[cntf] = data[cntf].filter(regex='Fz', axis=1)
            # select Ay as video Ax | select Ax as video Ay
            ax[cntf] = data[cntf].filter(regex='Ay', axis=1)
            ay[cntf] = data[cntf].filter(regex='Ax', axis=1)
        elif view == 'fxoh':
            # select Fx as video Fx | select Fy as video Fy
            fx[cntf] = data[cntf].filter(regex='Fx', axis=1)
            fy[cntf] = data[cntf].filter(regex='Fy', axis=1)
            # select Ax as video Ax | select Ay as video Ay
            ax[cntf] = data[cntf].filter(regex='Ax', axis=1)
            ay[cntf] = data[cntf].filter(regex='Ay', axis=1)
        elif view == 'fyoh':
            # select Fy as video Fx | select Fx as video Fy
            fx[cntf] = data[cntf].filter(regex='Fy', axis=1)
            fy[cntf] = data[cntf].filter(regex='Fx', axis=1)
            # select Ay as video Ax | select Ax as video Ay
            ax[cntf] = data[cntf].filter(regex='Ay', axis=1)
            ay[cntf] = data[cntf].filter(regex='Ax', axis=1)
    
    return fx, fy, ax, ay


def plateorigin(platelocs):
    # initialize plate_origin
    plate_origin = {}
    # loop through number of plates
    for cnt in range(len(platelocs)):
        # find plate origin
        x = np.mean([platelocs[cnt].iloc[0,:]])
        y = np.mean([platelocs[cnt].iloc[1,:]])
        # combine data
        plate_origin[cnt] = (x,y)
    
    return plate_origin


def datareform(fx, fy, ax, ay, mode='ind', platelocs=None):
    # initialize data_fp
    data_fp = {}
    # if mode is to keep plates individually
    if mode == 'ind':
        # loop through plates
        for cnt in range(len(fx)):
            data_fp[cnt] = pd.DataFrame({'fx': fx[cnt].iloc[:,0],
                                         'fy': fy[cnt].iloc[:,0],
                                         'ax': ax[cnt].iloc[:,0],
                                         'ay': ay[cnt].iloc[:,0]})
    else:
        # combine force data and rename
        fx = pd.DataFrame({'fx': fx.sum(axis=1)})
        fy = pd.DataFrame({'fy': fx.sum(axis=1)})
        # need to figure out how to combine cop data into one signal
        
        
        # combine data into single data frame
        data_fp = fx.join(fy).join(ax).join(ay)
    
    return data_fp


def flipdata(data, flip=None):
    # if flip is not none
    if flip is not None:
        # loop through force plates
        for cnt in range(len(data)):
            if 'fx' in flip[cnt]:
                data[cnt]['fx'] = data[cnt]['fx'] * -1
            if 'fy' in flip[cnt]:
                data[cnt]['fy'] = data[cnt]['fy'] * -1
            if 'ax' in flip[cnt]:
                data[cnt]['ax'] = data[cnt]['ax'] * -1
            if 'ay' in flip[cnt]:
                data[cnt]['ay'] = data[cnt]['ay'] * -1
    
    return data


def data2meter(data, pix2m, plate_origin=None):
    # loop through number of plates
    for cnt in range(len(data)):
        # if plate_origin is not None, move cop data to it
        if plate_origin is not None:
            data[cnt]['ax'] = data[cnt]['ax'] + plate_origin[cnt][0] * pix2m['x']
            data[cnt]['ay'] = data[cnt]['ay'] + plate_origin[cnt][1] * pix2m['x']
    
    return data


def data2pix(data, mag2pix, pix2m, plate_origin=None):
    # loop through number of plates
    for cnt in range(len(data)):
        # convert force data to pixels
        data[cnt][['fx','fy']] = data[cnt][['fx','fy']] / mag2pix
        # convert cop data to pixels
        data[cnt]['ax'] = data[cnt]['ax'] / pix2m['x']
        data[cnt]['ay'] = data[cnt]['ay'] / pix2m['z']
        # if plate_origin is not None, move cop data to it
        if plate_origin is not None:
            data[cnt]['ax'] = data[cnt]['ax'] + plate_origin[cnt][0]
            data[cnt]['ay'] = data[cnt]['ay'] + plate_origin[cnt][1]
    
    return data


def transfrom2vidrefsys(data, pix2m, view='fy', mode='ind', platelocs=None, flip=None):
    # select data
    fx, fy, ax, ay = selectdata(data, view=view)
    # find plate origin
    plate_origin = plateorigin(platelocs)
    # reformat data
    data_n = datareform(fx, fy, ax, ay, mode=mode, platelocs=platelocs)
    # flip data to video reference system
    data_f = flipdata(data_n, flip)
    # convert to meters
    data_out = data2meter(data_f, pix2m, plate_origin)
    
    return data_out


def main(data, mag2pix, pix2m, view='fy', mode='ind', platelocs=None, flip=None):
    # select data
    fx, fy, ax, ay = selectdata(data, view=view)
    # find plate origin
    plate_origin = plateorigin(platelocs)
    # reformat data
    data_n = datareform(fx, fy, ax, ay, mode=mode, platelocs=platelocs)
    # flip data to video reference system
    data_f = flipdata(data_n, flip)
    # convert to pixel
    data_out = data2pix(data_f, mag2pix, pix2m, plate_origin)
    
    return data_out
