# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 19:26:10 2020

@author: cwiens
"""

import pandas as pd
import matplotlib.pyplot as plt
from animatevideos.animationgraph import linegraph

""" set parameters """
# original video file name
video_file = 'exampledata/191118_1004055.mp4'
# new animated video file name
filename = 'exampledata/191118_1004055_graphvid.mp4'
# load previously procesed data
graph_data = 'exampledata/data.csv'
# sampling rate of force data
samp_force = 1200
# sampling rate of video data
samp_vid = 120


""" set graph start frame:
    This is the frame number when the graph animation should start
"""
graph_start = 0


""" set sampling factor:
    This is the ratio of force sampling rate (or what ever is being plotted)
    and the video sampling rate
"""
samp_factor = int(samp_force / samp_vid)


""" plot data """
""" all the data came from a previously processed example
    you just need to do what is needed to plot your own data however you'd like
"""
# read in data
data_plot = pd.read_csv(graph_data)
# plot data
fig, ax1 = plt.subplots()
ax1.plot(data_plot['time'], data_plot['fz'], label='Vertical Reaction Force')
ax1.plot([data_plot['time'].iloc[0], data_plot['time'].iloc[-1]], [0, 0], 'k--')
ax1.set_ylim([-3000, 3000])
ax1.legend(loc='upper left')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Reaction Force (N)')
ax2 = ax1.twinx()
ax2.plot(data_plot['time'], data_plot['fz_vel'], 'green', label='CM Vertical Velocity')
ax2.legend(loc='upper right')
ax2.set_ylabel('CM Vertical Velocity (m/s)')


""" create animated graph video """
linegraph(filename, fig, ax1, data_plot['time'], video_file,
          graph_start=graph_start, samp_factor=samp_factor)
