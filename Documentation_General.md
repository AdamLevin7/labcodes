# Documentation- General Lab Codes

## Table of Contents 

### Environment
Maybe have a section to explain how environment works
### [FindContactIntervals](#function-findcontactintervals)
### [ImportForce_TXT](#function-importforce_txt)
### Impulse_Velocity
### capture_area
### dataconversion_digi
### data_conversion_force
#### [convertdata](#function-convertdata)
### derivative
### findframe
### [findplate](#function-findplate)
### findpoint
### pixelratios
#### [pix2m_fromplate](#function-pix2m_fromplate)
#### [bw2pix](#function-bw2pix)
### projectiletraj  

End Table of Contents  <br/>

  
   
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

![bw2pix Example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/pix2m_ratio.png)<br/>
Figure: 

### **Arguments:**

#### *Inputs*

   * **data:** DATAFRAME force data read in from Bioware (preferred from ImportForce_TXT.py)
   * **mag2pix:** FLOAT64 magnitudeBW:pixel ratio obtained from bw2pix.py
   * **pix2m**: DICT pixel:meter ratio separated into x and y from pix2m_fromplate
   * **view**: STRING which dimension is parallel to image X (defalt='fy')  
  
  Insert picture here
   
   * **mode:** STRING keep plates separate or join into single vecotr (default='ind')  
   Insert picture here
   
   * **platelocs:** DICT plate corner locations obtained from findplate.py (default=None)  
   
   Insert picture here
   
   * **flip:** DICT Indicating how data should be flipped in video reference system
   
   Insert picture here
   
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

![bw2pix Example](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/pix2m_ratio.png)<br/>
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

