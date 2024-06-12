import sqlite3
from contextlib import closing
import csv
import logging

DATABASE = '/app/data/data.db'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables():
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS process_header (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT,
                    insertion_date TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS etl_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    first_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    email TEXT,
                    phone TEXT,
                    username TEXT,
                    birth_date TEXT,
                    height REAL,
                    weight REAL,
                    eye_color TEXT,
                    hair_color TEXT,
                    hair_type TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    postal_code TEXT,
                    country TEXT,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS register_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    register INTEGER,
                    total INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS gender_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    gender TEXT,
                    total INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS age_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    age_range TEXT,
                    male INTEGER,
                    female INTEGER,
                    other INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS city_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    city TEXT,
                    male INTEGER,
                    female INTEGER,
                    other INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS os_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    os TEXT,
                    total INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')

def insert_summary_data(filename, summary_data):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO process_header (file_name, insertion_date)
                VALUES (?, date('now'))
            ''', (filename,))
            process_id = cursor.lastrowid

            current_table = None
            for row in summary_data:
                if len(row) == 2 and row[0] == 'register':
                    current_table = 'register_data'
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, register, total)
                        VALUES (?, ?, ?)
                    ''', (process_id, row[0], row[1]))
                elif len(row) == 2 and row[0] in ['male', 'female', 'other']:
                    current_table = 'gender_data'
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, gender, total)
                        VALUES (?, ?, ?)
                    ''', (process_id, row[0], row[1]))
                elif len(row) == 4 and row[0] == 'age':
                    current_table = 'age_data'
                    continue
                elif len(row) == 4 and current_table == 'age_data' and row[0] != 'City':
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, age_range, male, female, other)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (process_id, row[0], row[1], row[2], row[3]))
                elif len(row) == 4 and row[0] == 'City':
                    current_table = 'city_data'
                    continue
                elif len(row) == 4 and current_table == 'city_data':
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, city, male, female, other)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (process_id, row[0], row[1], row[2], row[3]))
                elif len(row) == 2 and row[0] == 'OS':
                    current_table = 'os_data'
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, os, total)
                        VALUES (?, ?, ?)
                    ''', (process_id, row[0], row[1]))
                elif len(row) == 2 and row[0] in ['Windows', 'Apple', 'Linux']:
                    cursor.execute(f'''
                        INSERT INTO {current_table} (process_id, os, total)
                        VALUES (?, ?, ?)
                    ''', (process_id, row[0], row[1]))

def insert_etl_data(filename, etl_data):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO process_header (file_name, insertion_date)
                VALUES (?, date('now'))
            ''', (filename,))
            process_id = cursor.lastrowid
            for row in etl_data:
                cursor.execute('''
                    INSERT INTO etl_data (
                        process_id, first_name, last_name, age, gender, email, phone,
                        username, birth_date, height, weight, eye_color, hair_color,
                        hair_type, address, city, state, postal_code, country
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    process_id, row['firstName'], row['lastName'], row['age'], row['gender'], row['email'],
                    row['phone'], row['username'], row['birthDate'], row['height'], row['weight'],
                    row['eyeColor'], row['hairColor'], row['hairType'], row['address'], row['city'],
                    row['state'], row['postalCode'], row['country']
                ))

def csv_to_dict_list(csv_content):
    reader = csv.DictReader(csv_content.splitlines())
    return [row for row in reader]

def csv_to_list(csv_content):
    reader = csv.reader(csv_content.splitlines())
    return [row for row in reader]

def process_file(filename, content):
    create_tables()
    if 'summary_' in filename:
        summary_data = csv_to_list(content)
        insert_summary_data(filename, summary_data)
    elif 'ETL_' in filename:
        etl_data = csv_to_dict_list(content)
        insert_etl_data(filename, etl_data)
