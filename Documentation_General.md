# Documentation- General Lab Codes

## Table of Contents 

### [Environment](https://github.com/USCBiomechanicsLab/labcodes/blob/master/uscbrl_env.yaml)  
* .yaml file

### [FindContactIntervals](#function-findcontactintervals)
### Import KDA Files 
* #### [HBIO408_BatchImportKDA](#function-HBIO408_BatchImportKDA)
* #### [importForce_KDA](#function-importForce_KDA)
### [ImportForce_TXT](#function-importforce_txt)
### Impulse_Velocity
* #### [imp_vel](#function-imp_vel)
### apdm_load
* #### [apdm_import](#function-apdm_import)
### capture_area
* #### [findarea](#function-findarea)
### dataconversion_digi
* #### [dltdv_import](#function-dltdv_import)
### dataconversion_force
* #### [convertdata](#function-convertdata)
### derivative
* #### [centraldiff](#function-centraldiff)
### [findframe](#function-findframe)
### [findplate](#function-findplate)
### findpoint
* #### [clickpoint](#function-clickpoint)
### pixelratios
* #### [pix2m_fromplate](#function-pix2m_fromplate)
* #### [bw2pix](#function-bw2pix)
### projectiletraj  
* #### [flighttraj](#function-flighttraj)

End Table of Contents  <br/>

## Script: apdm_load
### Function apdm_import
[Link to apdm_load Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/apdm_load.py)

### **Keywords:**
APDM, quaternion, acceleration, gyrocope, magnetometer

### **Syntax:**
```
from apdm_load import apdm_import

acc_df, gyro_df, mag_df, orient_df = apdm_import(filename)                              
```
### Dependencies 
* **pd:** pandas 
* **np:** numpy 
* **h5py:** h5py

### **Description:**<br/>
Import data from APDM sensor .h5 file to get the following dataframes
* Accelerometer
* Gyroscope 
* Magnetometer 
* Quaternion 
Uses the sampling rate of the sensors set at the time of collection.
   
### **Arguments:**

#### *Inputs*

   * **filename:** STR filename of the h5 file to be loaded

#### *Outputs*

   * **acc_df:** DATAFRAME accelerometer data from all sensors (x, y, z)
   * **gyro_df:** DATAFRAME gyroscope data from all sensors (x, y, z)
   * **mag_df:** DATAFRAME magnetometer data from all sensors (x, y, z)
   * **orient_df:** DATAFRAME quaternion data from all sensors (r, x, y, z)
        [real (scalar), x (complex), y (complex), z (complex)]
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)

## Script: importForce_KDA.m
### Function importForce_KDA
[Link to importForce_KDA Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/importForce_KDA.m)

### **Keywords:**
KDA, Import, B10, Force, Data, Files

### **Syntax:**
```
[ForceFile] = importForce_KDA('_000.KDA',6, 7206);                   
```
### Dependencies 
* MATLAB fxn, make sure it is in your working directory

### **Description:**<br/>
Import force data from a KDA file in B10.
   
### **Arguments:**

#### *Inputs*

   * **filename** Filename from KDA file
   * **gain** Gain of the amplifier
   * **startRow** INT First row for reading in .txt data
   * **endRow** Select KDA file (or multiple)

#### *Outputs*

   * **ForceFile:** DATAFRAME with force data and COP data

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)

## Script: HBIO408_BatchImportKDA.m
### Function HBIO408_BatchImportKDA
[Link to HBIO408_BatchImport Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/HBIO408_BatchImportKDA.m)

### **Keywords:**
KDA, Batch, Import, B10, Force, Data, Files

### **Syntax:**
```
Run the HBIO408_BatchImport_Code in MATLAB                      
```
### Dependencies 
* MATLAB fxn, make sure it is in your working directory

### **Description:**<br/>
Batch import force data from a KDA file in B10. Can do one or multiple files.
   
### **Arguments:**

#### *Inputs*

   * **Input** Select KDA file (or multiple)

#### *Outputs*

   * **.csv:** FILE with force data (FP1x, FP1y, FP1z, FP2x, FP2y, FP2z) and COP data
   * **.jpeg:** IMG force vs time curve to check against .avi overlay

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)

## Script: projectiletraj
### Function flighttraj
[Link to projectiletraj Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/projectiletraj.py)

### **Keywords:**
Projectile, Trajectory, Position, Flight, X, Y, Position

### **Syntax:**
```
from projectiletraj import flighttraj

pos = flighttraj(x_i, y_i, vx_i, vy_i, t_flight, samp)                              
```
### Dependencies 
* **pd:** pandas 
* **np:** numpy 

