# -*- coding: utf-8 -*-
"""
pixelratios
    Calculate ratios involving pixels
    
Modules:
    pix2m_fromplate: Calculate ratio pixels to meters using plate dimensions.
    forcemagpixel: Calculate ratio of body weight to pixels.
    
Dependencies:
    numpy

Created on Mon Apr 13 14:38:03 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""

import numpy as np

#%%
"""
pix2m_fromplate
    Calculate ratio pixels to meters using plate dimensions.
    
Input:
    plate_area: DICT plate dimension in pixels (preferably from findplate.py)
    plate_dim: TUPLE dimension of plate in meters [(x, z) in image reference)]
    
Output:
    pix2m: DICT ratio of pixels:meter
    
Dependencies:
    numpy
"""
def pix2m_fromplate(plate_area, plate_dim):
    pix2m = {'x': plate_dim[0] / np.mean([plate_area[0][3][0]-plate_area[0][0][0],
                                          plate_area[0][2][0]-plate_area[0][1][0]]),
             
             'z': plate_dim[1] / np.mean([plate_area[0][1][1]-plate_area[0][0][1],
                                          plate_area[0][2][1]-plate_area[0][3][1]])}
    
    return pix2m



#%%
"""
forcemagpixel
    Calculate ratio of body weight to pixels.
    
Input:
    pixel2m: FLOAT64 ratio of pixels:meter
    bw: FLOAT64 body weight of individual
    bwpermeter: INT number of body weights in one meter (default=8)
    
Output:
    mag2pix: FLOAT64 ratio of bodyweight:pixel
    
Dependencies:
    none
"""
def bw2pix(pix2m, bw, bwpermeter=8):
    # newtons to pixels
    mag2pix = bw * bwpermeter * pix2m
    
    return mag2pix