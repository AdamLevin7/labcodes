"""
Script: document_fxn_py
    Create documentation functions for Github documentation.

Modules
    scrape_documentation: Scrape a code script for documentation info
    gather_scripts: List scripts in repository and scrape documentation information.
    create_documentation: Create Github documentation format for functions
    batch_documentation: Create markdown file with documentation for all functions in repository

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""
#TODO remove the .csv table element and just loop through files in a list
#TODO 2. Create exceptions for if a file doesn't contain "Function::" and print a list
# TODO Go through the functions and make sure format matches
# TODO make things into lists to regenerate documentation links and reflect updates (loop a list)
# TODO make a documentation package (not necessary but fun)

def scrape_documentation(code_script='', doc_csv_file=''):
    """
    Function::: scrape_documentation
        Description: Scrape a code script for documentation info
        Details: Scrape code for documentation information.
        Write that data into .csv file

    Inputs
        code_script: STR Code script with documentation info
        doc_codes_csv: STR .csv file containing documentation information

    Outputs
        output1: FILE .csv file containing updated documentation information


    Dependencies
        pandas
        tkinter

    """

    # Dependencies
    import pandas as pd
    from tkinter.filedialog import askopenfilename

    # Read in the documentation .csv files for the repository
    if doc_csv_file == '':
        doc_csv_file = askopenfilename(title='Select Documentation .csv file for Repository: ')
        documentation_csv = pd.read_csv(doc_csv_file)
    else:
        documentation_csv = pd.read_csv(doc_csv_file)

    # Read in the file of the code which contains the documentation information
    if code_script == '':
        code_script = askopenfilename(title='Select code script to scrape documentation: ')
        code_text = open(code_script)
    else:
        code_text = open(code_script)

    # Get the script name
    split_script = code_script.split('/')
    script_name = split_script[-1]

    # Inititalize the list
    info_list = []
    # For loop to append each line to a list
    for line in code_text:
        info_list.append(line)

    # Find indexes where Function:x3 occurs in the list:'
    fxn_pos_list = [i for i in range(len(info_list)) if 'Function:::' in info_list[i]]
    # Find indexes where Description: occurs in the list
    desc_pos_list = [i for i in range(len(info_list)) if 'Description:' in info_list[i]]
    # Find indexes where Details: occurs in the list
    details_pos_list = [i for i in range(len(info_list)) if 'Details:' in info_list[i]]
    # Find indexes where Input occurs in the list
    input_pos_list = [i for i in range(len(info_list)) if 'Inputs' in info_list[i]]
    # Find indexes where Output occurs in the list
    output_pos_list = [i for i in range(len(info_list)) if 'Outputs' in info_list[i]]
    # Find indexes where Dependencies occurs in the list
    depend_pos_list = [i for i in range(len(info_list)) if 'Dependencies' in info_list[i]]
    # Find indexes where """ docstrings occurs in the list
    docstr_pos_list = [i for i in range(len(info_list)) if '"""' in info_list[i]]

    for ind in fxn_pos_list:
    # Variables from script
    # Get the function name
        fxn_name_1 = info_list[ind].replace(" ", "")
        fxn_name_2 = fxn_name_1.replace("Function:::", "")
        fxn_name_3 = fxn_name_2.replace("\n", "")
        fxn_name = fxn_name_3.replace("#", "")

        # Get information closest to that function index
        desc_loc = min([i for i in desc_pos_list if i > ind])
        details_loc = min([i for i in details_pos_list if i > ind])
        input_loc = min([i for i in input_pos_list if i > ind])
        output_loc = min([i for i in output_pos_list if i > ind])
        depend_loc = min([i for i in depend_pos_list if i > ind])
        docstring_loc = min([i for i in docstr_pos_list if i > ind])

        # Get the variables
        fxn_desc = info_list[desc_loc]
        fxn_desc = fxn_desc.replace("#", "")
        fxn_desc = fxn_desc.replace("Description: ", "")
        fxn_desc = fxn_desc.replace("    ", "")

    # Join elements of list to create strings
        # Full detail string
        fxn_details = ''.join(info_list[details_loc:input_loc])
        fxn_details = fxn_details.replace("#", "")
        fxn_details = fxn_details.replace("Details: ", "")
        # Gather inputs
        fxn_inputs =''.join(info_list[input_loc+1:output_loc])
        fxn_inputs = fxn_inputs.replace("#", "")
        fxn_inputs = fxn_inputs.replace("    ", "")
        # Gather outputs
        fxn_outputs = ''.join(info_list[output_loc+1:depend_loc])
        fxn_outputs = fxn_outputs.replace("#", "")
        fxn_outputs = fxn_outputs.replace("    ", "")
        # Gather dependencies
        fxn_depen = ''.join(info_list[depend_loc+1:docstring_loc])
        fxn_depen = fxn_depen.replace("#", "")
        fxn_depen = fxn_depen.replace("    ", "")
    # Find name of Github org and repository by splitting the filename
        doc_csv_split = doc_csv_file.split('_')
        github_org = doc_csv_split[1]
        repo_name = doc_csv_split[2]

        # Find the folder names using the path
        folder_names_string = doc_csv_split[0].split('/')
        folder_name = folder_names_string[-2]

        # Create the string of the script webiste
        script_website = 'https://github.com/' + github_org + '/' + repo_name[:-4] + \
                     '/' + 'blob/master/' + folder_name + '/' + script_name

        # Remove row in table if the function was already documented to update
        if documentation_csv['fxn_name'].str.contains(fxn_name).any():
            documentation_csv[~documentation_csv.fxn_name.str.contains(fxn_name)]

        #Create row for the specific function
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

        # Append that row to the table for documentation
        frames = [documentation_csv, new_row]
        documentation_csv = pd.concat(frames)

        # End loop here

    #Write the table back out to .csv file
    documentation_csv.to_csv(doc_csv_file, index=False)

