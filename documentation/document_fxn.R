# Title     : Documentation Functions
# Objective : Create a script that outputs documentation markdowns
# Created by: hestewar, harperestewart7@gmail.com
# Created on: 8/17/2021

# TODO make it into an actual function
# TODO decide on a template for documentation
# TODO make a list of existing documentation codes (put in a database table?)
# TODO Make documentation format for all codes, specify the keywords/things to search for
# TODO Read that information as the inputs to this function
# TODO make things into lists to regenerate documentation links and reflect updates (loop a list)
# TODO make a documentation package (not necessary but fun)

# Gather input variables or make a normal function*
# Ask for input if nothing is provided

script_name <- "blah"
function_name <- "blah_function"
script_website <- 'blah_blah.com'
keywords <- "blah_keyword"
describe_fxn <- "describe blah blah blah"
depend_list <- "dEPenDenCies"
inputs <- "input1 , input 2"
outputs <- "output 1, output 7"

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
