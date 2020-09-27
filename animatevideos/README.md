# Documentation- Animated Vieos

### [Line Graph Tutorial](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/Example_LineGraph.md)

## Table of Contents

### animationgraph
#### [linegraph](#function-linegraph)
### fbd_display
#### [fbd_vis](#function-fbd_vis)

End Table of Contents  

## Script: fbd_display
### Function fbd_vis

[FBD_Visual](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/fbd_example.py)  
Figure: Example of FBD and NJMs video over time.


### **Keywords:**
FBD, Display, Video, NJM, Curves, Instant, Segments, Lower Body

### **Syntax:**
```
from animatevideos.fbd_display import fbd_vis

fbd_obj = fbd_vis(data_force, data_digi, data_cm, data_njm, side, cnt)

fbd_obj.fbd_update()

fbd_obj.fbd_animate(filename='fbd_animate_example.mp4')                           
```
### **Description:**  
Create a visual displaying free body diagrams (FBDs) at an instance along with the 
the net joint moment (NJM) curves of the segment.  
Currently only for LOWER BODY.

### **Dependencies:**
* **pd:** pandas

### **Arguments:**

#### *Inputs*

   * **data_force:** DATAFRAME
            force data (fx, fy, ax, ay) (N, N, m, m).
   * **data_digi:** DATAFRAME
            digitized data (m).
   * **data_cm**: DATAFRAME
            center of mass data for segments and body (m).
            format matches that of NJM.dig2jointkinetics.dig2jk.main().
   * **data_njm**: DATAFRAME
            contains calculated variables for segment's joint kinetics.
   * **side**: STRING
            which side of the body. (ex. 'left')
   * **cnt:** INT, optional
            counter - index of data to be visualized.
            The default is None, but will be reset to the first index of data
     
#### *Outputs*

   * **No return but if module fbd_animate is used, a video will be created with the specified filename**
   
### **Examples:**
[Helpful_example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/fbd_example.py)  



[Back to Table of Contents](#table-of-contents) 


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
