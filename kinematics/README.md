# Documentation- Kinematics 

## Table of Contents 
| Description | Script |Functions |
| ------------- | ------------- | ------------- |
| Calc segment angles | calc_segmentangle | [calc_segmentangle](#function-calc_segmentangle) |
| Calculates angle for each joint| calc_jointangle | [calc_jointangle](#function-calc_jointangle) |

### End Table of Contents  <br/>


## Script: calc_jointangle
### Function calc_jointangle

[Link to Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/calc_jointangle.py)

### **Keywords:**
Joint, Angle


### **Syntax:**
```
from kinematics.calc_jointangle import calc_angle

joint_angle = calc_angle(jointname, pt_a, pt_b, pt_c)                            
```
### **Description:**<br/>
Calculates the joint angle from the digitized data inputed.

### Dependencies
* pandas  
* numpy  
 
### **Arguments:**

#### *Inputs*

* **Jointname**: STRING of the joint name
* **segments**: DATAFRAME segment parameters from segdim_deleva.py
* **data**: DATAFRAME of digitized data for each landmark
    * Column 0 : time or frame number
    * Column 1+: location of each digitized point
* **pt_a**: joint location(x,y)
* **pt_b**: proximal joint of proximal segment(x,y)
* **pt_c**: distal joint of distal segment(x,y)
   
#### *Outputs*

   * **joint_angle:** DATAFRAME returns dataframe
   
### **Examples:**
Helpful examples

## Script: calc_segmentangle
### Function calc_segmentangle

[Link to Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/calc_segmentangle.py)

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
