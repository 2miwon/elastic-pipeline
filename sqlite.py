import sqlite3
from config import *
from module import *

def insert_data_end(connect: sqlite3.Connection):
    connect.commit()
    connect.close()

def db_init_check():
    conn = get_db_connection(DB_FILE_PATH)
    conn.cursor().execute('''
        CREATE TABLE IF NOT EXISTS bills (
            bill_no TEXT PRIMARY KEY,
            bill_id TEXT,
            raw_file_link TEXT,
            title TEXT
        )
    ''')
    insert_data_end(conn)

def insert_bill_metadata(bill_no: str, bill_id: str, raw_file_link: str, title: str):
    conn = get_db_connection(DB_FILE_PATH)
    conn.cursor().execute('''
        INSERT INTO bills (bill_no, bill_id, raw_file_link, title)
        VALUES (?, ?, ?, ?)
    ''', (bill_no, bill_id, raw_file_link, title))
    insert_data_end(conn)

def read_bill_metadata_by_bill_no(bill_no: str):
    conn = get_db_connection(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bills WHERE bill_no = ?
    ''', (bill_no,))
    row = cursor.fetchone()
    conn.close()
    return row

def read_all_bill_metadata():
    conn = get_db_connection(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bills
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows 

def get_bill_file_link_by_bill_no(bill_no: str):
    conn = get_db_connection(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT raw_file_link FROM bills WHERE bill_no = ?
    ''', (bill_no,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_bill_title_by_bill_no(bill_no: str):
    conn = get_db_connection(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT title FROM bills WHERE bill_no = ?
    ''', (bill_no,))
    row = cursor.fetchone()
    conn.close()
    return row
