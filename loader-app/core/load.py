from json import loads
from kafka import KafkaConsumer
import logging
import os
from core.sftp_client import upload_file_to_sftp
from core.enum import EnvironmentVariables as EnvVariables
from core.database_manager import create_tables, process_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def consume_messages(): 
    try:
        create_tables() 
        consumer = KafkaConsumer(
            "topic_test",
            bootstrap_servers="kafka:29092",
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )

        for message in consumer:
            file_data = message.value
            filename = file_data['filename']
            content = file_data['content']
            
            local_file_path = f'files/{filename}'
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, 'w') as file:
                file.write(content)
            
            logger.info(f'Received and reconstructed file: {local_file_path}')
            
            process_file(filename, content)
            
            upload_file_to_sftp(local_file_path, f'/upload/{filename}')

    except Exception as e:
        logger.error('Error in Kafka consumer', exc_info=e)

if __name__ == "__main__":
    consume_messages()
