# Documentation- Projectile Motion Functions

## Table of Contents 
| Description | Script |Functions |
| ------------- | ------------- | ------------- |
| Add visual representation of center of mass location and trajectory |[addcentermasstraj.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/projectilemotion/addcentermasstraj.py) | [addcmtraj](#function-addcmtraj) |
| Create data frame containing time, xy, and y position of object during flight|[projectiletraj.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/projectilemotion/projectiletraj.py)|[projectiletraj](#function-projectiletraj)|
| Create data frame containing time, xy, and y position of object during flight in pixels|[projectiletraj.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/projectilemotion/projectiletraj.py)|[flighttraj_pixels](#function-flighttraj_pixels)

### End Table of Contents  <br/>

# Script-addcentermasstraj
## Function addcmtraj

### **Keywords:**
Center of mass, trajectory

### **Syntax:**
```
from projectilemotion.addcentermasstraj import addcmtraj

 addcmtraj(file_vid, data, file_vid_n='cmtrajectoryvideo.mp4', samp_vid=120,
              data_max=None, data_min=None, olimage='yes')
```

### **Dependencies:** 
* **cv2** (opencv)
* **os:** 

### **Description:**<br/>
Add visual representation of center of mass location and trajectory.<br/>

#### *Inputs*

   * **file_vid:** STR full file name of video<br/>
   * **data:** DATAFRAME<br/>
	* **Column 0:** frame <br/>
	* **Column 1:** center of mass x location (pixels)<br/>
	* **Column 2:** center of mass y location (pixels)<br/>
   * **file_vid_n:** STR full file name of new video (default: cmtrajectoryvideo.mp4)<br/>
   * **samp_vid:** INT sampling rate of video (Hz) (default: 120)<br/>   
   * **data_max:** DATAFRAME display max range on video<br/>
	* **Column 0:** frame<br/>
	* **Column 1:** center of mass x location (pixels)<br/>
	* **Column 2:** center of mass y location (pixels)<br/>
   * **data_min:** DATAFRAME display min range on video<br/>
	* **Column 0:** frame<br/>
	* **Column 1:** center of mass x location (pixels)<br/>
	* **Column 2:** center of mass y location (pixels)<br/>
    
#### *Outputs*<br/>
video with body center of mass location and trajectory visually represented
image of each frame with body center of mass location and trajectory visually represented
location: 'SkeletonOL' folder within location of file_vid


### **Examples:**

[Back to Table of Contents](#table-of-contents)


# Script-projectiletraj
## Function projectiletraj

### **Keywords:**
dataframe, time, position, flight

### **Syntax:**
```
from projectilemotion.projectiletraj import flighttraj

pos = flighttraj(x_i, y_i, vx_i, vy_i, t_flight, samp)
```

### **Dependencies:** 
* **np:** numpy
* **pd:** pandas

### **Description:**<br/>
Create data frame containing time, x, and y position of object during flight.<br/>

#### *Inputs*

   * **x_i:** FLOAT initial x position (m)<br/>
   * **y_i:** FLOAT initial y position (m)<br/>
   * **vx_i:** FLOAT initial x velocity (m/s)<br/>
   * **vy_i:** FLOAT initial y velocity (m/s)<br/>	
   * **t_flight:** FLOAT flight time (s)<br/>
   * **samp:** FLOAT sampling rate of video (Hz)<br/>
	
    
#### *Outputs*<br/>
* **pos:** DATAFRAME contains array of time, x, and y position during flight<br/>

### **Examples:**

[Back to Table of Contents](#table-of-contents)


# Script-projectiletraj
## Function flighttraj_pixels

### **Keywords:**
dataframe, time, position, flight, pixels to meter

### **Syntax:**
```
from projectilemotion.projectiletraj import flighttraj_pixels

pos_pix, pos_pix_max, pos_pix_min = flighttraj_pixels(x_i, y_i, vx_i, vy_i, frame_start, frame_end, pix2m, samp, thresh=0.2, flip_x='no', flip_y='yes')
```
### **Dependencies:** 
* **np:** numpy
* **pd:** pandas

### **Description:**<br/>
Create data frame containing time, x, and y position of object during flight in pixels.<br/> 

#### *Inputs*

   * **x_i:** FLOAT initial x position (m)<br/>
   * **y_i:** FLOAT initial y position (m)<br/>
   * **vx_i:** FLOAT initial x velocity (m/s)<br/>
   * **vy_i:** FLOAT initial y velocity (m/s)<br/>
   * **frame_start:** 
   * **frame_end:**
   * **pix2m:** DICT ratio of pixels:meter
   * **samp:** FLOAT sampling rate of video (Hz)<br/>
   * **thresh:** FLOAT   
   * **flip_x:** STR Flip x direction on video  
   * **flip_y:** STR Flip y direciton on video  

#### *Outputs*<br/>
   * **pos_pix:** 
   * **pox_pix_max:**
   * **pos_pix_min:**


### **Examples:**

[Back to Table of Contents](#table-of-contents)
