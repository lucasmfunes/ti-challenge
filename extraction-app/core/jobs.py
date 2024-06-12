import requests
import json
import sys
import os
from datetime import datetime
from core.transform import main as transform_data
from core.kafka import create_kafka_producer, send_files_to_kafka

def fetch_and_save_data():
    print("Fetching data from API...")
    sys.stdout.flush() 

    
    response = requests.get('https://dummyjson.com/users')
    
    if response.status_code == 200:
        data = response.json()  
        today = datetime.today().strftime('%Y%m%d')
        json_file_path = f'files/data_{today}.json'
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data has been written to {json_file_path}")
        
        
        transform_data()
        send_csv_to_kafka()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
    
    sys.stdout.flush()


def send_csv_to_kafka():
    producer = create_kafka_producer('kafka:29092')
    send_files_to_kafka(producer, 'topic_test', 'files')