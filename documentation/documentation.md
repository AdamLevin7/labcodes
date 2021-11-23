    ## Script: document_fxn.py 
 
    ### Function: scrape_documentation 

    [Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 

    

    ### **Keywords:** 

    nan 

    

    ###Syntax:** 

    ``` 

    from document_fxn.py import scrape_documentation 

    

        Outputs
        output1: FILE .csv file containing updated documentation information


 = scrape_documentation(    Inputs
        code_script: STR Code script with documentation info
        doc_codes_csv: STR .csv file containing documentation information

) 

    ```` 

    ### Dependencies 

        Dependencies
        pandas
        tkinter

 

    

    ### **Description:** 

            Description: Scrape a code script for documentation info
 

            Details: Scrape code for documentation information.
        Write that data into .csv file

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

        Inputs
        code_script: STR Code script with documentation info
        doc_codes_csv: STR .csv file containing documentation information


    

    

    #### *Outputs* 

        Outputs
        output1: FILE .csv file containing updated documentation information


 

    

     

    ### **Examples:** 

    Helpful examples 

    

    [Back to Table of Contents](#table-of-contents) 

             ## Script: document_fxn.py 
 
    ### Function: gather_scripts 

    [Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 

    

    ### **Keywords:** 

    nan 

    

    ###Syntax:** 

    ``` 

    from document_fxn.py import gather_scripts 

    

        Outputs
        doc_csv_file: FILE Where documentation data is stored (.csv file)

 = gather_scripts(    Inputs
        extensions: TUPLE Specify the extensions to document in repo
        doc_csv_file: STR Path where .csv file with documentation info is stored

) 

    ```` 

    ### Dependencies 

        Dependencies
        os
        tkinter
        dep3 from uscbrl_script.py (USCBRL repo)
 

    

    ### **Description:** 

        	Description: List scripts in repository and scrape documentation information.
 

        	Details: Create list of scripts in the repository that you will create documentation
    	for, regenerate the table

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

        Inputs
        extensions: TUPLE Specify the extensions to document in repo
        doc_csv_file: STR Path where .csv file with documentation info is stored


    

    

    #### *Outputs* 

        Outputs
        doc_csv_file: FILE Where documentation data is stored (.csv file)

 

    

     

    ### **Examples:** 

    Helpful examples 

    

    [Back to Table of Contents](#table-of-contents) 

             ## Script: document_fxn.py 
 
    ### Function: create_documentation 

    [Link to document_fxn.py Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.py) 

    

    ### **Keywords:** 

    nan 

    

    ###Syntax:** 

    ``` 

    from document_fxn.py import create_documentation 

    

    nan = create_documentation(    Inputs
        script_name: STR Name of the script containing the function
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

            depend_list: LIST Dependencies needed to run the function
        inputs: LIST Input variable names and descriptions
        outputs: LIST Output variable names and descriptions

    Outputs
        docu_info: STR Documentation information as a long string?

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
 

    

    ### **Description:** 

        	Description: Create Github documentation format for functions
 

        	Details: Create Github documentation including inputs, outputs, dependencies, how to run the function etc.

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

        Inputs
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

    

    ###Syntax:** 

    ``` 

    from document_fxn.py import batch_documentation 

    

        Outputs
        Batch of Github markdown outputs for repository documentation

 = batch_documentation(    Inputs
        doc_codes_csv: STR .csv input file directory containing information

) 

    ```` 

    ### Dependencies 

        Dependencies
        tkinter
        pandas
 

    

    ### **Description:** 

            Description: Creates series of documentation for functions in a repository
 

            Details: Creates series of documentation for functions in a repository

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

        Inputs
        doc_codes_csv: STR .csv input file directory containing information


    

    

    #### *Outputs* 

        Outputs
        Batch of Github markdown outputs for repository documentation

 

    

     

    ### **Examples:** 

    Helpful examples 

    

    [Back to Table of Contents](#table-of-contents) 

             ## Script: document_fxn.R 
 
    ### Function: batch_documentation 

    [Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 

    

    ### **Keywords:** 

    nan 

    

    ###Syntax:** 

    ``` 

    from document_fxn.R import batch_documentation 

    

    Outputs
    Batch of Github markdown outputs for repository documentation

 = batch_documentation(Inputs
    doc_codes_csv: STR .csv input file directory containing information


) 

    ```` 

    ### Dependencies 

    Dependencies
    create_documentation USCBRL Repo: labcodes
 

    

    ### **Description:** 

    	Description: Creates series of documentation for functions in a repository
 

    	Details: Creates series of documentation for functions in a repository

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

    Inputs
    doc_codes_csv: STR .csv input file directory containing information



    

    

    #### *Outputs* 

    Outputs
    Batch of Github markdown outputs for repository documentation

 

    

     

    ### **Examples:** 

    Helpful examples 

    

    [Back to Table of Contents](#table-of-contents) 

             ## Script: document_fxn.R 
 
    ### Function: create_documentation 

    [Link to document_fxn.R Code](https://github.com/USCBiomechanicsLab/labcodes/blob/master/documentation/document_fxn.R) 

    

    ### **Keywords:** 

    nan 

    

    ###Syntax:** 

    ``` 

    from document_fxn.R import create_documentation 

    

    nan = create_documentation(Inputs
    script_name: STR Name of the script containing the function
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

        depend_list: LIST Dependencies needed to run the function
    inputs: LIST Input variable names and descriptions
    outputs: LIST Output variable names and descriptions

Outputs
    Prints Github markdown output to generate Github documentation

Dependencies
    None
 

    

    ### **Description:** 

    	Description: Creates Github markdown script for documenting a function
 

    	Details: Add details

 

    

    

    ### **Arguments:** 

    

    #### *Inputs* 

    Inputs
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

         