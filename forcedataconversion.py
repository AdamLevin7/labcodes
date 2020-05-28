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

class convertdata:
    
    def __init__(self, data, mag2pix, pix2m, view='fy', mode='ind',
                 platelocs=None, flip=None):
        # initialize variables
        self.data = data
        self.mag2pix = mag2pix
        self.pix2m = pix2m
        self.view = view
        self.mode = mode
        self.platelocs = platelocs
        self.flip = flip
        
        
    def selectdata(self):
        # initialize variables
        self.fx = {}
        self.fy = {}
        self.ax = {}
        self.ay = {}
        # loop through force plates
        for cntf in range(len(self.data)):
            if self.view == 'fx':
                # select Fx as video Fx | select Fz as video Fy
                self.fx[cntf] = self.data[cntf].filter(regex='Fx', axis=1)
                self.fy[cntf] = self.data[cntf].filter(regex='Fz', axis=1)
                # select Ax as video Ax | select Ay as video Ay
                self.ax[cntf] = self.data[cntf].filter(regex='Ax', axis=1)
                self.ay[cntf] = self.data[cntf].filter(regex='Ay', axis=1)
            elif self.view == 'fy':
                # select Fy as video Fx | select Fz as video Fy
                self.fx[cntf] = self.data[cntf].filter(regex='Fy', axis=1)
                self.fy[cntf] = self.data[cntf].filter(regex='Fz', axis=1)
                # select Ay as video Ax | select Ax as video Ay
                self.ax[cntf] = self.data[cntf].filter(regex='Ay', axis=1)
                self.ay[cntf] = self.data[cntf].filter(regex='Ax', axis=1)
            elif self.view == 'fxoh':
                # select Fx as video Fx | select Fy as video Fy
                self.fx[cntf] = self.data[cntf].filter(regex='Fx', axis=1)
                self.fy[cntf] = self.data[cntf].filter(regex='Fy', axis=1)
                # select Ax as video Ax | select Ay as video Ay
                self.ax[cntf] = self.data[cntf].filter(regex='Ax', axis=1)
                self.ay[cntf] = self.data[cntf].filter(regex='Ay', axis=1)
            elif self.view == 'fyoh':
                # select Fy as video Fx | select Fx as video Fy
                self.fx[cntf] = self.data[cntf].filter(regex='Fy', axis=1)
                self.fy[cntf] = self.data[cntf].filter(regex='Fx', axis=1)
                # select Ay as video Ax | select Ax as video Ay
                self.ax[cntf] = self.data[cntf].filter(regex='Ay', axis=1)
                self.ay[cntf] = self.data[cntf].filter(regex='Ax', axis=1)
    
    
    def plateorigin(self):
        # initialize plate_origin
        self.plate_origin = {}
        # loop through number of plates
        for cnt in range(len(self.platelocs)):
            # find plate origin
            x = np.mean([self.platelocs[cnt].iloc[0,:]])
            y = np.mean([self.platelocs[cnt].iloc[1,:]])
            # combine data
            self.plate_origin[cnt] = (x,y)
    
    
    def datareform(self):
        ### select data
        convertdata.selectdata(self)
        
        # initialize data_fp
        self.data_fp = {}
        # if mode is to keep plates individually
        if self.mode == 'ind':
            # loop through plates
            for cnt in range(len(self.fx)):
                self.data_fp[cnt] = pd.DataFrame({'fx': self.fx[cnt].iloc[:,0],
                                                  'fy': self.fy[cnt].iloc[:,0],
                                                  'ax': self.ax[cnt].iloc[:,0],
                                                  'ay': self.ay[cnt].iloc[:,0]})
        else:
            # combine force data and rename
            fx = pd.DataFrame({'fx': self.fx.sum(axis=1)})
            fy = pd.DataFrame({'fy': self.fx.sum(axis=1)})
            # need to figure out how to combine cop data into one signal!!!!
            
            
            # combine data into single data frame
            self.data_fp = fx.join(fy).join(ax).join(ay)
    
    
    def flipdata(self):
        ### select data
        convertdata.selectdata(self)
        ### reformat data
        convertdata.datareform(self)
        
        # if flip is not none
        if self.flip is not None:
            # loop through force plates
            for cnt in range(len(self.data)):
                if 'fx' in self.flip[cnt]:
                    self.data_fp[cnt]['fx'] = self.data_fp[cnt]['fx'] * -1
                if 'fy' in self.flip[cnt]:
                    self.data_fp[cnt]['fy'] = self.data_fp[cnt]['fy'] * -1
                if 'ax' in self.flip[cnt]:
                    self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] * -1
                if 'ay' in self.flip[cnt]:
                    self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] * -1
    
    
    def data2meter(self):
        ### select data
        convertdata.selectdata(self)
        ### find plate origin
        convertdata.plateorigin(self)
        ### reformat data
        convertdata.datareform(self)
        ### flip data to video reference system
        convertdata.flipdata(self)
        
        # loop through number of plates
        for cnt in range(len(self.data_fp)):
            # if plate_origin is not None, move cop data to it
            if self.plate_origin is not None:
                self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] + self.plate_origin[cnt][0] * self.pix2m['x']
                self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] + self.plate_origin[cnt][1] * self.pix2m['x']
    
    
    def data2pix(self):
        ### select data
        convertdata.selectdata(self)
        ### find plate origin
        convertdata.plateorigin(self)
        ### reformat data
        convertdata.datareform(self)
        ### flip data to video reference system
        convertdata.flipdata(self)
        
        # loop through number of plates
        for cnt in range(len(self.data_fp)):
            # convert force data to pixels
            self.data_fp[cnt][['fx','fy']] = self.data_fp[cnt][['fx','fy']] / self.mag2pix
            # convert cop data to pixels
            self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] / self.pix2m['x']
            self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] / self.pix2m['z']
            # if plate_origin is not None, move cop data to it
            if self.plate_origin is not None:
                self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] + self.plate_origin[cnt][0]
                self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] + self.plate_origin[cnt][1]