# Code Index

## Index with links to find functions within labcodes

### Links to other repositories-
| Organization | Repository | Description | Virtual Environment |
| ------------- | ------------- | ------------- | ------------- | 
| [USATF-Biomechanics](https://github.com/USATF-Biomechanics) | [processing_codes](https://github.com/USATF-Biomechanics/processing_codes)| Processing codes for USATF | [usatf_env.yaml](https://github.com/USATF-Biomechanics/processing_codes/blob/master/usatf_env.yaml) |
| [USATF-Biomechanics](https://github.com/USATF-Biomechanics) | [data_from_websites](https://github.com/USATF-Biomechanics/data_from_websites)| Scraping data from websites | [usatf_env.yaml](https://github.com/USATF-Biomechanics/processing_codes/blob/master/usatf_env.yaml) |
| [USATF-Biomechanics](https://github.com/USATF-Biomechanics) | [server_vis](https://github.com/USATF-Biomechanics/server_vis)| Shiny apps, htmls, for USATF server | [usatf_env.yaml](https://github.com/USATF-Biomechanics/processing_codes/blob/master/usatf_env.yaml) |


## Scripts, Functions, Links to Documentation

*** 
**Script:**  [toe_locations.py](https://github.com/USATF-Biomechanics/processing_codes/blob/master/toe_locations.py) 
Modules for calculating toe locations relative to certain objects (ie. board)

*Functions:*  
* **findtoelocations** - Find location of contact toe using the video or digitized data. (Assuming pixel locations are in the reference system of the video, origin - top left)   
[Documentation]  
* **toe2board** - Calculates distance from to board for a given frame. Fits a line btw edges of board and provides x-position of the toe distance relative to y-position of the fitted line. Positive value means toe is behind board (good jump/fair). Negative means toe is past board (fault/foul).      
[Documentation]
* **toeloc** - Identify the location of the toe.    
[Documentation]


*** 
**Script:**  [jumpvelocity.py](https://github.com/USATF-Biomechanics/processing_codes/blob/master/jumpvelocity.py) 
Modules with different methods for calculating velocity.

*Functions:*  
* **filtdata** - Filters all columns of the dataframe.    
[Documentation]  
* vel_filt - Velocity for every frame calculated from filtered data set.    
[Documentation]
* **vel_analytical** - Calculated takeoff and final velocity using equations of motion.    
[Documentation]
* **vel_poly** - Takeoff and final velocity caclulated using the mean different for x (horizontal) and polynomical fit for y (vertical)    
[Documentation]

*** 
**Script:**  [processlogsheet.py](https://github.com/USATF-Biomechanics/processing_codes/blob/master/processlogsheet.py) 
Gather info from the logsheet to upload info and/or upload and process force data

*Functions:*  
* **ls_info** - Gather logsheet info into specific tables to upload to database.  
[Documentation]  
* **ls_force** - Process force data and upload to database.  
[Documentation]

*** 
**Script:**  [sql_setdtypes.py](https://github.com/USATF-Biomechanics/processing_codes/blob/master/sql_setdtypes.py) 

*Functions:*  
* **setdtypes** - Create dictionary stating column names and data types for SQL database format.  
[Documentation]

*** 
**Script:**  [FindMotion.py](https://github.com/USATF-Biomechanics/processing_codes/blob/master/FindMotion.py) 

*Functions:*  
* **FindMotion** - Find frame when object/person enters and leaves the image (assuming this is reason for change in pixels occuring)   
[Documentation]
  
*** 
**Script:**  [ImportForce_TXT.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/ImportForce_TXT.py) 

*Functions:*  
* **ImportForce_TXT** - Import force data from text files     
[Documentation](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_txt)
* **combine_force** - Combine all force plates to time, fx, fy, fz    
[Documentation]

***
**Script:**  [FindContactIntervals.py](https://github.com/USCBiomechanicsLab/labcodes/blob/master/FindContactIntervals.py) 

*Functions:*
* **FindContactIntervals** - Find the beginning and end of contact intervals when provided a single column
vertical force data.     
[Documentation](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-findcontactintervals)

***
**Script:**  [HBIO408_BatchImportKDA.m](https://github.com/USCBiomechanicsLab/labcodes/blob/master/HBIO408_BatchImportKDA.m) 

*Functions:*
* **script** - Select KDA files and exports .csv and .jped with force-time curve to compare with .avi overlay  
[Documentation](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-hbio408_batchimportkda)

***

**Script:**  [importForce_KDA.m](https://github.com/USCBiomechanicsLab/labcodes/blob/master/importForce_KDA.m) 

*Functions:*
* **importForce_KDA** - Import numeric force data from a text file as column vectors. B10  
[Documentation](https://github.com/USCBiomechanicsLab/labcodes/blob/master/Documentation_General.md#function-importforce_kda)

***