### **Description:**<br/>
Create data frame containing time, x, and y position of object during flight.
Uses equations of projectile motion.
   
### **Arguments:**

#### *Inputs*

   * **x_i:** FLOAT initial x position (m)
   * **y_i:** FLOAT initial y position (m)
   * **vx_i:** FLOAT initial x velocity (m/s)
   * **vy_i:** FLOAT initial y velocity (m/s)
   * **t_flight:** FLOAT flight time (s)
   * **samp:** FLOAT sampling rate of video (Hz)

#### *Outputs*

   * **pos:** DATAFRAME contains array of time, x, and y position during flight
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: derivative
### Function centraldiff
[Link to derivative Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/derivative.py)

### **Keywords:**
Derivative, Central Difference, CentralDiff, Signal, Derive

### **Syntax:**
```
from derivative import central_diff

d = central_diff(f, dt)                              
```
### Dependencies 
* **pd:** pandas 
* **np:** numpy 

### **Description:**<br/>
Uses the central difference method for all frames except the first and last
        frame. It uses the forward and backward difference method for the first
        and last frame, respectively.
   
### **Arguments:**

#### *Inputs*

   * **f:** DATAFRAME data signal to be derived
   * **dt:** FLOAT time step
   
#### *Outputs*

   * **d:** DATAFRAME derived data signal
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: Impulse_Velocity
### Function imp_vel
[Link to Impulse_Velocity Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Impulse_Velocity.py)

### **Keywords:**
Impulse, Velocity, Duration, Contact Interval

### **Syntax:**
```
from Impulse_Velocity import imp_vel

imp, velD = imp_vel(data, bw, samp)                              
```
### Dependencies 
* **pd:** pandas 

### **Description:**<br/>
Calculate impulse and change in velocity throughout duration.
   
### **Arguments:**

#### *Inputs*

   * **data:** DATAFRAME Mx3 dataframe of force data (includes X, Y, and Z !) 
   * **bw:** FLOAT participant's body weight in Newtons
   * **samp:** INT sampling rate of force plate (default: 1200)
   
#### *Outputs*

   * **imp:** DATAFRAME net impulse of X, Y, Z, and positive impulse Z (Ns)
   * **velD:** DATAFRAME change in velocity of X, Y, and Z (m/s)
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: capture_area
### Function findarea
[Link to capture_area Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/capture_area.py)

### **Keywords:**
Find, Area, Image, Box, Region, Select

### **Syntax:**
```
from capture_area import findarea

ref_point = findarea(video, label, frame)                              
```
### Dependencies 
* **cv2:** opencv 

### **Description:**<br/>
Outputs the area of the image that is selected.

Steps:
1) Click-drag over the area you want selected.
2) If area selection is good, press 'c' to view cropped image
    * If area selection is poor, press 'r' to recrop, and repeat Step 2 
       
 
### **Arguments:**

#### *Inputs*

   * **video:** STR full file name of video 
   * **label:** STR Label to be displayed in window (default='')
   * **frame**: INT frame number of the video to use a selection imgage (default=0)
   
#### *Outputs*

   * **ref_point:** LIST contains two tuple with x,y location of top-left and bottom-right
        location of the selected area
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)




## Script: findpoint
### Function clickpoint
[Link to findpoint Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/findpoint.py)

### **Keywords:**
Find, Point, Click, Double


### **Syntax:**
```
from findpoint import clickpoint

ix1, iy1 = clickpoint(file, label, framestart)                              
```
### Dependencies 
* **cv2:** opencv 
* **capture_area:** [USCBRL Function](#function-findarea) 

### **Description:**<br/>
Identifies x and y locations of mouse point that was double clicked.

Steps:  
1) Crop original image to zoom into plate(s) by click, hold and drag over area  
2) If cropped image is good, press 'c', then press 'esc' on next window  
   * If cropped image is not good, press 'r' with green box present, or 'o'  if new image is up    
3) Double-click the location(s) of interest. You may identify objects.   
       
 
### **Arguments:**

#### *Inputs*

   * **file:** STR full file name of video 
   * **label:** STR a label to be displayed in window (default='')
   * **framestart**: INT frame number to use as selection image (default=0)
   
#### *Outputs*

   * **cnt:** LIST x location of each double-click (pixels)
   * **key:** LIST y location of each double-click (pixels)
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: findframe
### Function findframe
[Link to findframe Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/findframe.py)

### **Keywords:**
Find, Frame, Sync, Video, Data


