#%% LIB
import sqlite3
import pandas as pd
pd.set_option('display.max_columns', None)
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
        
    def get_grade_list(self):
        query = "SELECT grade FROM KNOWLEDGE_CTGDPT2018"
        return list(
            pd.read_sql(
                sql=query,
                con=self.connection
                )['grade'].unique()
            )
        
    def get_subject_list(self):
        query = "SELECT subject FROM KNOWLEDGE_CTGDPT2018"
        return list(
            pd.read_sql(
                sql=query,
                con=self.connection
                )['subject'].unique()
            )
        
    def get_author_list(self):
        query="SELECT author FROM KNOWLEDGE_CTGDPT2018"
        return list(
            pd.read_sql(
                sql=query,
                con=self.connection
                )['author'].unique()
            )
        
    def get_lesson_list(self, subject, grade, author):
        query = """
            SELECT lesson 
            FROM KNOWLEDGE_CTGDPT2018 
            WHERE subject=? AND grade=? AND author=?
            """
        
        return list(
            pd.read_sql(
                sql=query,
                con=self.connection,
                params=(subject, int(grade), author)
                )['lesson'].unique()
            )
        
    def get_knowledge(self, subject, grade, author, lesson):
        query = """
            SELECT knowledge 
            FROM KNOWLEDGE_CTGDPT2018 
            WHERE subject=? AND grade=? AND author=? AND lesson=?
            """
        
        return pd.read_sql(
                sql=query,
                con=self.connection,
                params=(subject, int(grade), author, lesson)
                )['knowledge'].unique()[0]
            
        
        
        
        
        
        
#%% CREATE DATABASE

# GET DATA
df_knowledge_CTGDPT2018 = pd.read_csv('data_raw/knowledge_CTGDPT2018.csv')
df_question_format = pd.read_csv('data_raw/question_format.csv')
df_question_level = pd.read_csv('data_raw/question_level.csv')

# INSERT DATA
## Remove previous version
database_pre_ver = [file for file in os.listdir() if '.db' in file]
for file in database_pre_ver:
    os.remove(file)
    print(f"{file} has been deleted.")

## Create new database

database_name = f"database_v{datetime.now().strftime('%Y%m%d')}.db"
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

#%% TEST DATABASE
database_name = f"database_v{datetime.now().strftime('%Y%m%d')}.db"

connection = sqlite3.connect(
    database=database_name,
    check_same_thread=False
    )

repo = SQLRepository(connection)
repo.get_grade_list()
repo.get_author_list()

repo.get_lesson_list('Toán', 6, 'Cánh Diều')
repo.get_knowledge('Toán', 6, 'Cánh Diều', 'Đoạn thẳng')

list(pd.read_sql(sql="SELECT subject FROM KNOWLEDGE_CTGDPT2018", con=connection)['subject'].unique())
