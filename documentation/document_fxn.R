# Title     : Documentation Functions
# Objective : Create a script that outputs documentation markdowns
# Created by: hestewar, harperestewart7@gmail.com
# Created on: 8/17/2021

# TODO make a list of existing documentation codes (put in a csv file that stays with labcodes)
# TODO Make documentation format for all codes, specify the keywords/things to search for
# TODO Read that information as the inputs to this function
# TODO make things into lists to regenerate documentation links and reflect updates (loop a list)
# TODO make a documentation package (not necessary but fun)

# Other thoughs, documentation becomes a folder within each repository
# Contains: .csv of the codes and docu info, github markdown of all of the documentation

batch_documentation <- function(doc_codes_csv, repo){
  # Function::: batch_documentation
  # Creates series of documentation for functions in a repository

  # Inputs
  # doc_codes_csv: STR .csv input file containing information
  # repo: STR Name of repository

  # Outputs
  # Batch of Github markdown outputs for repository documentation

  # Dependencies
  # None

  #TODO Read in the .csv file

  #TODO Use create_documentation function to cycle through each row and create the documentation


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
  # Github markdown output to generate Github documentation

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
