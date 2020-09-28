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
import cv2

class convertdata:
    
    def __init__(self, data, mag2pix, pix2m, view='fy', mode='ind',
                 plate_dim=(0.6, 0.4), platelocs=None, flip=None):
        # initialize variables
        self.data = data
        self.mag2pix = mag2pix
        self.pix2m = pix2m
        self.view = view
        self.mode = mode
        self.plate_dim = plate_dim
        self.platelocs = platelocs
        self.flip = flip
        
        
    def selectdata(self):
        # initialize data_fp
        self.data_fp = {}
        
        # loop through force plates
        for cntf in range(len(self.data)):
            if self.view == 'fx':
                # select Fx as video Fx | select Fz as video Fy
                fx = self.data[cntf].filter(regex='Fx', axis=1)
                fy = self.data[cntf].filter(regex='Fz', axis=1)
                # select Ax as video Ax | select Ay as video Ay
                ax = self.data[cntf].filter(regex='Ax', axis=1)
                ay = self.data[cntf].filter(regex='Ay', axis=1)
            elif self.view == 'fy':
                # select Fy as video Fx | select Fz as video Fy
                fx = self.data[cntf].filter(regex='Fy', axis=1)
                fy = self.data[cntf].filter(regex='Fz', axis=1)
                # select Ay as video Ax | select Ax as video Ay
                ax = self.data[cntf].filter(regex='Ay', axis=1)
                ay = self.data[cntf].filter(regex='Ax', axis=1)
            elif self.view == 'fxoh':
                # select Fx as video Fx | select Fy as video Fy
                fx = self.data[cntf].filter(regex='Fx', axis=1)
                fy = self.data[cntf].filter(regex='Fy', axis=1)
                # select Ax as video Ax | select Ay as video Ay
                ax = self.data[cntf].filter(regex='Ax', axis=1)
                ay = self.data[cntf].filter(regex='Ay', axis=1)
            elif self.view == 'fyoh':
                # select Fy as video Fx | select Fx as video Fy
                fx = self.data[cntf].filter(regex='Fy', axis=1)
                fy = self.data[cntf].filter(regex='Fx', axis=1)
                # select Ay as video Ax | select Ax as video Ay
                ax = self.data[cntf].filter(regex='Ay', axis=1)
                ay = self.data[cntf].filter(regex='Ax', axis=1)
            
            # assign to dataframe
            self.data_fp[cntf] = pd.DataFrame({'fx': fx.iloc[:,0],
                                               'fy': fy.iloc[:,0],
                                               'ax': ax.iloc[:,0],
                                               'ay': ay.iloc[:,0]})
    
    
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
    
    
    def flipdata(self):
        ### select data
        convertdata.selectdata(self)
        
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
    
    
    def datareform(self):
        
        # if mode is to keep plates individually
        if self.mode == 'ind':
            pass
        
        else:
            ### for fy and ax
            # calculate "moment" from image origin to force fy
            fp1_m_fy = -abs(self.data_fp[0]['fy']) * self.data_fp[0]['ax']
            fp2_m_fy = -abs(self.data_fp[1]['fy']) * self.data_fp[1]['ax']
            # sum fy force data from each plate
            fy = abs(self.data_fp[0]['fy']) + abs(self.data_fp[1]['fy'])
            # calculate location of centralized center of pressure
            # fp1_m_fy + fp2_m_fy + fy*ax = 0
            ax = (-fp1_m_fy - fp2_m_fy) / fy
            # convert fy back to reformated values
            fy = (self.data_fp[0]['fy']) + (self.data_fp[1]['fy'])
            
            ### for fx and ay
            # calculate "moment" from image origin to force fx
            fp1_m_fx = -abs(self.data_fp[0]['fx']) * self.data_fp[0]['ay']
            fp2_m_fx = -abs(self.data_fp[1]['fx']) * self.data_fp[1]['ay']
            # sum fx force data from each plate
            fx = abs(self.data_fp[0]['fx']) + abs(self.data_fp[1]['fx'])
            # calculate location of centralized center of pressure
            # fp1_m_fx + fp2_m_fx + fx*ay = 0
            ay = (-fp1_m_fx - fp2_m_fx) / fx
            # convert fy back to reformated values
            fx = (self.data_fp[0]['fx']) + (self.data_fp[1]['fx'])
            
            # combine data into single data frame
            self.data_fp = {}
            self.data_fp[0] = pd.DataFrame({'fx': fx,
                                            'fy': fy,
                                            'ax': ax,
                                            'ay': ay})
    
    
    def data2meter(self, flipy_cp='yes', file_vid=None, scale_y='yes'):
        ### select data
        convertdata.selectdata(self)
        ### find plate origin
        convertdata.plateorigin(self)
        ### flip data to video reference system
        convertdata.flipdata(self)
        
        """ scale ay to match video """
        if scale_y == 'yes':
            # find plate length in y in pixels
            y_pix = self.platelocs[0][1]['y'] - self.platelocs[0][0]['y']
            # find plate length in y in meters
            y_m = y_pix * self.pix2m['x']
            # calculate conversion
            y_m_conv = self.plate_dim[1] / y_m
            # loop through number of plates
            for cnt in range(len(self.data_fp)):
                # scale ay
                self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] / y_m_conv
        
        """ move center of pressure data to relative to plate origin """
        # loop through number of plates
        for cnt in range(len(self.data_fp)):
            # if plate_origin is not None, move cop data to it
            if self.plate_origin is not None:
                self.data_fp[cnt]['ax'] = self.data_fp[cnt]['ax'] + self.plate_origin[cnt][0] * self.pix2m['x']
                self.data_fp[cnt]['ay'] = self.data_fp[cnt]['ay'] + self.plate_origin[cnt][1] * self.pix2m['x']
        
        """ flip y-axis of center of pressure data """
        if flipy_cp == 'yes':
            # find height of image (max y value)
            cap = cv2.VideoCapture(file_vid)
            frame_height = int(cap.get(4))
            cap.release()
            for cnt in range(len(self.data_fp)):
                # subtract digitzed loction from frame height (only y columns)
                self.data_fp[cnt]['ay'] = (frame_height * self.pix2m['x']) - self.data_fp[cnt]['ay']
            
        
        ### reformat data
        convertdata.datareform(self)
    
    
    def data2pix(self):
        ### select data
        convertdata.selectdata(self)
        ### find plate origin
        convertdata.plateorigin(self)
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
        
        ### reformat data
        convertdata.datareform(self)
