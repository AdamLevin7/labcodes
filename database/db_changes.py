"""
Script: db_changes
    Make changes to a database.

Modules
    check_column_names: Check if a column name is within a database table.
    check_column_exist: Check if a column exists in a database table.


Author:
    Casey Wiens
    cwiens32@gmail.com
"""

def check_column_names(engine, table_name, df_in):
    """
    Function::: check_column_names
    	Description: Check if a column name is within a database table.
    	Details: Check if a column exists in a database table so a new data can be appended.

    Inputs
        engine: ENGINE Database engine for connection
        table_name: STR Name of the table you are checking in the database
        df_in: DATAFRAME Table you are trying to add to existing database table

    Outputs
        Print line if new column was added

    Dependencies
        sqlalchemy
        pandas
    """
    # Dependencies
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
    Function::: check_column_exist
    	Description: Check if a column exists in a database table.
    	Details: Check if a column exists in a db table and if not, create it.

    Inputs
        engine: ENGINE Database engine for connection
        table_name: STR Name of the table you are checking in the database
        col_name: STR Name of the column you are checking for
        col_type: STR Datatype in quotes that you want the column to be (ie. Float, INT)

    Outputs
        Adds column to database table if it didn't exist

    Dependencies
        sqlalchemy
        pandas

    """

    # Dependencies
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