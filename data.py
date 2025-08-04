#%% LIB
import sqlite3
import pandas as pd
from datetime import datetime
import os

#%% CLASS
class SQLRepository:
    def __init__(self, connection):
        self.connection = connection
        
    def insert_table(self, table_name, records, if_exists='fail'):
        n_inserted = records.to_sql(
            name=table_name,
            con=self.connection,
            if_exists=if_exists
            )
        
        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
            }
    
    def database_overview(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_indatabase = cursor.fetchall()
        
        # Print out
        tables_indatabase = [n[0] for n in tables_indatabase]
        print("List of table in the database:")
        print(', '.join(tables_indatabase))
        
        
        for table in tables_indatabase:
            # Check number of observation
            cursor.execute(f"SELECT COUNT(*) FROM '{table}'")
            n_observations = cursor.fetchall()
            print(f"\nNumber of observation in {table} are: {n_observations[0][0]}")
           
            # Check columns in each table
            cursor.execute(f"PRAGMA table_info('{table}');")
            columns = cursor.fetchall()
            print(f"Columns in {table} are:")
            print(pd.DataFrame(columns)[[1, 2]])
            
        cursor.close()
#%% CREATE DATABASE

# GET DATA
df_knowledge_CTGDPT2018 = pd.read_csv('data_raw/knowledge_CTGDPT2018.csv')
df_question_format = pd.read_csv('data_raw/question_format.csv')
df_question_level = pd.read_csv('data_raw/question_level.csv')

# INSERT DATA
database_name = f"database_v{datetime.now().strftime('%Y%m%d')}.db"

## Check if previous ver. exists => Delete if so
if os.path.exists(database_name):
    os.remove(database_name)
    print(f"{database_name} has been deleted.")
else:
    print(f"{database_name} does not exist.")

## Create new database
connection = sqlite3.connect(
    database=database_name,
    check_same_thread=False
    )

repo = SQLRepository(connection)

repo.insert_table('KNOWLEDGE_CTGDPT2018', df_knowledge_CTGDPT2018)
repo.insert_table('QUES_FORMAT', df_question_format)
repo.insert_table('QUES_LEVEL', df_question_level)

# OVERVIEW
repo.database_overview()
