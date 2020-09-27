# Example Net Joint Moment Calculations
## This file will provide the step by step process for using the functions in the labcodes repository to get net joint moment calculations from foot to hip


Add a video example eventually 
[Click Here](https://drive.google.com/drive/folders/1bKA8pVp695KqJMAeGPvVXo6gOT0loFao)

## Process for NJM: Steady State Running Example

### Import Package and Modules
USC BRL Modules
```
from dataconversion_digi import dltdv_import
from ImportForce_TXT import ImportForce_TXT
from CalcCOM.segdim_deleva import segmentdim
from CalcCOM.calc_centermass import main as calc_cm
from CalcCOM.displayskeleton import addskeleton
from NJM.dig2jointkinetics import dig2jk_format
from NJM.dig2jointkinetics import dig2jk
```
Packages
```
import numpy as np
import matplotlib.pyplot as plt
```
## Functions Used in this Code
[dltdv_import](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-dltdv_import)  
[ImportForce_TXT](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_txt)  
[segmentdim](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM#function-segmentdim)  
[calc_cm](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM#table-of-contents)  
[addskeleton](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM#table-of-contents)  
[dig2jk_format](https://github.com/USCBiomechanicsLab/labcodes/tree/master/NJM/README.md)  
[dig2jk](https://github.com/USCBiomechanicsLab/labcodes/tree/master/NJM/README.md)  

### Set Path (MODIFY for your project)<br/>
This is the path on your computer where the digitized joint, video, and force data are stored. <br/>
Note: In Python, "r" stands for "raw" so it causes backslashes to be interpreted as actual backslashes instead of special characters
You need the following to complete this process:
* Force data
* Digitized joint centers (see documentation for how to digitize)
* Video (the video that was used to digitize the kinematic data)

```
file_digi = r'F:\USC Biomechanics Research\HBIO 408\Tasks\Steady State Running\Digitizing\SSRun_7minxypts.csv'
file_video = r'F:\USC Biomechanics Research\HBIO 408\Tasks\Steady State Running\Videos\7min_120Hz_SSRun_Fa19_OL.mp4'
file_force = r'F:\USC Biomechanics Research\HBIO 408\Tasks\Steady State Running\Force Files\7min_120Hz_SSRun_Fa19_Force.txt'
```

### Set Variables/Plate Contact/Parameters <br/>
You need to know the sampling rate of the video (typically 120 or 240 Hz for Panasonic cameras)
You need to know the participant sex for determining segment parameters.
Need force plates that were used in the collection (The following code demos the portable force plates)

```
samp_vid = 120 #Hz
sex = 'f'
fp1 = 'Attila49'
fp2 = 'Ryan52'
con_plate = ['Attila49 9286BA', 'Ryan52 9286BA']
```
This is the video frame when the runner contacts the force plate. 
```
frame_contact_f1 = 241
```
Create dictionary to flip the force data to match video reference system.
```
flip = {0: ['fx'],
        1: ['fx']}
```
### Load Data <br/>
Load in the digitized data
```
data_digi, frame_digi_start, frame_digi_end = dltdv_import(file_digi, file_vid=file_video, flipy='yes')
```

*Documentation for* [dltdv_import](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-dltdv_import)  


Load in the force data
```
data_f1_raw, samp_force, bw = ImportForce_TXT(file_force, rezero='b')
```
*Documentation for* [ImportForce_TXT](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_txt)  

### Calculate Center of Mass <br/>
Find the segment parameters
```
segments = segmentdim(sex)
```
*Documentation for* [segmentdim](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM#function-segmentdim)  
  

Calculate center of mass (convert from pixels to meters)
```
data_cm = calc_cm(data_digi, segments)
```
*Documentation for* [calc_cm](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM#table-of-contents)  

### Create Object to Reformat
Set up the Python object so it can be reformatted.
```
data_obj = dig2jk_format(data_digi, data_cm, data_f1_raw, bw, sex,
                         con_plate, frame_contact_f1, flip=flip, file_vid=file_video)

```
*Documentation for* [dig2jk_format](https://github.com/USCBiomechanicsLab/labcodes/tree/master/NJM/README.md)  


Create reformatted data object.
```
data_reformat_obj = data_obj.data_reformat(samp_vid=samp_vid)
```

### Create Joint Kinetics Object
```
jk_obj = dig2jk(data_reformat_obj.data_dig, data_reformat_obj.data_cm,
                data_reformat_obj.data_force, data_reformat_obj.segments,
                data_reformat_obj.xvals, contact_seg='foot_left', mass=bw/9.81,
                samp_dig=samp_vid, samp_force=samp_force)

```
*Documentation for* [dig2jk](https://github.com/USCBiomechanicsLab/labcodes/tree/master/NJM/README.md)  

### Calculate NJMs
Runs a series of modules which use the joint kinetics objects to determine the net joint moments over time throughout the contact phase.
```
data_njm = jk_obj.main()
```

### Output Interactive NJM Video
This function will output a video showing how the moments change over time on the FBDs for the lower extremity.
[fbd_display](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/fbd_display.py)

This is an example of how to use the function.
[Example Link](https://github.com/USCBiomechanicsLab/labcodes/blob/master/animatevideos/fbd_example.py)

### Example for NJM Plots
Example code for generating plots to show moments over time.
Can do this if you don't want to creat the video of the FBD and NJMs over time.

Foot, Ankle, and Reaction Force Moments
```
plt.plot(data_njm['time'], data_njm['foot_md'], label='Distal NJF Moment')
plt.plot(data_njm['time'], data_njm['foot_mp'], label='Proximal NJF Moment')
plt.plot(data_njm['time'], data_njm['foot_njmd'], label='Distal NJM Moment')
plt.plot(data_njm['time'], data_njm['foot_njmp'], label='Proximal NJM Moment')
plt.legend()
plt.ylim(-600, 600)
plt.title('SS Run 7 min  - Foot')
```

Ankle, Shank, Knee Moments
```
plt.figure()
plt.plot(data_njm['time'], data_njm['shank_md'], label='Distal NJF Moment')
plt.plot(data_njm['time'], data_njm['shank_mp'], label='Proximal NJF Moment')
plt.plot(data_njm['time'], data_njm['shank_njmd'], label='Distal NJM Moment')
plt.plot(data_njm['time'], data_njm['shank_njmp'], label='Proximal NJM Moment')
plt.legend()
plt.ylim(-600, 600)
plt.title('SS Run 7 min  - Shank')
```

Knee, Hip and Thigh Moments
```
plt.figure()
plt.plot(data_njm['time'], data_njm['thigh_md'], label='Distal NJF Moment')
plt.plot(data_njm['time'], data_njm['thigh_mp'], label='Proximal NJF Moment')
plt.plot(data_njm['time'], data_njm['thigh_njmd'], label='Distal NJM Moment')
plt.plot(data_njm['time'], data_njm['thigh_njmp'], label='Proximal NJM Moment')
plt.legend()
plt.ylim(-600, 600)
plt.title('SS Run 7 min  - Thigh')
```
