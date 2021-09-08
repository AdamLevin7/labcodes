# Title     : Documentation Functions
# Objective : Create functions that help outputs documentation markdowns in Github
# Created by: hestewar, harperestewart7@gmail.com
# Created on: 8/17/2021

# TODO Go through the functions and make sure format matches
# TODO Scrape all of those files and put them into .csv
# TODO Make a way to generate/update the table of contents automatically
# TODO make things into lists to regenerate documentation links and reflect updates (loop a list)
# TODO make a documentation package (not necessary but fun)

# Other thoughs, documentation becomes a folder within each repository
# Contains: .csv of the codes and docu info, github markdown of all of the documentation

batch_documentation <- function(doc_codes_csv =''){
  # Function::: batch_documentation
  # Creates series of documentation for functions in a repository

  # Inputs
  # doc_codes_csv: STR .csv input file directory containing information

  # Outputs
  # Batch of Github markdown outputs for repository documentation

  # Dependencies
  # create_documentation USCBRL Repo: labcodes

  # Dependencies
  if (doc_codes_csv == ""){
    print("Select document_fxn R code with functions")
    source(file.choose())
  }

  # Read in the .csv file
  print("Select .csv file containing documentation information")
  funct_tab <- read.csv(file.choose())

  # Use create_documentation function to cycle through each row and create the documentation
  for (i in 1:nrow(funct_tab)) {
    create_documentation(script_name = funct_tab[["script_name"]][i],
                                 function_name= funct_tab[["function_name"]][i],
                                 script_website= funct_tab[["script_website"]][i],
                                 keywords= funct_tab[["keywords"]][i],
                                 describe_fxn= funct_tab[["describe_fxn"]][i],
                                 depend_list= funct_tab[["depend_list"]][i],
                                 inputs= funct_tab[["inputs"]][i],
                                 outputs= funct_tab[["outputs"]][i])
  # End loop here
  }

    # End function here
}

create_documentation <- function(script_name = '',
                                 function_name= '',
                                 script_website= '',
                                 keywords= '',
                                 describe_fxn= '',
                                 depend_list= '',
                                 inputs= '',
                                 outputs= ''){

  # Function::: create_documentation
  # Creates Github markdown script for documenting a function
  # More details?

  # Inputs
  # script_name: STR Name of the script containing the function
  # function_name: STR Name of the specific function (module)
  # script_website: STR Github website of the script
  # keywords: STR keywords associated with the function
  # describe_fxn: STR Description of the function
  # depend_list: LIST Dependencies needed to run the function
  # inputs: LIST Input variable names and descriptions
  # outputs: LIST Output variable names and descriptions

  # Outputs
  # Prints Github markdown output to generate Github documentation

  # Dependencies
  # None

  # Test to see if all variables were provided
  var_list <- list(script_name,
                   function_name,
                   script_website,
                   keywords,
                   describe_fxn,
                   depend_list,
                   inputs,
                   outputs)

  # Prompt for input if it was not provided to the function
  prompt_list <- list('Provide script name: ',
                      'Provide function (module) name: ',
                      'Provide script Github website: ',
                      'Provide function keywords: ',
                      'Provide function description: ',
                      'Provide list of dependencies: ',
                      'Provide list of inputs: ',
                      'Provide list of outputs: ')

  # For loop cycles through each input and checks to see if it was provided
    # If it was not provided then it prompts for input
  for (i in 1:length(var_list)) {
    if (var_list[i] == ""){
      var_list[i] <- readline(prompt= prompt_list[i])}
  }

  # Reassign variables
  script_name <- var_list[[1]]
  function_name<- var_list[[2]]
  script_website <- var_list[[3]]
  keywords<- var_list[[4]]
  describe_fxn<- var_list[[5]]
  depend_list<-  var_list[[6]]
  inputs<- var_list[[7]]
  outputs<- var_list[[8]]

  # Concatenate the lines together
cat(paste0("
## Script: ", script_name, "\n",
"### Function ", function_name, "\n",
"[Link to ", script_name, " Code](", script_website, ")", "\n",
"\n",
"### **Keywords:**", "\n",
keywords, "\n",
"\n",
"### **Syntax:**", "\n",
"```" , "\n",
"from ", script_name," import ", function_name, "\n",
"\n",
outputs, " = ", function_name, "(", inputs, ")", "\n",
"```" , "\n",
"### Dependencies", "\n",
 depend_list, "\n",
   # TODO make a for loop here that allows you to format multiple dependencies
"\n",
"### **Description:**", "\n",
describe_fxn, "\n",
"\n",
"### **Arguments:**","\n",
"\n",
"#### *Inputs*", "\n",
   # TODO make a for loop to format the inputs the way you want them
   inputs, "\n",
"\n",
"#### *Outputs*", "\n",
   # TODO make a for loop to format the outputs the way you want them
   outputs, "\n",
"\n",
"### **Examples:**", "\n",
"Helpful examples", "\n",
"\n",
"[Back to Table of Contents](#table-of-contents)"
))

}

scrape_documentation <- function(code_script ='', doc_codes_csv ='' ){

#Function::: scrape_documentation
#	Scrape documentation information from scripts
#	Way to scrape documentation data from scripts, be sure to use the associated template.
  # this will add the function information to the .csv documentation file for the repository.
#
#Inputs
#    input1: DATATYPE description goes here (units)
#    input2: DATATYPE description goes here (units)
#    input3: DATATYPE description goes here (units)
#    input4: DATATYPE description goes here (units)
#
#Outputs
#    output1: DATATYPE description goes here (units)
#    output2: DATATYPE description goes here (units)
#    output3: DATATYPE description goes here (units)
#    output4: DATATYPE description goes here (units)
#
#Dependencies
#    dep1
#    dep2
#    dep3 from uscbrl_script.py (USCBRL repo)


  # Read in the file of the code which contains the documentation information
   if (code_script == ""){
    print("Select script to scrape documentation information: ")
    code_script <- read.delim(file.choose())} else {
     code_script <- read.delim(code_script)
   }

  # Read in the .csv file (if it exists) containing already documented codes
  if (doc_codes_csv == ""){
    print("Select document_fxn R code with functions: ")
    funct_tab <- read.csv(file.choose())} else {
     funct_tab <- read.delim(doc_codes_csv)
   }

  #TODO Find the functions within the script
    #TODO Make sure this is set up in a loop to handle multiple functions in one script
  #TODO Scrape the information that you need and assign it to variables
  #TODO check if those functions exist within the .csv table (if not then append to .csv)
  #TODO Assign those variables to a row in a table
  #TODO Append or update a .csv file with that information


}


