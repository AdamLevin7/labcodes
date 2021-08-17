# Title     : Documentation Functions
# Objective : Create a script that outputs documentation markdowns
# Created by: hestewar, harperestewart7@gmail.com
# Created on: 8/17/2021

# TODO Make documentation format for all codes, specify the keywords/things to search for
# TODO Read that information as the inputs to this function
# TODO make things into lists to regenerate documentation links and reflect updates (loop a list)
# TODO make a documentation package (not necessary but fun)


# Gather input variables or make a normal function*
# Ask for input if nothing is provided

script_name = "blah"
function_name = "blah_function"
script_website = 'blah_blah.com'
keywords <- "blah_keyword"

# Concatenate the lines together


cat(paste0("
## Script: ", script_name, "\n",
"### Function ", function_name, "\n",
"[Link to ", script_name, " Code](", script_website, ")", "\n",
"\n",
"### **Keywords:**", "\n",
keywords))

### **Syntax:**
```
from ", script_name," import", function_name,"

", outputs, " = ", function_name, "(", inputs, ")",
```
### Dependencies
* **scipy:**
* **np**: numpy
* **centraldiff:** USC BRL Function from derivative script

### **Description:**<br/>
Filter all columns of a dataframe using a spine interpolation method and filtfilt (zero-phase)

### **Arguments:**

#### *Inputs*

* **df:** DATAFRAME data with columns to be filtered (first column will not be)
* **b:** ARRAY_LIKE numerator coefficient vector of the filter
* **a:** ARRAY_LIKE denominator coefficient vector of the filter

#### *Outputs*

   * **filt_data:** DF Filtered input dataframe

### **Examples:**
Helpful examples

[Back to Table of Contents](#table-of-contents)

"

