# Documentation- Kinematics 

## Table of Contents 
| Description | Script |Functions |
| ------------- | ------------- | ------------- |
| Calc segment angles | calc_segmentangle | [calc_segmentangle](#function-calc_segmentangle) |
| Calculates angle for each joint| calc_jointangle | [jointangle](#function-jointangle) |
| Creates joint dictionary of the joint angles | calc_jointangle| [calc_angle](#function-calc_angle) |

### End Table of Contents  <br/>


# Function strobe_image

## Script: calc_jointangle
### Function jointangle

[Link to calc_jointangle](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/calc_jointangle.py)


## Keywords:

Joint, Angle, Dictionary

## Syntax: 

```
from kinematics.calc_jointangle import jointangle

segments = calc_angle(datain, segments)
```

## Dependencies

* Pandas
* numpy

## Description 

Calculates  all joint angles from the digitized data inputed and then puts it into a dictionary which can be selected from later. 

## Arguments

*Inputs* 

* **Datain**: DATAFRAME digitized data for each landmark
* **segments**: DATAFRAME segment parameters from [segdim_deleva.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/CalcCOM/segdim_deleva.py)

*Outputs*

* **dataout:** DATAFRAME that has angles for each joint: neck, shoudler, elbow, wrist, hip, knee, and ankle.

## Examples

[Back to Table of Contents](#table-of-contents)


## Script: calc_jointangle
### Function calc_angle

[Link to calc_jointangle](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/calc_jointangle.py)

## Keywords:

Joint, Angle

## Syntax:
```
 from kinematics.calc_jointangle import calc_angle
 
 joint_angle = calc_angle(jointname, pt_a, pt_b, pt_c)
```
## Dependencies

* Pandas
* numpy

## Description 
Calculates the joint angle from the digitized data inputed.

## Arguments

*Inputs* 

* **Jointname**: STRING of the joint name
* **segments**: DATAFRAME segment parameters from segdim_deleva.py
* **data**: DATAFRAME of digitized data for each landmark
    * Column 0 : time or frame number
    * Column 1+: location of each digitized point
* **pt_a**: joint location(x,y)
* **pt_b**: proximal joint of proximal segment(x,y)
* **pt_c**: distal joint of distal segment(x,y)

*Outputs*

* **joint_angle:** DATAFRAME returns dataframe joint angle

## Examples

[Back to Table of Contents](#table-of-contents)



## Script: calc_segmentangle
### Function calc_segmentangle

[Link to calc_segmentangle](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/calc_segmentangle.py)

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