def gather_scripts(extensions = ('.py', '.R'), doc_csv_file = ''):
    """
    Function::: gather_scripts
    	Description: List scripts in repository and scrape documentation information.
    	Details: Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

    Inputs
        extensions: TUPLE Specify the extensions to document in repo
        doc_csv_file: STR Path where .csv file with documentation info is stored

    Outputs
        doc_csv_file: FILE Where documentation data is stored (.csv file)

    Dependencies
        os
        tkinter
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    import os.path
    from tkinter.filedialog import askdirectory

    # Select the repository that you are creating documentation for
    path = askdirectory(title='Select Repository to Update: ')

    # Create a list of all the files
    file_list = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            file_list.append(name)
        for name in directories:
            print('Directories: ')
            print(os.path.join(root, name))

    # Keep only the files that you want documented using languages argument
    # Don't document the init file
    file_list_sm = list(filter(lambda x: x.endswith(extensions) and not x.startswith('__init__'), file_list))
    print('Files to document: ')
    print(file_list_sm)

    # Run the documentation function
    for i in range(len(file_list_sm)):
        scrape_documentation(code_script=str(root + '/' + file_list_sm[i]),
                             doc_csv_file='')


def create_documentation(script_name='',
                         function_name='',
                         script_website='',
                         keywords='',
                         describe_fxn='',
                         details_fxn='',
                         depend_list='',
                         inputs='',
                         outputs=''):
    """
    Function::: create_documentation
    	Description: Create Github documentation format for functions
    	Details: Create Github documentation including inputs, outputs, dependencies, how to run the function etc.

    Inputs
        script_name: STR Name of the script containing the function
        function_name: STR Name of the specific function (module)
        script_website: STR Github website of the script
        keywords: STR keywords associated with the function
        describe_fxn: STR Description of the function
        depend_list: LIST Dependencies needed to run the function
        inputs: LIST Input variable names and descriptions
        outputs: LIST Output variable names and descriptions

    Outputs
        docu_info: STR Documentation information as a long string?

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """

    # Test to see if all variables were provided
    var_list = [script_name,
                function_name,
                script_website,
                keywords,
                describe_fxn,
                details_fxn,
                depend_list,
                inputs,
                outputs]

    # Prompt for input if it was not provided to the function
    prompt_list = ['Provide script name: ',
                       'Provide function (module) name: ',
                       'Provide script Github website: ',
                       'Provide function keywords: ',
                       'Provide function description: ',
                       'Provide function details: ',
                       'Provide list of dependencies: ',
                       'Provide list of inputs: ',
                       'Provide list of outputs: ']

    # For loop cycles through each input and checks to see if it was provided
    # If it was not provided then it prompts for input
    for i in range(len(var_list)):
        if (var_list[i] == ""):
            var_list[i] = input(prompt_list[i])

    # Reassign variables
    script_name = var_list[0]
    function_name= var_list[1]
    script_website= var_list[2]
    keywords= var_list[3]
    describe_fxn= var_list[4]
    details_fxn = var_list[5]
    depend_list= var_list[6]
    inputs= var_list[7]
    outputs= var_list[8]

    # Format the long documentation string
    docu_info = '''## Script: {script_name} \n 
### Function: {function_name} \n
[Link to {script_name} Code]({script_website}) \n
\n
### **Keywords:** \n
{keywords} \n
\n
### **Syntax:** \n
``` \n
from {script_name} import {function_name} \n
\n
{outputs} = {function_name}({inputs}) \n
```` \n
### Dependencies \n
{depend_list} \n
### **Description:** \n
{describe_fxn} \n
{details_fxn} \n
### **Arguments:** \n
#### *Inputs* \n
{inputs}\n
#### *Outputs* \n
{outputs} \n
### **Examples:** \n
Helpful examples \n
[Back to Table of Contents](#table-of-contents) \n'''.format(script_name = script_name,
                   function_name = function_name,
                   script_website = script_website,
                   keywords = keywords,
                   inputs = inputs,
                   outputs = outputs,
                   depend_list = depend_list,
                   describe_fxn= describe_fxn,
                   details_fxn = details_fxn
                   )
    return(docu_info)

#TODO make a for loop to format the outputs the way you want them
#TODO Other thoughts, documentation becomes a folder within each repository

def batch_documentation(doc_csv_file=''):
    """
    Function::: batch_documentation
        Description: Creates series of documentation for functions in a repository
        Details: Creates series of documentation for functions in a repository

    Inputs
        doc_codes_csv: STR .csv input file directory containing information

    Outputs
        Batch of Github markdown outputs for repository documentation

    Dependencies
        tkinter
        pandas
    """
    # Dependencies
    import pandas as pd
    from tkinter.filedialog import askopenfilename
    from documentation.document_fxn import create_documentation
    import os.path

    # Read in the documentation .csv files for the repository
    if doc_csv_file == '':
        doc_csv_file = askopenfilename(title='Select Documentation .csv file for Repository: ')
        docu_csv = pd.read_csv(doc_csv_file)
    else:
        docu_csv = pd.read_csv(doc_csv_file)

    # Make a .md File
    # open text file
    filename = 'documentation.md'
    file_exists = os.path.isfile(filename)

    # If the file doesn't exist
    if file_exists == False:
        text_file = open(filename, "x")
    # If the file does exist
    else:
        text_file = open(filename, "a")

    # Add the table of contents
    tab_cont_str = table_of_contents(doc_csv_file)
    text_file.write(tab_cont_str)

    # Use create_documentation function to cycle through each row and create the documentation
    docu_info_full = []
    for i in range(len(docu_csv)):
        docu_info_full = create_documentation(script_name=docu_csv.script_name[i],
                                              function_name=docu_csv.fxn_name[i],
                                              script_website=docu_csv.script_website[i],
                                              keywords=docu_csv.keywords[i],
                                              describe_fxn=docu_csv.fxn_desc[i],
                                              details_fxn =docu_csv.fxn_details[i],
                                              depend_list=docu_csv.fxn_depen[i],
                                              inputs=docu_csv.fxn_inputs[i],
                                              outputs=docu_csv.fxn_outputs[i])

        # write documentation information to the file
        text_file.write(docu_info_full)

    # close file
    text_file.close()

def table_of_contents(doc_csv_file=''):
    """
    Function::: table_of_contents
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        doc_csv_file: FILE csv file with documentation of functions

    Outputs
        tab_contents: STR Table of contents of functions in repository

    Dependencies
        pandas
        tkinter
    """
    # Dependencies
    import pandas as pd
    from tkinter.filedialog import askopenfilename

    # Read in the documentation .csv files for the repository
    if doc_csv_file == '':
        doc_csv_file = askopenfilename(title='Select Documentation .csv file for Repository: ')
        docu_csv = pd.read_csv(doc_csv_file)
    else:
        docu_csv = pd.read_csv(doc_csv_file)

    # Create a list of strings in the correct format for each function
    str_fxns = ''

    for i in range(len(docu_csv)):
        str_fxns = str_fxns + '''|{description}|{script}|[{fxn}](#function-{fxn})|'''.format(description=docu_csv.fxn_desc[i],
            script=docu_csv.script_name[i],
            fxn=docu_csv.fxn_name[i])

    # Create the table of contents for a repository
    tab_contents = '''# Documentation- \n
## Table of Contents \n
|Description|Script|Functions| 
| ------------- | ------------- | ------------- | 
{all_fxns} \n
### End Table of Contents <br/> \n'''.format(all_fxns = str_fxns)

    return(tab_contents)






