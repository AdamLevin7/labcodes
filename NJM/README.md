# Documentation- Net Joint Moment Functions

## Table of Contents 

### dig2jointkinetics
* #### [main](#function-main dig2jointkinetics)
* #### [filtdata](#function-filtdata)
* #### [interpdatasig](#function-interpdatasig)
* #### [datainterp](#function-datainterp)
* #### [cm_angularimpulse](#function-cm_angularimpulse)
* #### [cm_velocityacceleration](#function-cm_velocityacceleration)
* #### [segmentangle_vel_acc](#function-segmentangle_vel_acc)
* #### [jointangle_vel](#function-jointangle_vel)
* #### [selectdata](#function-selectdata)

### jointkinetics
* #### [calcnjm](#function-calcnjm)
* #### [njm_full](#function-njm-full)

### power_work
* #### [power](#function-power)
* #### [work](#function-work)
* #### [main](#function-main power_work)

End Table of Contents  <br/>

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
