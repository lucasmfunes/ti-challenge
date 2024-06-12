import sqlite3
from contextlib import closing
import csv
import logging

DATABASE = '/app/data/data.db'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create tables
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
                CREATE TABLE IF NOT EXISTS summary_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_id INTEGER,
                    register INTEGER,
                    male INTEGER,
                    female INTEGER,
                    other INTEGER,
                    FOREIGN KEY (process_id) REFERENCES process_header(id)
                )
            ''')

# Insert summary data into the database
def insert_summary_data(filename, summary_data):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO process_header (file_name, insertion_date)
                VALUES (?, datetime('now'))
            ''', (filename,))
            process_id = cursor.lastrowid
            for row in summary_data:
                if len(row) == 2:
                    cursor.execute('''
                        INSERT INTO summary_data (process_id, register, male, female, other)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (process_id, row[1], 0, 0, 0))
                elif len(row) == 4:
                    cursor.execute('''
                        INSERT INTO summary_data (process_id, register, male, female, other)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (process_id, 0, row[1], row[2], row[3]))

# Insert ETL data into the database
def insert_etl_data(filename, etl_data):
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO process_header (file_name, insertion_date)
                VALUES (?, datetime('now'))
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

# Convert CSV content to list of dictionaries for ETL data
def csv_to_dict_list(csv_content):
    reader = csv.DictReader(csv_content.splitlines())
    return [row for row in reader]

# Convert CSV content to list of lists for summary data
def csv_to_list(csv_content):
    reader = csv.reader(csv_content.splitlines())
    return [row for row in reader]

def process_file(filename, content):
    if 'summary_' in filename:
        summary_data = csv_to_list(content)
        insert_summary_data(filename, summary_data)
    elif 'ETL_' in filename:
        etl_data = csv_to_dict_list(content)
        insert_etl_data(filename, etl_data)
