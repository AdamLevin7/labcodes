# Documentation- Kinematics 

## Table of Contents 


### [calc_segmentangle]
#### [calc_segmentangle](#function-calc_segmentangle)

End Table of Contents  <br/>


## Script: calc_segmentangle
### Function calc_segmentangle

### **Keywords:**
Segment, Angles, Deleva, Right, Horizontal


### **Syntax:**
```
from kinematics.calc_segmentangle import segangle

angles_seg = segangle(data_digi, segments)
                              
```
### **Description:**<br/>
Calculate angles for each body segment.

### Dependencies
* pandas  
* numpy  
 
### **Arguments:**

#### *Inputs*

   * **data:** DATAFRAME digitized data for each segment
        Column 0: time or frame number
        Column 1+: length of the segment
   * **segments:** DATAFRAME segment parameters obtained from segdim_deleva.py
   
#### *Outputs*

   * **dataout:** DATAFRAME angle of each segment (radians)
   
### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)    
