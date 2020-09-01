# Example Vector Overlay
## This file will provide the step by step process for using the functions in the labcodes repository to generate a vector overlay.


For a video that walks you through creating a vector overlay for the PAC12 Steady State Running 
[Click Here](https://drive.google.com/drive/folders/1bKA8pVp695KqJMAeGPvVXo6gOT0loFao)


## Process for Vector Overlay: Basketball Jump Shot Example

### Import Package and Modules

import os <br/>
from ImportForce_TXT import ImportForce_TXT<br/>
from FindContactIntervals import FindContactIntervals<br/>
from findplate import findplate<br/>
from pixelratios import pix2m_fromplate, bw2pix<br/>
from dataconversion_force import convertdata<br/>
from VectorOverlay.vectoroverlay import vectoroverlay<br/>

### Set Path (MODIFY for your project)<br/>
This is the path on your computer where the video and corresponding force file will be stored.<br/>
Note: In Python, "r" stands for "raw" so it causes backslashes to be interpreted as actual backslashes instead of special characters

path_force = __r'F:\USC Biomechanics Research\HBIO 408\Tasks\Baskball- Jump Shot\Force'__<br/>
path_video = __r'F:\USC Biomechanics Research\HBIO 408\Tasks\Baskball- Jump Shot\Video'__

### Set Filenames (MODIFY for your project)<br/>
Indicate the name of the video and corresponding video for the vector overlay you are creating.

file1_force = __'Trial 055.txt'__ <br/>
file1_video = __'191118_1004055.mp4'__

### Identify the Force Plates (MODIFY for your project)<br/>
Indicate the name of the force plates so the correct data can be pulled from the imported file.<br/>
Note: This will change/not be needed for older collections (any collection done without the use of portable force plates will not have these variables)

fp1 = 'Attila49' <br/>
fp2 = 'Ryan52'

### Indicate Video Sampling Rate (MODIFY for your project)<br/>
Specify the sampling rate of the video that was recorded<br/>
__Typical Sampling Rates__:<br/>
*Panasonic Cameras- 120, 240 Hz<br/>
*Older Video- 30-60 Hz<br/>

sampvid_f1 = 120

### Identify Video Sync Frame <br/>
Note: Python is a zero based coding language so if the sync frame is 120, in Python the frame should be 119

contactframe_f1 = 163-1 

*Insert a picture of the sync frame*

### Load the Force Data <br/>
Use the ImportForce_TXT function to import force data from Bioware. You can also create a pandas dataframe if the force data is in another format.<br/>
bw is the Body weight of the participant from that session. This is sometimes messed up during collections and can be hard coded if needed.<br/>
samp is the sampling rate of the force plate. (Can be hard coded if needed but is typically 1200 Hz for most collections)

data_f1_raw, samp, bw = ImportForce_TXT(os.path.join(path_force, file1_force)

Example of hardcoding bw or samp:
bw = 607 
samp = 1200

### Find Contact Intervals <br/>
Uses the FindContactIntervals function to find where the reaction force crosses a specific threshold. Typically we use Vertical GRF.<br/>
The threshold should be ideally less than 20N and can be set using the argument "thresh" within the function.

ci_f1 = FindContactIntervals((data_f1_raw['Attila49 9286BA_Fz'] +data_f1_raw['Ryan52 9286BA_Fz']),samp,thresh=16)

*Insert a picture of the contact intervals*






