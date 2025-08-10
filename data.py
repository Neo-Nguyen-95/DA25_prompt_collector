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
                )['knowledge'][0]
    
    def get_cong_van(self, cong_van, section):
        query = """
            SELECT content
            FROM CONG_VAN
            WHERE cong_van=? AND section=?
        """   
        
        return pd.read_sql(
            sql=query,
            con=self.connection,
            params=(cong_van, section)
            )['content'][0]
        
    def get_item_info(self):
        return """*** Trắc nghiệm nhiều lựa chọn: Có 4 lựa chọn, học sinh cần chọn 1 đáp án đúng. Ví dụ: 
Câu 1 (M1). Quốc gia nào sau đây có hơn 10.000 bãi biển?
A. Úc (đúng)
B. Anh
C. Pháp
D. Italia
*** Trắc nghiệm đúng sai: Mỗi câu có 4 khẳng định, học sinh xét tính đúng sai của mỗi khẳng định. Không được thiết kế tất cả đúng hoặc tất cả sai. Ví dụ: 
Câu 2 (M2). Vật rơi tự do gần bề mặt Trái Đất, bỏ qua ma sát:
a) Vận tốc tăng đều theo thời gian.
b) Gia tốc không đổi và bằng 9.8 m/s².
c) Đường đi là đường cong.
d) Trong chân không, tất cả vật rơi cùng gia tốc.
Học sinh đánh dấu từng ý: Đúng/Sai
*** Trắc nghiệm trả lời ngắn: HS viết nội dung ngắn gọn trả lời. Vị trí điền cần sử dụng kí hiệu ___. Câu dẫn ghi rõ dạng của số hoặc từ cần điền. Ví dụ: 
Câu 3 (M3). Điền số tự nhiên thích hợp vào ô trống:
Khi một chất từ dung dịch đậm đặc khuếch tán sang dung dịch loãng, hiện tượng gọi là __.
        """
    
    def get_item_diff(self):
        return """*** Mức 1: Nhận biết, nhắc lại hoặc mô tả được nội dung đã học và áp dụng trực tiếp để giải quyết một số tình huống, vấn đề quen thuộc trong học tập;
*** Mức 2: Kết nối, sắp xếp được một số nội dung đã học để giải quyết vấn đề có nội dung tương tự;
*** Mức 3: Vận dụng các nội dung đã học để giải quyết một số vấn đề mới hoặc đưa ra những phản hồi hợp lý trong học tập và cuộc sống.
    """
        
        
        
        
#%% CREATE DATABASE

# GET DATA
df_knowledge_CTGDPT2018 = pd.read_csv('data_raw/knowledge_CTGDPT2018.csv')
df_cong_van = pd.read_csv('data_raw/cong_van.csv')

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
repo.insert_table('CONG_VAN', df_cong_van)

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
repo.get_cong_van('5512/BGDĐT-GDTrH', 'khung khbd')

# list(pd.read_sql(sql="SELECT subject FROM KNOWLEDGE_CTGDPT2018", con=connection)['subject'].unique())
