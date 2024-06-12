import sqlite3
from contextlib import closing

DATABASE = '/app/data/data.db'  # Cambia el nombre del archivo si es necesario

def query_db(query, args=(), one=False):
    with closing(sqlite3.connect(DATABASE)) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        r = cursor.fetchall()
        return (r[0] if r else None) if one else r
