# Example Angle Angle Diagram Code
## This file will provide the step by step process for using the functions in the labcodes repository to generate an angle-angle diagram.


For a video that walks you through creating angle-angle diagrams for the PAC12 Steady State Running 
[Click Here](https://drive.google.com/drive/u/0/folders/1bKA8pVp695KqJMAeGPvVXo6gOT0loFao)

## Process for creating Angle Angle Diagrams: Steady State Running Example



### Import Package and Modules

```
from dataconversion_digi import convertdigi
from CalcCOM.segdim_deleva import segmentdim
from CalcCOM.calc_centermass import main as calc_cm
from kinematics.calc_segmentangle import segangle
from kinematics.calc_jointangle import jointangle
from derivative import centraldiff
import numpy as np
import matplotlib.pyplot as plt
```

## Functions Used in this Code

### Set Path, Filenames, Parameters (MODIFY for your project)  
You will need the digitized video data, video file, and force file, video sampling rate (Hz), and sex of the participant to get started.

```
file_digi = r'C:\Users\hestewar\Codes-USCBiomechanicsLab\summerprojects2020\harper\Digitizing\24281_Sp20_Trial24xypts.csv'
file_video = r'C:\Users\hestewar\Codes-USCBiomechanicsLab\summerprojects2020\harper\Video\P1001238.MOV'
file_force = r'C:\Users\hestewar\Codes-USCBiomechanicsLab\summerprojects2020\harper\Force\24281Trial 024.txt'
samp_vid = 240
sex = 'f'
```

### Load Data
Use the function convertdigi to convert the digitizied data from the .csv file. This example uses digitized data from MATLAB.  
However there are other functions within convertdigi which can be used to reformat other types of digitized data.

```
transformdata = convertdigi(file_digi)
data_digi = transformdata.dltdv_reformat()
```

### Calculate Center of Mass (COM)

Find the segment parameters.  
This function is using data from the DeLeva tables which is a classic anthropometry paper used commonly in biomechanics for analyzing biomechanics of athletic populations.

```
segments = segmentdim(sex)
```

Calculate the center of mass (COM) of the participant.

```
data_cm = calc_cm(data_digi,segments)
```

### Calculate Angles

Calculate the segment angles.
These are the angle measured from the right horizontal to each individual segment (ie. shank angle, thigh angle, foot angle)
```
angles_seg = segangle(data_digi, segments)
```

Calculate Joint angles. 
This calculates the angle between two adjacent segments (ie. knee angle would be between the thigh and the shank)

```
angles_joint = jointangle(data_digi, segments)
```

### Convert to Degrees

Convert both sets of angles from radians to degrees. 
```
angles_seg.iloc[:,1:] = angles_seg.iloc[:,1:] * (180/np.pi)
angles_joint.iloc[:,1:] = angles_joint.iloc[:,1:] * (180/np.pi)
```

### Calculate Angular Velocity

Calculate the angular velocity of the segment angles. (Angular velocity is how much the angular position or orientation changes over time)
```
angvel_seg = centraldiff(angles_seg, 1/samp_vid)
```

Calculate the joint angular velocity.
```
angvel_joint = centraldiff(angles_joint, 1/samp_vid)
```

### Plot Angle-Angle Diagrams
Plot examples that could be generated to show the coordination between two segments or joints. 

Angle-angle plot that shows the coordination between the shank and the thigh segments. 
```
plt.plot(angles_seg['shank_left'], angles_seg['thigh_left'],'o')
plt.axis([0,180,0,180])
plt.xlabel('Shank Angle (deg)')
plt.ylabel('Thigh Angle (deg)')
plt.title('Shank-Thigh Coordination')
plt.savefig('24281 Trial 024_angang_shankthigh.png')
```
![ShankThigh](https://github.com/USCBiomechanicsLab/labcodes/tree/master/DocMaterials/angang_shankthigh.png)
Figure: Example of Shank-Thigh Angle-Angle plot demonstrating coordination patterns.

Angle-angle plot that shows the coordination between the knee and hip joints.
```
plt.plot(angles_joint['knee_left'], angles_joint['hip_left'],'o')
plt.axis([90,180,90,180])
plt.xlabel('Knee Angle (deg)')
plt.ylabel('Hip Angle (deg)')
plt.title('Knee-Hip Coordination')
plt.savefig('24281 Trial 024_angang_kneehip.png')
```

![KneeHip](https://github.com/USCBiomechanicsLab/labcodes/tree/master/DocMaterials/angang_kneehip.png)
Figure: Example of Knee-Hip Angle-Angle plot demonstrating coordination patterns.


