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
### derivative
### findframe
### [findplate](#function-findplate)
### findpoint
### pixelratios
### projectiletraj





## Script: ImportForce_TXT
### Function ImportForce_TXT

### **Keywords:**
Import, Force, Text file, Bodyweight, BW, Sampling Rate, Rezero

### **Syntax:**

* from *ImportForce_TXT* import *ImportForce_TXT *

* data, sample, weight = *ImportForce_TXT*(file, rezero=None) 

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

* from *FindContactIntervals* import *FindContactIntervals*

* CI = *FindContactIntervals*(data, samp=1200, thresh=50) 

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

* from *findplate* import *findplate*

* plate = *findplate*(file, framestart=0, label='') 

### **Description:**<br/>
Identify 4 corners of a force plate(s) in an image.<br/>

![DataFrame Input](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/FindPlates_CornersExample.PNG)<br/>
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