### **Syntax:**
```
from findframe import findframe

cnt, key = findframe(file, label, framestart)                            
```
### Dependencies 
* **cv2:** opencv 

### **Description:**<br/>
Exports frame number of last frame identified. User manually moves through video
    searching for frame of interest. When frame is found, click 'q' or 'esc' to exit.   

The following buttons shift the current frame by:  
    k : -100  
    m : -10  
    , : -1  
    . : +1  
    / : +10  
    ; : +100  
    
If the trackbar was manually moved, user must press a key before it will update.  
   
 
### **Arguments:**

#### *Inputs*

   * **file:** STR full file name of video 
   * **label:** STR text to be displayed in window (default: Find Frame)
   * **framestart**: INT start search at this frame (default: 0)
   
#### *Outputs*

   * **cnt:** INT frame number when video was closed
   * **key:** INT key identifier for last selected key
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)  


## Script: dataconversion_digi
### Function dltdv_import

### **Keywords:**
Digitize, Load, Data, DLTV, MATLAB, Body, Points


### **Syntax:**
```
from dataconversion_digi import dltdv_import

data_digi, frame_digi_start, frame_digi_end  = dltdv_import(file_digi, file_vid=file_video, flipy='yes')                              
```
### **Description:**<br/>
Module for importing digitized data from MATLAB DLTdv code created by group at UNC Chapel Hill.   
[DLTdv Website Link](http://biomech.web.unc.edu/dltdv/)
 
### **Arguments:**

#### *Inputs*

   * **file:** STRING full file path of digitized data using DLTdv 
   * **file_vid:** STRING full file path of digitized video 
   * **flipy**: STRING 'yes' to flip y-axis of digitized and center of mass data
   
#### *Outputs*

   * **data_digi:** DATAFRAME Digitized data in pandas dataframe
   * **frame_digi_start:** INT First frame where all data is non nan
   * **frame_digi_end:** INT Last frame where all data is not nan
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)  

  
   
## Script: data_conversion_force
### Function convertdata

### **Keywords:**


### **Syntax:**
```
from dataconversion_force import convertdata

transform_data = convertdata(data, mag2pix, pix2m, view = "fy",
                             mode= "ind",
                              platelocs =None, flip =None )                              
```
### **Description:**<br/>
Series of modules to transform force data into video reference system.  
Run 'main' function (convertdata) to use all modules
 
### **Arguments:**

#### *Inputs*

   * **data:** DATAFRAME force data read in from Bioware (preferred from ImportForce_TXT.py)
   * **mag2pix:** FLOAT64 magnitudeBW:pixel ratio obtained from bw2pix.py
   * **pix2m**: DICT pixel:meter ratio separated into x and y from pix2m_fromplate
   * **view**: STRING which dimension is parallel to image X (defalt='fy')  
  
![View Arg](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/View_ConvertData.png)<br/>
Figure: Examples of different "view" options which puts force data in video reference system.
   
   * **mode:** STRING keep plates separate or join into single vecotr (default='ind')  
![Mode Arg](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/Mode_ConvertData.png)<br/>
Figure: Examples of how forces can be combined or left separate.
   
   * **platelocs:** DICT plate corner locations obtained from findplate.py (default=None)   
   * **flip:** DICT Indicating how data should be flipped in video reference system
   
![Flip Arg](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/Flip_convertData.png)<br/>
Figure: The sections shows how to flip the force vector to match the **top left corner.**

   
#### *Outputs*

   * **data_out:** DICT force data in video reference system (fx, fy, ax, ay).
        Size dependent on number of plates/vectors.
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)     
     
## Script: pixelratios
### Function bw2pix

### **Keywords:**
Ratio, Pixel, Meter, Bodyweight, BW

### **Syntax:**
```
from pixelratios import bw2pix

mag2pix = bw2pix(pix2m, bw, bwpermeter=8)
```
### **Description:**<br/>
Calculate ratio of body weight to pixels in the video/image.

![bw2pix Example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/mag2pix_VectorChange.png)<br/>
Figure: Example of how adjusting bwpermeter argument changes force vector length

### **Arguments:**

#### *Inputs*

   * **pix2m:** FLOAT64 ratio of pixels:meter 
   * **bw:** FLOAT64 body weight of individual
   * **bwpermeter**: INT number of body weights in one meter (default=8)
   
#### *Outputs*

   * **mag2pix:** FLOAT64 ratio of bodyweight:pixel
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: pixelratios
### Function pix2m_fromplate

### **Keywords:**
Force, Plate, Ratio, Pixel, Meter

