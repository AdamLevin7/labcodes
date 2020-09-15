# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 10:55:44 2020

@author: cwiens
"""

from animatevideos.fbd_display import fbd_vis
import pandas as pd

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


""" set side:
    This is the side of the body in which the joint kinetics were calculated
"""
side = 'left'

""" set cnt (counter):
    This is the index of the data in which you'd like to display
"""
cnt = 4326 

"""
create object
"""
fbd_obj = fbd_vis(data_force, data_digi, data_cm, data_njm, side, cnt)

"""
if creating visual at one instant...
(you will need to manually save image if that is what is wanted)
"""
fbd_obj.fbd_update()

"""
if create full animation video...
"""
fbd_obj.fbd_animate(filename='fbd_animate_example.mp4')
