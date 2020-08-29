# Documentation- Vector Overlay Functions

## vectoroverlay: _vectoroverlay_

### **Keywords:**
Vector, Overlay, Force, Vector

### **Syntax:**

* from *VectorOverlay.vectoroverlay* import *vectoroverlay*

* *vectoroverlay*(file, file_out, data_vid, frame_con, vect_color='g', samp_force=1200, samp_video=240, dispthresh=60) 

### **Description:**<br/>
Add a colored vector to the video to represent the ground reaction force.

### **Arguments:**

#### *Inputs*

   * **file:** STRING file name of video<br/>
   * **file_out:** STRING file name for new video<br/>
   * **data_vid:** DICT force and cop data, prefer that output from data2pix.<br/>
      * format (0: {fx, fy, ax, ay}, 1: {fx, fy, ax, ay},...)<br/>
   * **frame_con:** LIST contact frame of video<br/>  
      * format [INT, INT, ...]<br/>   
   * **vect_color:** LIST color of vector<br/>   
      * format ['x', 'y', ...] for how many plates<br/>    
       * ex: FP1 as green and FP2 as blue: ['g', 'b']<br/>      
       * ex: both FPs as green: ['g', 'g']<br/>
   * **samp_video:** INT sampling rate of video<br/>
   * **samp_force:** INT sampling rate of force<br/>
   * **dispthresh:** INT display threshold, amount of force needed to display vector (unit=Newtons, default=60)
    
#### *Outputs*<br/>
* Creates a new video with force vector overlaid on the original video:

![Vector Overlay](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/VectorOverlayExample.PNG)<br/>
Figure 1: Example of Vector Overlay

### **Examples:**
Helpful examples

