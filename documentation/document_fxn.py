"""
Script: document_fxn_py
    Create documentation functions for Github documentation.

Modules
    main: Runs the series of modules
    scrape_documentation: Scrape a code script for documentation info
    gather_scripts: List scripts in repository and scrape documentation information.
    create_documentation: Create Github documentation format for functions
    batch_documentation: Create markdown file with documentation for all functions in repository

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""
# TODO 2. Create exceptions for if a file doesn't contain "Function::" and print a list
# TODO Go through the functions and make sure format matches
# TODO make a documentation package (not necessary but fun)

def main(path_to_repo = ''):
    df_docu, repo_path = gather_scripts(extensions=('.py', '.R'),
                             df_documentation='',
                             path=path_to_repo)
    df_docu = df_docu.reset_index(drop=True)
    df_docu = df_docu.drop_duplicates()
    batch_documentation(df_documentation=df_docu, path =repo_path)


def scrape_documentation(code_script='',
                         df_documentation='',
                         path=''):
    """
    Function::: scrape_documentation
        Description: Scrape a code script for documentation info
        Details: Scrape code for documentation information.
        Write that data into .csv file

    Inputs
        code_script: STR Code script with documentation info
        df_documentation: DF Dataframe containing documentation information

    Outputs
        df_documentation: DF Updated dataframe with additional docu information

    Dependencies
        pandas
        tkinter

    """

    # Dependencies
    import pandas as pd
    from tkinter.filedialog import askopenfilename
    import tkinter

    # Read in the file of the code which contains the documentation information
    root = tkinter.Tk()
    root.withdraw()
    if code_script == '':
        code_script = askopenfilename(title='Select code script to scrape documentation: ')
        code_text = open(code_script)
    else:
        code_text = open(code_script)
    root.destroy()


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
        fxn_desc = fxn_desc.replace("\n", "")
        fxn_desc_list = fxn_desc.split()
        fxn_desc = " ".join(fxn_desc_list)

    # Join elements of list to create strings
        # Full detail string
        fxn_details = ''.join(info_list[details_loc:input_loc])
        fxn_details = fxn_details.replace("#", "")
        fxn_details = fxn_details.replace("Details: ", "")
        fxn_details_list = fxn_details.split()
        fxn_details = " ".join(fxn_details_list)
        # Gather inputs
        fxn_inputs = ''.join(info_list[input_loc+1:output_loc])
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

        # Find the folder names using the path
        folder_names_string = path.split('/')
        folder_name = folder_names_string[-1]
        github_org = folder_names_string[-3]
        repo_name = folder_names_string[-2]

        # Create the string of the script webiste
        script_website = 'https://github.com/' + github_org + '/' + repo_name + \
                         '/' + 'blob/master/' + folder_name + '/' + script_name

        # Create row for the specific function
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
        frames = [df_documentation, new_row]
        df_documentation = pd.concat(frames)

    return df_documentation


def gather_scripts(extensions = ('.py', '.R'),
                   df_documentation='',
                   path=''):
    """
    Function::: gather_scripts
    	Description: List scripts in repository and scrape documentation information.
    	Details: Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

    Inputs
        extensions: TUPLE Specify the extensions to document in repo
        df_documentation: DF Table with the documentation information
        path: STR Path of the repository

    Outputs
        df_documentation: DF Updated documentation table

    Dependencies
        os
        tkinter
        pandas
        glob
    """
    # Dependencies
    import os.path
    from tkinter.filedialog import askdirectory
    import pandas as pd
    import tkinter
    import glob

    root = tkinter.Tk()
    root.withdraw()
    # Select the repository that you are creating documentation for
    if path == '':
        path = askdirectory(title='Select Repository to Update: ')
    root.destroy()

    # Create a list of all the files
    file_list = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    # Keep only the files that you want documented using languages argument
    # Don't document the init file
    ignore_list = ['.git', 'pycache','.idea', '__init__']

    file_list_sm = [s for s in file_list if not any(x in s for x in ignore_list)]
    file_list_sm = [s for s in file_list_sm if any(x in s for x in extensions)]

    print('Files to document: ')
    print(file_list_sm)

    # If the dataframe hasn't been created yet, then create it
    if df_documentation == '':
        df_documentation = pd.DataFrame(columns=['script_name',
                                                 'fxn_name',
                                                 'script_website',
                                                 'fxn_desc',
                                                 'fxn_details',
                                                 'fxn_depen',
                                                 'fxn_inputs',
                                                 'fxn_outputs'])

    # Run the documentation function
    for i in range(len(file_list_sm)):
        print('Starting on '+str(i)+' of '+str(len(file_list_sm)) + ': '+file_list_sm[i])
        df_documentation = scrape_documentation(code_script=file_list_sm[i],
                                                df_documentation=df_documentation,
                                                path=path)

    return df_documentation, path


def create_documentation(script_name='',
                         function_name='',
                         script_website='',
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
        describe_fxn: STR Description of the function
        depend_list: LIST Dependencies needed to run the function
        inputs: LIST Input variable names and descriptions
        outputs: LIST Output variable names and descriptions

    Outputs
        docu_info: STR Documentation info, long string for a function

    Dependencies

    """

    # Test to see if all variables were provided
    var_list = [script_name,
                function_name,
                script_website,
                describe_fxn,
                details_fxn,
                depend_list,
                inputs,
                outputs]

    # Prompt for input if it was not provided to the function
    prompt_list = ['Provide script name: ',
                   'Provide function (module) name: ',
                   'Provide script Github website: ',
                   'Provide function description: ',
                   'Provide function details: ',
                   'Provide list of dependencies: ',
                   'Provide list of inputs: ',
                   'Provide list of outputs: ']

    # For loop cycles through each input and checks to see if it was provided
    # If it was not provided then it prompts for input
    for i in range(len(var_list)):
        if var_list[i] == "":
            print(function_name)
            var_list[i] = input(prompt_list[i])

    # Reassign variables
    script_name = var_list[0]
    function_name = var_list[1]
    script_website = var_list[2]
    describe_fxn = var_list[3]
    details_fxn = var_list[4]
    depend_list = var_list[5]
    inputs = var_list[6]
    outputs = var_list[7]

    # Reformat the inputs
    # Split the lines using word before the semicolon
    if isinstance(inputs, str) is True:
        split_inputs = inputs.split('\n')
    else:
        split_inputs = str(inputs)

    new_inputs = ''
    for line in split_inputs:
        if line == '':
            continue
        else:
            line = '* ' + line + '\n'
            new_inputs = new_inputs + line

    # Reformat the outputs by adding bullet point to front
    # Split the lines using word before the semicolon
    if isinstance(outputs, str) is True:
        split_outputs = outputs.split('\n')
    else:
        split_outputs = str(outputs)

    new_outputs = ''
    # Reformat the inputs
    for line in split_outputs:
        if line == '':
            continue
        else:
            line = '* ' + line + '\n'
            new_outputs = new_outputs + line

    # Reformat the dependencies with bullets
    if isinstance(depend_list,str) is True:
        split_dependencies = depend_list.split('\n')
    else:
        split_dependencies = str(depend_list)

    new_dependencies = ''
    for line in split_dependencies:
        if line == '':
            continue
        else:
            line = '* ' + line + '\n'
            new_dependencies = new_dependencies + line

    # Format the long documentation string
    docu_info = '''## Script: {script_name} \n 
### Function: {function_name} \n
[Link to {script_name} Code]({script_website}) \n
### **Description:** \n
{describe_fxn} \n
{details_fxn} 
### Dependencies \n
{depend_list} \n
### **Arguments:** \n
#### *Inputs* \n
{new_inputs}\n
#### *Outputs* \n
{new_outputs} \n
### **Examples:** \n
Helpful examples \n
[Back to Table of Contents](#table-of-contents) \n'''.format(script_name=script_name,
                   function_name=function_name,
                   script_website=script_website,
                   inputs=inputs,
                   outputs=outputs,
                   depend_list=new_dependencies,
                   describe_fxn=describe_fxn,
                   details_fxn=details_fxn,
                   new_outputs=new_outputs,
                   new_inputs=new_inputs)
    return docu_info

