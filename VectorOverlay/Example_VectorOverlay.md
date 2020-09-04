# Example Vector Overlay
## This file will provide the step by step process for using the functions in the labcodes repository to generate a vector overlay.


For a video that walks you through creating a vector overlay for the PAC12 Steady State Running 
[Click Here](https://drive.google.com/drive/folders/1bKA8pVp695KqJMAeGPvVXo6gOT0loFao)

## Process for Vector Overlay: Basketball Jump Shot Example

### Import Package and Modules
```
import os
from ImportForce_TXT import ImportForce_TXT
from FindContactIntervals import FindContactIntervals
from findplate import findplate
from pixelratios import pix2m_fromplate, bw2pix
from dataconversion_force import convertdata
from VectorOverlay.vectoroverlay import vectoroverlay
```
## Functions Used in this Code
[ImportForce_TXT](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_txt)


### Set Path (MODIFY for your project)<br/>
This is the path on your computer where the video and corresponding force file will be stored.<br/>
Note: In Python, "r" stands for "raw" so it causes backslashes to be interpreted as actual backslashes instead of special characters

```
path_force = r'F:\USC Biomechanics Research\HBIO 408\Tasks\Baskball- Jump Shot\Force'
path_video = r'F:\USC Biomechanics Research\HBIO 408\Tasks\Baskball- Jump Shot\Video'
```

### Set Filenames (MODIFY for your project)<br/>
Indicate the name of the video and corresponding video for the vector overlay you are creating.

```
file1_force = 'Trial 055.txt' 
file1_video = '191118_1004055.mp4'
file1_vid_new = file1_video[:-4]+ '_OL.mp4'
```
### Identify the Force Plates (MODIFY for your project)<br/>
Indicate the name of the force plates so the correct data can be pulled from the imported file.<br/>
Note: This will change/not be needed for older collections (any collection done without the use of portable force plates will not have these variables)

```
fp1 = 'Attila49'
fp2 = 'Ryan52'
```
### Indicate Video Sampling Rate (MODIFY for your project)<br/>
Specify the sampling rate of the video that was recorded<br/>
__Typical Sampling Rates__:<br/>
*Panasonic Cameras- 120, 240 Hz<br/>
*Older Video- 30-60 Hz<br/>

```sampvid_f1 = 120```

### Identify Video Sync Frame   
Note: Python is a zero based coding language so if the sync frame is 120, in Python the frame should be 119

```
contactframe_f1 = 163-1 
```

*Insert a picture of the sync frame*

### Load the Force Data <br/>
Use the ImportForce_TXT function to import force data from Bioware. You can also create a pandas dataframe if the force data is in another format.<br/>
bw is the Body weight of the participant from that session. This is sometimes messed up during collections and can be hard coded if needed.<br/>
samp is the sampling rate of the force plate. (Can be hard coded if needed but is typically 1200 Hz for most collections)

```
data_f1_raw, samp, bw = ImportForce_TXT(os.path.join(path_force, file1_force)
```

Example of hardcoding bw or samp:
```
bw = 607 
samp = 1200
```

Functions Used in this Section  
[ImportForce_TXT](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_txt)

### Find Contact Intervals <br/>
Uses the FindContactIntervals function to find where the reaction force crosses a specific threshold. Typically we use Vertical GRF.<br/>
The threshold should be ideally less than 20N and can be set using the argument "thresh" within the function.

```
ci_f1 = FindContactIntervals((data_f1_raw['Attila49 9286BA_Fz'] +data_f1_raw['Ryan52 9286BA_Fz']),samp,thresh=16)
```

*Insert a picture of the contact intervals*

Functions Used in this Section  
[FindContactIntervals](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-findcontactintervals)

### Find Plate Corners
Find the location of the force plate corners using the function _findplate_.  
You can use framestart to select another frame in the video to use for the selection (ie. if person is on the plate and blocks one of the corners).  
Use the _label_ argument to add a message that you want to remember (ie. Select both plates with Atttila49 FIRST).  
Corners should be selected in a CW direction starting with the TOP LEFT CORNER.

```
plate_area = findplate(os.path.join(path_video, file1_video),framestart=0,
                       label = 'Insert image here')
```

* Insert a picture of how to select the corners of the plates properly

Functions Used in this Section  
[findplate](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-findplate)

### Crop Data
Find the region of the force data that you would like to overlay on the video. 

Method 1: Overlay a specific contact region  
Use this method when you only want to display a specific contact region on for the Vector Overlay
```
### Crop Data
data_f1 = {0: data_f1_raw.filter(regex = fp1).iloc[ci_f1['Start'][2]:ci_f1['End'][2],:],
           1: data_f1_raw.filter(regex = fp2).iloc[ci_f1['Start'][2]:ci_f1['End'][2],:]}
```

* Insert a picture of choosing one region to overlay

Method 2: Start vector overlay from a certain region of force data  
Use this method when the person is already in contact with the plate when the video begins
```
# Identify the sync frame in the force data
sync_frame_force = ci_f1['End'][1]
# Identify the sync frame in the video
sync_frame_vid = 162
# Find the point in the force data where the video would begin
init_frame_force = sync_frame_force - (sync_frame_vid * (samp/sampvid_f1))
                             

### Crop Data
data_f1 = {0: data_f1_raw.filter(regex = fp1).iloc[init_frame_force:ci_f1['End'][2],:],
           1: data_f1_raw.filter(regex = fp2).iloc[init_frame_force:ci_f1['End'][2],:]}
```

### Zero Force Plates<br/>
__Note:__ This doesn't necessarily have to be done but can help reduce noice from FP vectors.

```
# # # Set values below 16N to 0 
 ### File 1
 for cntf in range(len(data_f1[0])):
     if (data_f1[0].iloc[cntf,2] < 16):
         data_f1[0].iloc[cntf,:] = 0
     if (data_f1[1].iloc[cntf,2] < 16):
         data_f1[1].iloc[cntf,:] = 0
```

### Calculate Pixel to Meter Ratio and Magnitude to Pixel Ratio
pix2m is a function which uses the the plate area found above to determine the number of pixels in a meter in the x and y directions in the video.   
mag2pix is a function which determines how big the vector should be in relation to the participants bodyweight.  
Dimensions of FPs used by the USC BRL Lab:  
Kistler Portable Force Plates: Long (0.6 meters), Short (0.4 meters)

```
pix2m = pix2m_fromplate(plate_area, (0.6, 0.4))
mag2pix = bw2pix(pix2m['x'],bw,bwpermeter=2)
```

Functions Used in this Section  
[pix2m_fromplate](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-pix2m_fromplate), [mag2pix](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-bw2pix)


### Convert Force Data to Pixels
This argument of the convertdata function helps to put the force data in the __video__ reference system. 
If FP1 needs to be adjusted you can use 0 within the dictionary. 

![Flip](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/Flip_convertData.png)  
Figure: Illustrating how flips impact how force is displayed for the vector overlay.
```
flip = {0: ['fy','ax'],
        1: ['fy','ay']}
```

An object called _transform_data_ is created using the previously defined arguments.  
*The argument _mode_ is used to determine if 1 or 2 vectors should be plotted:
* One force vector use "combine"
* Two (or more) force vectors use "ind" 

```
transform_data = convertdata(data_f1, mag2pix, pix2m, view = "fx",
                             mode= "combine",
                              platelocs = plate_area, flip = flip )
```                             
                           

Run the data2pix function within dataconversion_force script to convert the force data to pixels in the video reference system.

```
transform_data.data2pix()
```

Pulls the force plate data in pixels from the transform_data structure and places it into a new variable.
```
data_pix_f1 = transform_data.data_fp
```

Functions Used in this Section  
[convertdata](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-convertdata)

### Run Vector Overlay
Run the vector overlay function after setting up all of the appropriate variables/input arguments.  
The video will be saved in the same path that was specified for the original video defined by path_video and file1_video

```
vectoroverlay(os.path.join(path_video, file1_video), file1_vid_new,data_pix_f1,
              contactframe_f1,samp_force= samp, samp_video= sampvid_f1,
              dispthresh=2)
```

Functions Used in this Section  
[vectoroverlay](https://github.com/USCBiomechanicsLab/labcodes/blob/master/VectorOverlay/Documentation_VectorOverlay.md#vectoroverlay-vectoroverlay)
