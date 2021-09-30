"""
Script: script_name
    Description of the overall purpose of the script.

Modules
    module_1: module description here
    module_2: module description here
    module_3: module description here
    module_4: module description here

Author:
    FirstName LastName
    email
"""

def check_column_names(engine, table_name, df_in):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """
    import sqlalchemy as db
    import pandas as pd

    # set query to grab column names from table in database
    qry = '''
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{}'
        ORDER BY ORDINAL_POSITION
        '''.format(table_name)
    # execute statement
    col_names = pd.read_sql(qry, engine)
    # loop through new column names and add to database
    for newcol in df_in.columns:
        if newcol not in col_names.COLUMN_NAME.to_numpy():
            # set data type of column
            if df_in[[newcol]].dtypes[0] == 'float64':
                settype = "FLOAT"
            elif df_in[[newcol]].dtypes[0] == 'int64':
                settype = "BIGINT"
            with engine.connect() as con:
                # set query
                qry = '''
                    ALTER TABLE {}
                    ADD {} {} 
                    '''.format(table_name, newcol, settype)
                # execute statement
                con.execute(db.text(qry))
            # message new columns were added
            print("New column was added! Table: " + table_name + " Column: " + newcol)

def check_column_exist(engine, table_name, col_name, col_type):
    """
    Function::: name_of_function
    	Description: brief description here (1 line)
    	Details: Full description with details here

    Inputs
        input1: DATATYPE description goes here (units)
        input2: DATATYPE description goes here (units)
        input3: DATATYPE description goes here (units)
        input4: DATATYPE description goes here (units)

    Outputs
        output1: DATATYPE description goes here (units)
        output2: DATATYPE description goes here (units)
        output3: DATATYPE description goes here (units)
        output4: DATATYPE description goes here (units)

    Dependencies
        dep1
        dep2
        dep3 from uscbrl_script.py (USCBRL repo)
    """

    # Packages
    import sqlalchemy as db
    import pandas as pd

    # set query to grab column names from table in database
    qry = '''
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{}'
        ORDER BY ORDINAL_POSITION
        '''.format(table_name)
    # execute statement
    col_names = pd.read_sql(qry, engine)
    # check if column name is in table
    if col_name not in col_names.COLUMN_NAME.to_numpy():
        # set data type of column
        if col_type == 'float64' or col_type.lower() == "float":
            settype = "FLOAT"
        elif col_type == 'int64' or col_type.lower() == "bigint":
            settype = "BIGINT"
        with engine.connect() as con:
            # set query
            qry = '''
                ALTER TABLE {}
                ADD {} {} 
                '''.format(table_name, col_name, settype)
            # execute statement
            con.execute(db.text(qry))
        # message new columns were added
        print("New column was added! Table: " + table_name + " Column: " + col_name)

