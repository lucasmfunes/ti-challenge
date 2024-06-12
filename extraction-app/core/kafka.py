import json
import os
from kafka import KafkaProducer

def create_kafka_producer(bootstrap_servers):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def send_to_kafka(producer, topic, data):
    producer.send(topic, data)
    producer.flush()

def send_files_to_kafka(producer, topic, directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):   
            with open(file_path, 'r') as file:
                content = file.read()
            message = {
                'filename': filename,
                'content': content
            }
            send_to_kafka(producer, topic, message)
            os.remove(file_path)