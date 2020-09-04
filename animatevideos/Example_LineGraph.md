# Example Line Graph Video
## This file will provide the step by step process for using the functions in the labcodes repository to generate a video with data below it with a vertical line marking the time sync.

Example:
![LinegraphExample](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/GraphVid_Example.png)  
Figure: Example of vertical line overlayed on plotted data and synced with video.

## Process for Line Graph Videos

### Import Package and Modules
```
import pandas as pd
import matplotlib.pyplot as plt
from animatevideos.animationgraph import 
```

## Functions Used in this Code
[linegraph](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/Documentation_AnimateVids.md#function-linegraph)

### Set Parameters

The original video file name: 
```
video_file = 'exampledata/191118_1004055.mp4'
```

Output animated video:
```
filename = 'exampledata/191118_1004055_graphvid.mp4'
```

Load previously processed data
```
graph_data = 'exampledata/data.csv'
```
Sampling rate of the force data in Hz
```
samp_force = 1200
```

Sampling rate of the video in Hz
```
samp_vid = 120
```
Set video frame number when graph animation should start

```
graph_start = 0
```


### Set Sampling Factor
This is the ratio of the sampling rate of the data being plotted and the video sampling rate

```
samp_factor = int(samp_force / samp_vid)
```

### Plot Data
Plot the data that will be visualized in the video 

Read in the data
```
data_plot = pd.read_csv(graph_data)
```

Plot the data (This is an example plot, you will need to modify for your data)
```
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
```

### Create Animated Graph Video
Use the function _linegraph_ to create the video 

```
linegraph(filename, fig, ax1, data_plot['time'], video_file,
          graph_start=graph_start, samp_factor=samp_factor)
```

Functions Used in this Section  
[linegraph](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/Documentation_AnimateVids.md#function-linegraph)


