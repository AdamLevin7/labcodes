## Documentation- Vector Overlay Functions

# vectoroverlay: _vectoroverlay_

**Keywords:**
Vector, Overlay, Force, Vector

**Syntax:**

from *VectorOverlay.vectoroverlay* import *vectoroverlay*

*vectoroverlay*(file, file_out, data_vid, frame_con, vect_color='g', samp_force=1200, samp_video=240, dispthresh=60) 

**Description:**
Add a colored vector to the video to represent the ground reaction force.

**Arguments:**

*Inputs*

   * **file:** STRING file name of video\
   * **file_out:** STRING file name for new video\
   * **data_vid:** DICT force and cop data, prefer that output from data2pix.\
      * format (0: {fx, fy, ax, ay}, 1: {fx, fy, ax, ay},...)\
   * **frame_con:** LIST contact frame of video\    
      * format [INT, INT, ...]\    
   * **vect_color:** LIST color of vector\   
      * format ['x', 'y', ...] for how many plates\      
       * ex: FP1 as green and FP2 as blue: ['g', 'b']\       
       * ex: both FPs as green: ['g', 'g']\
   * **samp_video:** INT sampling rate of video\
   * **samp_force:** INT sampling rate of force
   * **dispthresh:** INT display threshold, amount of force needed to display vector (unit=Newtons, default=60)
    
*Outputs*
* Creates vector overlay video

![Test Image](https://github.com/USCBiomechanicsLab/labcodes/blob/README-Documentation/DocMaterials/PSYC501_HW2_Density_Stewart_Rev02.jpeg)

**Examples:**
Helpful examples

