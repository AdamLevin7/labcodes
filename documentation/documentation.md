# Documentation- 

## Table of Contents 

|Description|Script|Functions| 
| ------------- | ------------- | ------------- | 
|Scrape a code script for documentation info|document_fxn.py|[scrape_documentation](#function-scrape_documentation)| 
| Find indexes where occurs in the list|document_fxn.py|[fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]]](#function-fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]])| 
|fxn_desc = fxn_desc.replace("", "")|document_fxn.py|[fxn_name_2=fxn_name_1.replace("","")](#function-fxn_name_2=fxn_name_1.replace("",""))| 
|	List scripts in repository and scrape documentation information.|document_fxn.py|[gather_scripts](#function-gather_scripts)| 
|	Create Github documentation format for functions|document_fxn.py|[create_documentation](#function-create_documentation)| 
|Creates series of documentation for functions in a repository|document_fxn.py|[batch_documentation](#function-batch_documentation)| 
|	brief description here (1 line)|document_fxn.py|[table_of_contents](#function-table_of_contents)| 
|	Creates series of documentation for functions in a repository|document_fxn.R|[batch_documentation](#function-batch_documentation)| 
|	Creates Github markdown script for documenting a function|document_fxn.R|[create_documentation](#function-create_documentation)| 
|	Create documentation csv file if it doesn't exist|document_fxn.py|[create_doc_csv](#function-create_doc_csv)| 
|Scrape a code script for documentation info|document_fxn.py|[scrape_documentation](#function-scrape_documentation)| 
| Find indexes where occurs in the list|document_fxn.py|[fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]]](#function-fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]])| 
|fxn_desc = fxn_desc.replace("", "")|document_fxn.py|[fxn_name_2=fxn_name_1.replace("","")](#function-fxn_name_2=fxn_name_1.replace("",""))| 
|	List scripts in repository and scrape documentation information.|document_fxn.py|[gather_scripts](#function-gather_scripts)| 
|	Create Github documentation format for functions|document_fxn.py|[create_documentation](#function-create_documentation)| 
|Creates series of documentation for functions in a repository|document_fxn.py|[batch_documentation](#function-batch_documentation)| 
|	brief description here (1 line)|document_fxn.py|[table_of_contents](#function-table_of_contents)| 
|	Creates series of documentation for functions in a repository|document_fxn.R|[batch_documentation](#function-batch_documentation)| 
|	Creates Github markdown script for documenting a function|document_fxn.R|[create_documentation](#function-create_documentation)| 
 

### End Table of Contents <br/> 
## Script: document_fxn.py 
 
### Function: scrape_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import scrape_documentation 



output1: FILE .csv file containing updated documentation information


 = scrape_documentation(code_script: STR Code script with documentation info
doc_codes_csv: STR .csv file containing documentation information

) 

```` 

### Dependencies 

pandas
tkinter

 

### **Description:** 

Scrape a code script for documentation info 

        Scrape code for documentation information.
        Write that data into .csv file

 

### **Arguments:** 

#### *Inputs* 

code_script: STR Code script with documentation info
doc_codes_csv: STR .csv file containing documentation information



#### *Outputs* 

output1: FILE .csv file containing updated documentation information


 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]] 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]] 



nan = fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]]( Find indexes where Output occurs in the list
) 

```` 

### Dependencies 

depend_pos_list = [i for i in range(len(info_list)) if 'Dependencies' in info_list[i]]
 

### **Description:** 

 Find indexes where occurs in the list 

     Find indexes where occurs in the list
    details_pos_list = [i for i in range(len(info_list)) if 'Details:' in info_list[i]]
     Find indexes where Input occurs in the list
 

### **Arguments:** 

#### *Inputs* 

 Find indexes where Output occurs in the list


#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: fxn_name_2=fxn_name_1.replace("","") 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import fxn_name_2=fxn_name_1.replace("","") 



doc_csv_file: FILE Where documentation data is stored (.csv file)

 = fxn_name_2=fxn_name_1.replace("","")(extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored

) 

```` 

### Dependencies 

nan 

### **Description:** 

fxn_desc = fxn_desc.replace("", "") 

        fxn_details = fxn_details.replace("", "")
         Gather inputs
        fxn_inputs =''.join(info_list[input_loc+1:output_loc])
        fxn_inputs = fxn_inputs.replace("", "")
        fxn_inputs = fxn_inputs.replace("    ", "")
         Gather outputs
        fxn_outputs = ''.join(info_list[output_loc+1:depend_loc])
        fxn_outputs = fxn_outputs.replace("", "")
        fxn_outputs = fxn_outputs.replace("    ", "")
         Gather dependencies
        fxn_depen = ''.join(info_list[depend_loc+1:docstring_loc])
        fxn_depen = fxn_depen.replace("", "")
        fxn_depen = fxn_depen.replace("    ", "")
     Find name of Github org and repository by splitting the filename
        doc_csv_split = doc_csv_file.split('_')
        github_org = doc_csv_split[1]
        repo_name = doc_csv_split[2]

         Find the folder names using the path
        folder_names_string = doc_csv_split[0].split('/')
        folder_name = folder_names_string[-2]

         Create the string of the script webiste
        script_website = 'https://github.com/' + github_org + '/' + repo_name[:-4] + \
                     '/' + 'blob/master/' + folder_name + '/' + script_name

         Remove row in table if the function was already documented to update
        if documentation_csv['fxn_name'].str.contains(fxn_name).any():
            documentation_csv[~documentation_csv.fxn_name.str.contains(fxn_name)]

        Create row for the specific function
        new_row = pd.DataFrame([[script_name,
                                 fxn_name,
                                 script_website,
                                 fxn_desc,
                                 fxn_details,
                                 fxn_depen,
                                 fxn_inputs,
                                 fxn_outputs]],
                               columns=['script_name', 'fxn_name',
                                        'script_website', 'fxn_desc',
                                        'fxn_details', 'fxn_depen',
                                        'fxn_inputs', 'fxn_outputs'])

         Append that row to the table for documentation
        frames = [documentation_csv, new_row]
        documentation_csv = pd.concat(frames)

         End loop here

    Write the table back out to .csv file
    documentation_csv.to_csv(doc_csv_file, index=False)

def gather_scripts(extensions = ('.py', '.R'), doc_csv_file = ''):
    """
    Function::: gather_scripts
    	Description: List scripts in repository and scrape documentation information.
    	Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

 

### **Arguments:** 

#### *Inputs* 

extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored



#### *Outputs* 

doc_csv_file: FILE Where documentation data is stored (.csv file)

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: gather_scripts 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import gather_scripts 



doc_csv_file: FILE Where documentation data is stored (.csv file)

 = gather_scripts(extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored

) 

```` 

### Dependencies 

os
tkinter
dep3 from uscbrl_script.py (USCBRL repo)
 

### **Description:** 

	List scripts in repository and scrape documentation information. 

    	Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

 

### **Arguments:** 

#### *Inputs* 

extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored



#### *Outputs* 

doc_csv_file: FILE Where documentation data is stored (.csv file)

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: create_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import create_documentation 



nan = create_documentation(script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

) 

```` 

### Dependencies 

inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

Outputs
docu_info: STR Documentation information as a long string?

Dependencies
dep1
dep2
dep3 from uscbrl_script.py (USCBRL repo)
 

### **Description:** 

	Create Github documentation format for functions 

    	Create Github documentation including inputs, outputs, dependencies, how to run the function etc.

 

### **Arguments:** 

#### *Inputs* 

script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions



#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: batch_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import batch_documentation 



Batch of Github markdown outputs for repository documentation

 = batch_documentation(doc_codes_csv: STR .csv input file directory containing information

) 

```` 

### Dependencies 

tkinter
pandas
 

### **Description:** 

Creates series of documentation for functions in a repository 

        Creates series of documentation for functions in a repository

 

### **Arguments:** 

#### *Inputs* 

doc_codes_csv: STR .csv input file directory containing information



#### *Outputs* 

Batch of Github markdown outputs for repository documentation

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: table_of_contents 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import table_of_contents 



tab_contents: STR Table of contents of functions in repository

 = table_of_contents(doc_csv_file: FILE csv file with documentation of functions

) 

```` 

### Dependencies 

pandas
tkinter
 

### **Description:** 

	brief description here (1 line) 

    	Full description with details here

 

### **Arguments:** 

#### *Inputs* 

doc_csv_file: FILE csv file with documentation of functions



#### *Outputs* 

tab_contents: STR Table of contents of functions in repository

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.R 
 
### Function: batch_documentation 

[Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.R import batch_documentation 



Batch of Github markdown outputs for repository documentation

 = batch_documentation(doc_codes_csv: STR .csv input file directory containing information


) 

```` 

### Dependencies 

create_documentation USCBRL Repo: labcodes
 

### **Description:** 

	Creates series of documentation for functions in a repository 

	Creates series of documentation for functions in a repository

 

### **Arguments:** 

#### *Inputs* 

doc_codes_csv: STR .csv input file directory containing information




#### *Outputs* 

Batch of Github markdown outputs for repository documentation

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.R 
 
### Function: create_documentation 

[Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.R import create_documentation 



nan = create_documentation(script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

) 

```` 

### Dependencies 

inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

Outputs
Prints Github markdown output to generate Github documentation

Dependencies
None
 

### **Description:** 

	Creates Github markdown script for documenting a function 

	Add details

 

### **Arguments:** 

#### *Inputs* 

script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions



#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: create_doc_csv 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import create_doc_csv 



output1: DATATYPE description goes here (units)

 = create_doc_csv(path_to_file: STR Path to .csv with repo information

) 

```` 

### Dependencies 

dep1
dep2
dep3 from uscbrl_script.py (USCBRL repo)
 

### **Description:** 

	Create documentation csv file if it doesn't exist 

    	Full description with details here

 

### **Arguments:** 

#### *Inputs* 

path_to_file: STR Path to .csv with repo information



#### *Outputs* 

output1: DATATYPE description goes here (units)

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: scrape_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import scrape_documentation 



output1: FILE .csv file containing updated documentation information


 = scrape_documentation(code_script: STR Code script with documentation info
doc_codes_csv: STR .csv file containing documentation information

) 

```` 

### Dependencies 

pandas
tkinter

 

### **Description:** 

Scrape a code script for documentation info 

        Scrape code for documentation information.
        Write that data into .csv file

 

### **Arguments:** 

#### *Inputs* 

code_script: STR Code script with documentation info
doc_codes_csv: STR .csv file containing documentation information



#### *Outputs* 

output1: FILE .csv file containing updated documentation information


 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]] 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]] 



nan = fxn_pos_list=[iforiinrange(len(info_list))if''ininfo_list[i]]( Find indexes where Output occurs in the list
) 

```` 

### Dependencies 

depend_pos_list = [i for i in range(len(info_list)) if 'Dependencies' in info_list[i]]
 

### **Description:** 

 Find indexes where occurs in the list 

     Find indexes where occurs in the list
    details_pos_list = [i for i in range(len(info_list)) if 'Details:' in info_list[i]]
     Find indexes where Input occurs in the list
 

### **Arguments:** 

#### *Inputs* 

 Find indexes where Output occurs in the list


#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: fxn_name_2=fxn_name_1.replace("","") 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import fxn_name_2=fxn_name_1.replace("","") 



doc_csv_file: FILE Where documentation data is stored (.csv file)

 = fxn_name_2=fxn_name_1.replace("","")(extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored

) 

```` 

### Dependencies 

nan 

### **Description:** 

fxn_desc = fxn_desc.replace("", "") 

        fxn_details = fxn_details.replace("", "")
         Gather inputs
        fxn_inputs =''.join(info_list[input_loc+1:output_loc])
        fxn_inputs = fxn_inputs.replace("", "")
        fxn_inputs = fxn_inputs.replace("    ", "")
         Gather outputs
        fxn_outputs = ''.join(info_list[output_loc+1:depend_loc])
        fxn_outputs = fxn_outputs.replace("", "")
        fxn_outputs = fxn_outputs.replace("    ", "")
         Gather dependencies
        fxn_depen = ''.join(info_list[depend_loc+1:docstring_loc])
        fxn_depen = fxn_depen.replace("", "")
        fxn_depen = fxn_depen.replace("    ", "")
     Find name of Github org and repository by splitting the filename
        doc_csv_split = doc_csv_file.split('_')
        github_org = doc_csv_split[1]
        repo_name = doc_csv_split[2]

         Find the folder names using the path
        folder_names_string = doc_csv_split[0].split('/')
        folder_name = folder_names_string[-2]

         Create the string of the script webiste
        script_website = 'https://github.com/' + github_org + '/' + repo_name[:-4] + \
                     '/' + 'blob/master/' + folder_name + '/' + script_name

         Remove row in table if the function was already documented to update
        if documentation_csv['fxn_name'].str.contains(fxn_name).any():
            documentation_csv[~documentation_csv.fxn_name.str.contains(fxn_name)]

        Create row for the specific function
        new_row = pd.DataFrame([[script_name,
                                 fxn_name,
                                 script_website,
                                 fxn_desc,
                                 fxn_details,
                                 fxn_depen,
                                 fxn_inputs,
                                 fxn_outputs]],
                               columns=['script_name', 'fxn_name',
                                        'script_website', 'fxn_desc',
                                        'fxn_details', 'fxn_depen',
                                        'fxn_inputs', 'fxn_outputs'])

         Append that row to the table for documentation
        frames = [documentation_csv, new_row]
        documentation_csv = pd.concat(frames)

         End loop here

    Write the table back out to .csv file
    documentation_csv.to_csv(doc_csv_file, index=False)

def gather_scripts(extensions = ('.py', '.R'), doc_csv_file = ''):
    """
    Function::: gather_scripts
    	Description: List scripts in repository and scrape documentation information.
    	Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

 

### **Arguments:** 

#### *Inputs* 

extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored



#### *Outputs* 

doc_csv_file: FILE Where documentation data is stored (.csv file)

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: gather_scripts 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import gather_scripts 



doc_csv_file: FILE Where documentation data is stored (.csv file)

 = gather_scripts(extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored

) 

```` 

### Dependencies 

os
tkinter
dep3 from uscbrl_script.py (USCBRL repo)
 

### **Description:** 

	List scripts in repository and scrape documentation information. 

    	Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

 

### **Arguments:** 

#### *Inputs* 

extensions: TUPLE Specify the extensions to document in repo
doc_csv_file: STR Path where .csv file with documentation info is stored



#### *Outputs* 

doc_csv_file: FILE Where documentation data is stored (.csv file)

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: create_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import create_documentation 



nan = create_documentation(script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

) 

```` 

### Dependencies 

inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

Outputs
docu_info: STR Documentation information as a long string?

Dependencies
dep1
dep2
dep3 from uscbrl_script.py (USCBRL repo)
 

### **Description:** 

	Create Github documentation format for functions 

    	Create Github documentation including inputs, outputs, dependencies, how to run the function etc.

 

### **Arguments:** 

#### *Inputs* 

script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions



#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: batch_documentation 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import batch_documentation 



Batch of Github markdown outputs for repository documentation

 = batch_documentation(doc_codes_csv: STR .csv input file directory containing information

) 

```` 

### Dependencies 

tkinter
pandas
 

### **Description:** 

Creates series of documentation for functions in a repository 

        Creates series of documentation for functions in a repository

 

### **Arguments:** 

#### *Inputs* 

doc_codes_csv: STR .csv input file directory containing information



#### *Outputs* 

Batch of Github markdown outputs for repository documentation

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.py 
 
### Function: table_of_contents 

[Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.py import table_of_contents 



tab_contents: STR Table of contents of functions in repository

 = table_of_contents(doc_csv_file: FILE csv file with documentation of functions

) 

```` 

### Dependencies 

pandas
tkinter
 

### **Description:** 

	brief description here (1 line) 

    	Full description with details here

 

### **Arguments:** 

#### *Inputs* 

doc_csv_file: FILE csv file with documentation of functions



#### *Outputs* 

tab_contents: STR Table of contents of functions in repository

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.R 
 
### Function: batch_documentation 

[Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.R import batch_documentation 



Batch of Github markdown outputs for repository documentation

 = batch_documentation(doc_codes_csv: STR .csv input file directory containing information


) 

```` 

### Dependencies 

create_documentation USCBRL Repo: labcodes
 

### **Description:** 

	Creates series of documentation for functions in a repository 

	Creates series of documentation for functions in a repository

 

### **Arguments:** 

#### *Inputs* 

doc_codes_csv: STR .csv input file directory containing information




#### *Outputs* 

Batch of Github markdown outputs for repository documentation

 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: document_fxn.R 
 
### Function: create_documentation 

[Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 



### **Keywords:** 

nan 



### **Syntax:** 

``` 

from document_fxn.R import create_documentation 



nan = create_documentation(script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

) 

```` 

### Dependencies 

inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions

Outputs
Prints Github markdown output to generate Github documentation

Dependencies
None
 

### **Description:** 

	Creates Github markdown script for documenting a function 

	Add details

 

### **Arguments:** 

#### *Inputs* 

script_name: STR Name of the script containing the function
function_name: STR Name of the specific function (module)
script_website: STR Github website of the script
keywords: STR keywords associated with the function
describe_fxn: STR Description of the function
depend_list: LIST Dependencies needed to run the function
inputs: LIST Input variable names and descriptions
outputs: LIST Output variable names and descriptions



#### *Outputs* 

nan 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
