# Documentation- General Lab Codes

## Table of Contents 

### Environment
Maybe have a section to explain how environment works
### FindContactIntervals
### [ImportForce_TXT - ImportForce_TXT](#importforce_txt)
### Impulse_Velocity
### capture_area
### dataconversion_digi
### data_conversion_force
### derivative
### findframe
### findplate
### findpoint
### pixelratios
### projectiletraj




## ImportForce_TXT

### _ImportForce_TXT_

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
 ![Vector Overlay](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/VectorOverlayExample.PNG)<br/>
Figure 1: Example of "data" output dataframe<br/>

   * **samp:** FLOAT64 sampling rate of collection<br/>
   * **weight:** FLOAT64 weight (N) that was stored with collection (MAY OR MAY NOT BE ACTUAL WEIGHT OF INDIVIDUAL/SYSTEM - COULD BE FROM A PREVIOUS SESSION)<br/>

### **Examples:**
Helpful examples
