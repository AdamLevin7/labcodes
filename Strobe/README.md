# Documentation- Strobe Motion

## Table of Contents 
| Description | Script |Functions |
| ------------- | ------------- | ------------- |
| Generates Strobe Image| [strobe.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Strobe/strobe.py) | [strobe_image](#function-strobe_image) |
| Identify frames for strobe | [strobe.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Strobe/strobe.py) | [strobe_findframes](#function-strobe_findframes) |

### End Table of Contents  <br/>


# Script-strobe
## Function strobe_findframes

[Link to strobe_findframes Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Strobe/strobe.py)

### **Keywords:**
strobe, findframe 

### **Syntax:**
```
from Strobe.strobe import strobe_findframes

strobeframes, searcharea = strobe_findframes(filename, crop='yes', autoid_thresh=None, autoid_num=None)

```

### **Dependencies:** 
* **findframe** USCBRL
* **pd:** pandas 
* **findarea** *capture_area* USCBRL
* **np:** numpy

### **Description:**<br/>
Allows user to identify which frames to use for strobe creation.<br/>
This uses the function 'findframe'.<br/>
* user can advance using the trackbar but must click button after to update <br/>
* **'k'** = -100 frames<br/>
* **'m'** = -10 frames<br/>
* **','** = -1 frame<br/>
* **'.'** = +1 frame<br/>
* **'/'** = +10 frames<br/>
* **';'** = +100 frames<br/>
* click **'q'** to select frame when identified in GUI<br/>
* click **'esc'** to exit out of GUI<br/>

### **Arguments:**

#### *Inputs*

   * **filename:** full path file name<br/>
   * **crop:** if 'yes' (default), user will identify area around the object of
        interest that could be used to limit noise in strobe image<br/>
   * **autoid_thresh:** OPTIONAL default: None, minimum number of frames between manually 
        identified strobe frames before auto id occurs (will find apex and two
        additional frames before and after apex)<br/>
   * **autoid_num:** OPTIONAL default None, number of frames to automatically find
        when autoid_thresh is triggered (ex: when two manual frames are spaced
                                         greater than autoid_thresh, it will find
                                         autoid_num of frames -including the
                                         original two frames- between the
                                         chosen frames)<br/>   
    
#### *Outputs*<br/>
   * **strobeframes:** Frames identified for strobe image <br/>
   * **searcharea:** Search region for strobe <br/> 

### **Examples:**

[Back to Table of Contents](#table-of-contents)


# Script-strobe
# Function strobe_image

[Link to strobe_image Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Strobe/strobe.py)

## Keywords:

Strobe, Image, Frames

## Syntax: 
```
from Strobe.strobe import strobe_image

strobe_image(filename, filesave, frames, searcharea=None, samp=240, thresh=60, bgint=5)
```

## Dependencies

* cv2
* numpy
* scipy ndimage


## Description 

Creates a strobe image. This will show an image with an subject in multiple places over time, allowing the user to see changes in subjects movement in one photo. 


## Arguments

*Inputs* 

1. **filename**: STRING full path file name
2. **filesave**: STRING full path file name that is to be saved as a jpeg
3. **frames**: SERIES list of strobe frames
4. **searcharea**: DICTIONARY list of searcha area for each strobe frame
    * key: frame number
    * value: search area from capture_area.py's 'find_area
5. **samp**: INT sampling rate of video
6. **thresh**: INT absolute difference threshold to find which pixels changed
7. **bgint**: INT number of frame difference from current image to use as subtraction image


*Outputs*

* Creates a jpeg image of combined multiple images and returns it to the location of filesave titled img_strobe


## Examples

Helpful examples :writing_hand:

[Back to Table of Contents](#table-of-contents)