def batch_documentation(df_documentation='',path = ''):
    """
    Function::: batch_documentation
        Description: Creates series of documentation for functions in a repository
        Details: Creates series of documentation for functions in a repository

    Inputs
        df_documentation: DF Table with documentation inforamtion

    Outputs
        documentation.md file added to the repository

    Dependencies
        os
        create_documentation uscbrl labcodes
        table_of_contents uscbrl labcodes
    """
    # Dependencies
    from documentation.document_fxn import create_documentation
    import os.path
    from documentation.document_fxn import table_of_contents

    docu_csv = df_documentation

    # Make a .md File
    # open text file
    filename = os.path.join(path, 'documentation.md')
    file_exists = os.path.isfile(filename)

    # If the file doesn't exist
    if file_exists == False:
        text_file = open(filename, "x")
    # If the file does exist
    else:
        text_file = open(filename, "a")

    # Add the table of contents
    tab_cont_str = table_of_contents(df_documentation)
    text_file.write(tab_cont_str)

    # Use create_documentation function to cycle through each row and create the documentation
    docu_info_full = []
    for i in range(len(docu_csv)):
        docu_info_full = create_documentation(script_name=docu_csv.script_name[i],
                                              function_name=docu_csv.fxn_name[i],
                                              script_website=docu_csv.script_website[i],
                                              describe_fxn=docu_csv.fxn_desc[i],
                                              details_fxn =docu_csv.fxn_details[i],
                                              depend_list=docu_csv.fxn_depen[i],
                                              inputs=docu_csv.fxn_inputs[i],
                                              outputs=docu_csv.fxn_outputs[i])

        # write documentation information to the file
        text_file.write(docu_info_full)

    # close file
    text_file.close()


def table_of_contents(df_documentation=''):
    """
    Function::: table_of_contents
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        doc_csv_file: FILE csv file with documentation of functions

    Outputs
        tab_contents: STR Table of contents of functions in repository

    Dependencies

    """
    # Dependencies

    # Read in the documentation dataframe for the repository
    docu_csv = df_documentation

    # Create a list of strings in the correct format for each function
    str_fxns = ''

    for i in range(len(docu_csv)):
        str_fxns = str_fxns + '''|{description}|{script}|[{fxn}](#function-{fxn})| \n'''.format(description=docu_csv.fxn_desc[i],
            script=docu_csv.script_name[i],
            fxn=docu_csv.fxn_name[i])

    # Create the table of contents for a repository
    tab_contents = '''# Documentation- \n
## Table of Contents \n
|Description|Script|Functions| 
| ------------- | ------------- | ------------- | 
{all_fxns} \n
### End Table of Contents <br/> \n'''.format(all_fxns=str_fxns)

    return tab_contents