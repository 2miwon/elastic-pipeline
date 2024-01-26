import sqlite3

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def get_db_connection(db_path: str):
    return sqlite3.connect(db_path, check_same_thread=False)

def get_db_cursor(db_path: str):
    connect = sqlite3.connect(db_path, check_same_thread=False)
    return connect.cursor()