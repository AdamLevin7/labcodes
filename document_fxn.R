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

script_name <- "blah"
function_name <- "blah_function"
script_website <- 'blah_blah.com'
keywords <- "blah_keyword"
describe_fxn <- "describe blah blah blah"
depend_list <- "dEPenDenCies"
inputs <- "input1 , input 2"
outputs <- "output 1, output 7"

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