### **Syntax:**
```
from pixelratios import pix2m_fromplate

pix2m = pix2m_fromplate(plate_area, plate_dim)
```
### **Description:**<br/>
Use the force plate dimensions from function *findplate* which selects the 4 corners of a forceplate to determine the number of pixels in a meter in the horizontal and vertical directions.

![Pix2M Example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/pix2m_ratio.png)<br/>
Figure: Example pixel to meter ratio 

### **Arguments:**

#### *Inputs*

   * **plate_area:** DICT plate dimension in pixels (preferably from findplate.py)  
   * **plate_dim:** TUPLE dimension of plate in meters [(x, z) in image reference)]  
   
#### *Outputs*

   * **pix2m:** DICT ratio of pixels:meter
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: ImportForce_TXT
### Function ImportForce_TXT

### **Keywords:**
Import, Force, Text file, Bodyweight, BW, Sampling Rate, Rezero

### **Syntax:**
```
from ImportForce_TXT import ImportForce_TXT 

data, sample, weight = ImportForce_TXT(file, rezero=None) 
```
### **Description:**<br/>
Import force data from text file. <br/>
Bodyweight values and sampling rate of force plate can also be pulled from the text file.<br/>
Force data can be re-zeroed based on the beginning or end of trial. <br/>


### **Arguments:**

#### *Inputs*

   * **file:** STR file name (.txt) of force data<br/>
   * **rezero:** STR ability to rezero force data (default: None)<br/>
       * Options:
        * b - subtracted based on beginning 200 frames
        * e - subtracted based on ending 200 frames

#### *Outputs*<br/>
   * **data:** DATAFRAME force data with plate names and components<br/>

 Fix this
 ![Vector Overlay](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/ImportTXT_DataframeExample.PNG)<br/>
Figure 1: Example of "data" output dataframe<br/>

   * **samp:** FLOAT64 sampling rate of collection<br/>
   * **weight:** FLOAT64 weight (N) that was stored with collection (MAY OR MAY NOT BE ACTUAL WEIGHT OF INDIVIDUAL/SYSTEM - COULD BE FROM A PREVIOUS SESSION)<br/>

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: FindContactIntervals
### Function FindContactIntervals

### **Keywords:**
Contact, Intervals, Force, Threshold, Vertical 

### **Syntax:**
```
from FindContactIntervals import FindContactIntervals

CI = FindContactIntervals(data, samp=1200, thresh=50) 
```
### **Description:**<br/>
Finds the beginning and end of contact intervals when provided a single column vertical force data based on an input threshold.

### **Arguments:**

#### *Inputs*

   * **data:** Single column of vertical force data<br/> 
![DataFrame Input](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/CI_VertForce_DataframeExample.PNG)<br/>
Figure: Example "data" which should be the input argument to this function <br/>  
   
   * **thresh:** NUM force threshold in N to identify when contact occurs (default=50)


#### *Outputs*<br/>
   * **CI:** two column data frame. "Start" identifies beginning of contact  interval, while "End" identifies the end of interval. The number of rows signifies the number of contact intervals
   
![CI](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/CI_Output_DataframeExample.PNG)<br/>
Figure: Output dataframe with start and end of the contact intervals <br/>  

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)


## Script: findplate
### Function findplate

### **Keywords:**
Force, Plate, Identify, Corners, Find

### **Syntax:**
```
from findplate import findplate

plate = findplate(file, framestart=0, label='') 
```
### **Description:**<br/>
Identify 4 corners of a force plate(s) in an image.  

![DataFrame Input](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/findplate_platecorners.png)<br/>
Figure: Example of 2 force plates with corners selected in the CCW direction starting from top left <br/>  

#### Directions:
* Drag and select a large region including the force plates (green box)
* Press ESC if you are satisfied with the region selected
* Double click the corners of each FP in a **CCW direction starting at the TOP LEFT CORNER**
* Repeat for the second FP if necessary
* When satisfied press ESC to commit the coordinates of the plate

### **Arguments:**

#### *Inputs*

   * **file:** STRING file name of video<br/> 
   * **framestart:** INT frame number to use as selection image (default=0)<br/> 
   * **label:** STRING a label to be displayed in window (default='')
   
#### *Outputs*

   * **plate:** DICT containing 2x4 dataframe with rows x and y.<br/> 
    * Column order is dependent on the selection order
    * Size of DICT depends on the number of plates
   
![Output](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/FindPlates_Output_DictExample.PNG)<br/>
Figure: Output dictionary with the corners selected <br/>  

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)

