# Documentation- Animated Vieos

## Table of Contents

### [animationgraph]
#### [linegraph](#function-linegraph)

End Table of Contents  


## Script: animationgraph
### Function linegraph

![LineGraphEx](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/GraphVid_Example.png)  
Figure: Example of vertical line overlayed on plotted data and synced with video.


### **Keywords:**
Line, Graph, Animation, Data, Vertical Line, Time, Sync

### **Syntax:**
```
from animatevideos.animationgraph import linegraph

linegraph(filename, fig, ax1, data_plot['Time'], video_file,
          graph_start=graph_start, samp_factor=samp_factor)
                              
```
### **Description:**  
Combine a video and a (line) graph into an animated video.
Vertical line will move across the graph in sync with the video data.
 
### **Arguments:**

#### *Inputs*

   * **filename:** STRING file name of output video
   * **fig:** FIGURE matplotlib figure object of graph
        ex.) fig, ax = plt.subplots()
   * **ax**: AxesSubplot matplotlib axes object of the graph
        ex.) fig, ax = plt.subplots()
   * **xind**: ARRAY indices of x-axis for line animation advancement 
        ex.) This would be the "time" array if the x-axis is time
   * **video_file:** STRING file name of original input video
   * **graph_start**: INT (default: 0) the VIDEO frame number where the graph animation should begin
   * **samp_factor**: INT (default: 10) the factor of plot signal sampling rate to the video sampling rate
        ex.) 1200 / 120 = 10  -> samp_force / samp_video = samp_factor
           
#### *Outputs*

   * **An mp4 file will be created with the name of the input 'filename'**
   
### **Examples:**
[Helpful example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/linegraph_example.py)

[Back to Table of Contents](#table-of-contents) 
