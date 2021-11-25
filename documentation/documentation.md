# Documentation- 

## Table of Contents 

|Description|Script|Functions| 
| ------------- | ------------- | ------------- | 
|	Check if a column name is within a database table.|db_changes.py|[check_column_names](#function-check_column_names)| 
|	Check if a column exists in a database table.|db_changes.py|[check_column_exist](#function-check_column_exist)| 
|	Check if a column name is within a database table.|db_changes.py|[check_column_names](#function-check_column_names)| 
|	Check if a column exists in a database table.|db_changes.py|[check_column_exist](#function-check_column_exist)| 
 

### End Table of Contents <br/> 
## Script: db_changes.py 
 
### Function: check_column_names 

[Link to db_changes.py Code](https://github.com/Codes-USCBiomechanicsLab/labcodes/blob/master/database/db_changes.py) 

### **Syntax:** 

``` 
*Need to fix this*
from db_changes.py import check_column_names 

Print line if new column was added

 = check_column_names(engine: ENGINE Database engine for connection
table_name: STR Name of the table you are checking in the database
df_in: DATAFRAME Table you are trying to add to existing database table

) 

```` 

### Dependencies 

sqlalchemy
pandas
 

### **Description:** 

	Check if a column name is within a database table. 

    	Check if a column exists in a database table so a new data can be appended.

 

### **Arguments:** 

#### *Inputs* 

* engine: ENGINE Database engine for connection
* table_name: STR Name of the table you are checking in the database
* df_in: DATAFRAME Table you are trying to add to existing database table


#### *Outputs* 

* Print line if new column was added
 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: db_changes.py 
 
### Function: check_column_exist 

[Link to db_changes.py Code](https://github.com/Codes-USCBiomechanicsLab/labcodes/blob/master/database/db_changes.py) 

### **Syntax:** 

``` 
*Need to fix this*
from db_changes.py import check_column_exist 

Adds column to database table if it didn't exist

 = check_column_exist(engine: ENGINE Database engine for connection
table_name: STR Name of the table you are checking in the database
col_name: STR Name of the column you are checking for
col_type: STR Datatype in quotes that you want the column to be (ie. Float, INT)

) 

```` 

### Dependencies 

sqlalchemy
pandas

 

### **Description:** 

	Check if a column exists in a database table. 

    	Check if a column exists in a db table and if not, create it.

 

### **Arguments:** 

#### *Inputs* 

* engine: ENGINE Database engine for connection
* table_name: STR Name of the table you are checking in the database
* col_name: STR Name of the column you are checking for
* col_type: STR Datatype in quotes that you want the column to be (ie. Float, INT)


#### *Outputs* 

* Adds column to database table if it didn't exist
 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: db_changes.py 
 
### Function: check_column_names 

[Link to db_changes.py Code](https://github.com/Codes-USCBiomechanicsLab/labcodes/blob/master/database/db_changes.py) 

### **Syntax:** 

``` 
*Need to fix this*
from db_changes.py import check_column_names 

Print line if new column was added

 = check_column_names(engine: ENGINE Database engine for connection
table_name: STR Name of the table you are checking in the database
df_in: DATAFRAME Table you are trying to add to existing database table

) 

```` 

### Dependencies 

sqlalchemy
pandas
 

### **Description:** 

	Check if a column name is within a database table. 

    	Check if a column exists in a database table so a new data can be appended.

 

### **Arguments:** 

#### *Inputs* 

* engine: ENGINE Database engine for connection
* table_name: STR Name of the table you are checking in the database
* df_in: DATAFRAME Table you are trying to add to existing database table


#### *Outputs* 

* Print line if new column was added
 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
## Script: db_changes.py 
 
### Function: check_column_exist 

[Link to db_changes.py Code](https://github.com/Codes-USCBiomechanicsLab/labcodes/blob/master/database/db_changes.py) 

### **Syntax:** 

``` 
*Need to fix this*
from db_changes.py import check_column_exist 

Adds column to database table if it didn't exist

 = check_column_exist(engine: ENGINE Database engine for connection
table_name: STR Name of the table you are checking in the database
col_name: STR Name of the column you are checking for
col_type: STR Datatype in quotes that you want the column to be (ie. Float, INT)

) 

```` 

### Dependencies 

sqlalchemy
pandas

 

### **Description:** 

	Check if a column exists in a database table. 

    	Check if a column exists in a db table and if not, create it.

 

### **Arguments:** 

#### *Inputs* 

* engine: ENGINE Database engine for connection
* table_name: STR Name of the table you are checking in the database
* col_name: STR Name of the column you are checking for
* col_type: STR Datatype in quotes that you want the column to be (ie. Float, INT)


#### *Outputs* 

* Adds column to database table if it didn't exist
 

### **Examples:** 

Helpful examples 

[Back to Table of Contents](#table-of-contents) 
