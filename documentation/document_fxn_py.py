"""
Script: document_fxn_py
    Create documentation functions for Github documentation.

Modules
    scrape_documentation: Scrape a code script for documentation info

Author:
    Harper Stewart
    harperestewart7@gmail.com
"""


def scrape_documentation(code_script = '', doc_codes_csv = ''):
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
    doc_csv_file = askopenfilename()
    documentation_csv = pd.read_csv(doc_csv_file)

    # Read in the file of the code which contains the documentation information
    if code_script == '':
        code_script = askopenfilename()
        code_text = open(code_script)
    else:
        code_text  = open(code_script)

    # Get the script name
    split_script = code_script.split('/')
    script_name = split_script[-1]

    # Inititalize the list
    info_list = []
    # For loop to append each line to a list
    for line in code_text:
        info_list.append(line)

    # Find indexes where Function:x3 occurs in the list:'
    fxn_pos_list = [i for i in range(len(info_list)) if ' Function:::' in info_list[i]]
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
        fxn_name = fxn_name_2.replace("\n", "")

        # Get information closest to that function index
        desc_loc = min([i for i in desc_pos_list if i > ind])
        details_loc = min([i for i in details_pos_list if i > ind])
        input_loc = min([i for i in input_pos_list if i > ind])
        output_loc = min([i for i in output_pos_list if i > ind])
        depend_loc = min([i for i in depend_pos_list if i > ind])
        docstring_loc = min([i for i in docstr_pos_list if i > ind])

        # Get the variables
        fxn_desc = info_list[desc_loc]

        # Join elements of the list to create full detail string
        fxn_details = ''.join(info_list[details_loc:input_loc])


        fxn_inputs =''.join(info_list[input_loc:output_loc])
        fxn_outputs = ''.join(info_list[output_loc:depend_loc])
        fxn_depen = ''.join(info_list[depend_loc:docstring_loc])


 # Write that information out to the .csv file

    # TODO Figure out a way to pull the Github site
    script_website = 'test.web.github'

    # TODO Create function that pulls keywords for the function
    # Placeholder for now to write out to the csv file
    # Pull the most common words for that function to use as the keywords* ??

    # Remove row in table if the function was already documented to update
    if documentation_csv['fxn_name'].str.contains(fxn_name).any():
        documentation_csv[~documentation_csv.fxn_name.str.contains(fxn_name)]

    # TODO Create row for that specific function

    new_row = pd.DataFrame([[script_name,
                             fxn_name,
                             script_website,
                             fxn_desc, fxn_details,fxn_depen,fxn_inputs,
                                                       fxn_outputs]],
                           columns = ['script_name',
                                                       'fxn_name',
                                                       'script_website',
                                                       'fxn_desc',
                                                       'fxn_details',
                                                       'fxn_depen',
                                                       'fxn_inputs',
                                                       'fxn_outputs'
                                                       ])

    # Append that row to the table for documentation
    frames = [documentation_csv, new_row]
    documentation_csv = pd.concat(frames)


#TODO Write the table back out to .csv file
documentation_csv.to_csv(doc_csv_file, index = False)







