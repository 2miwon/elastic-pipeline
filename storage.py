import sqlite3
import os 

db_file_path = f'{os.getcwd()}/sqlite/database.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

def db_init_check():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            bill_no TEXT PRIMARY KEY,
            bill_id TEXT,
            raw_file_name TEXT,
        )
    ''')