# -*- coding: utf-8 -*-
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

Created on Mon Apr 13 14:38:03 2020

@author: cwiens, Casey Wiens, cwiens32@gmail.com
"""


def bw2pix(pix2m, bw, bwpermeter=8):
    # newtons to pixels
    mag2pix = bw * bwpermeter * pix2m
    
    return mag2pix