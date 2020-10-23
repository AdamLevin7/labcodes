# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 10:55:44 2020

@author: cwiens
"""

from animatevideos.fbd_display import fbd_vis
import pandas as pd
from NJM.jointkinetics import convert_to_flexext_ref

""" all the data came from a previously processed example
    currently, it is assuming you are in the animatevideos folder. if you are
    not, then you must change directory or edit data_file path
"""
data_file = 'exampledata/data_fbd.xlsx'
# read in data
data_force = pd.read_excel(data_file, sheet_name='data_force', index_col=0)
data_digi = pd.read_excel(data_file, sheet_name='data_digi', index_col=0)
data_cm = pd.read_excel(data_file, sheet_name='data_cm', index_col=0)
data_njm = pd.read_excel(data_file, sheet_name='data_njm', index_col=0)


""" set anterior
    This is the direction the individual is facing
    It is used to set positive/negative values to extensor/flexor moments
"""
anterior = 'left'

""" convert NJM data to flexor/extensor references 
    This makes extensor moments positive and flexor moments negative
"""
data_njm_update = convert_to_flexext_ref(data_njm, anterior=anterior)

""" set side:
    This is the side of the body in which the joint kinetics were calculated
"""
side = 'left'

""" set cnt (counter):
    This is the index of the data in which you'd like to display
"""
cnt = 4326

""" set colorlegend (what does the color scheme represent):
    This is what will be displayed in the legend, describing what a positive/negative moment means
    'flexext' would say Extensor = positive and Flexor = negative
    'posneg' would say Positive = positive (CCW) and Negative = negative (CW)
"""
colorlegend = 'flexext'

"""
create object
"""
fbd_obj = fbd_vis(data_force, data_digi, data_cm, data_njm_update, side, cnt, colorlegend=colorlegend)

"""
if creating visual at one instant...
(you will need to manually save image if that is what is wanted)
"""
fbd_obj.fbd_update()
# change to diferent time
fbd_obj.cnt = 4423
fbd_obj.fbd_update()

"""
if create full animation video...
"""
fbd_obj.fbd_animate(filename='fbd_animate_example.mp4')
