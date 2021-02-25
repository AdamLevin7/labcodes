# Documentation- Strobe Motion

## Table of Contents 
| Description | Script |Functions |
| ------------- | ------------- | ------------- |
| Generates a Strobe Image| strobe.py | [strobe_image](#function-strobe_image) |

### End Table of Contents  <br/>

# Script-strobe
# Function strobe_image

[Link to Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Strobe/strobe.py)

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
