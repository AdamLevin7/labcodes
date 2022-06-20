# USCBRL: Codes for USC Biomechanics Research Lab

## START HERE:
### Creating a Jetbrains account to use Pycharm IDE (Interactive way to run python)
[How to get Pycharm](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/_Getting%20PyCharm%20Educational%20Version.pdf)
  Created by Westview HS Students Arnav Sharma and Anirudh Kannan :slightly_smiling_face:

## Environment Installation Directions
### In Anaconda prompt:
* Change directory to where requirements.txt is located
```
conda create --name uscbrl_env
conda activate uscbrl_env
```
* Install pip in the blank environment
```
conda install pip
```
* Install package requirements from .txt file
```
pip install -r requirements.txt --user 
```
### In Pycharm
* File > Setting (Gear in top right corner) > Add
* Select "Conda Environment" on left hand side
* Choose Exising Environment radio button
* Change interpreter to uscbrl_env file (probably don't select "Make available to all projects")
* Hit OK
* Bottom right corner will show the Python version you are running ie. Python 3.8 and the environment (uscbrl_env)


## Biomechanics Workflow

![Biomech Workflow](https://github.com/USCBiomechanicsLab/labcodes/blob/master/DocMaterials/Biomechanics_Workflow.png)
**Figure:** *General biomechanics workflow*

## Topics:

| Description | Folder Link |
| ------------- | ------------- | 
| Documentation for general codes | ⚫ [General Codes](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md)| 
| Vector Overlay | ![#add8e6](https://via.placeholder.com/15/add8e6/000000?text=+) [Vector Overlay](https://github.com/USCBiomechanicsLab/labcodes/tree/master/VectorOverlay)|
| Animate Videos (Linegraphs, FBD visuals) | 🟢 [Animate Videos](https://github.com/USCBiomechanicsLab/labcodes/tree/master/animatevideos) |
| Strobe Images and Videos| 🟢[Strobe Images/Videos](https://github.com/USCBiomechanicsLab/labcodes/tree/master/Strobe) |
|Calculate Center of Mass | 🟠[COM](https://github.com/USCBiomechanicsLab/labcodes/tree/master/CalcCOM)|
|Digitizing Resources | 🔴[Digitizing](https://github.com/USCBiomechanicsLab/labcodes/tree/master/digitizing)|
|Calculate Net Joint Moments| 🟣[NJM](https://github.com/USCBiomechanicsLab/labcodes/tree/master/NJM)|
|Calculating Kinematics| [Kinematics](https://github.com/USCBiomechanicsLab/labcodes/tree/master/kinematics)|
|Apply Projectile Motion to video | 🟢[Projectile Motion](https://github.com/USCBiomechanicsLab/labcodes/tree/master/projectilemotion)|
|Angle-Angle Plots | 🔴[Angle-Angle Diagrams](https://github.com/USCBiomechanicsLab/labcodes/blob/master/kinematics/Example_AngAng.md) |

[Index of Available Codes](https://github.com/USCBiomechanicsLab/labcodes/blob/master/code_index.md)
