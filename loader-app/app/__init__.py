from json import loads
from app.enum import EnvironmentVariables as EnvVariables
from kafka import KafkaConsumer
import paramiko
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    try:
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )

        for message in consumer:
            file_data = message.value
            filename = file_data['filename']
            content = file_data['content']
            
            # Reconstruct the file locally
            local_file_path = f'files/{filename}'
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, 'w') as file:
                file.write(content)
            
            logger.info(f'Received and reconstructed file: {local_file_path}')
            
            # Upload the file to the SFTP server
            upload_file_to_sftp(local_file_path, f'/upload/{filename}')

    except Exception as e:
        logger.error('Error in Kafka consumer', exc_info=e)


def upload_file_to_sftp(local_file_path, remote_file_path):
    try:
        sftp_port = int(EnvVariables.SFTP_PORT.get_env())
        sftp_user = EnvVariables.SFTP_USER.get_env()
        sftp_password = EnvVariables.SFTP_PASSWORD.get_env()
        
        transport = paramiko.Transport(('sftp', sftp_port))
        transport.connect(username=sftp_user, password=sftp_password)
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_file_path, remote_file_path)
        
        sftp.close()
        transport.close()
        
        logger.info(f'Successfully uploaded {local_file_path} to {remote_file_path} on SFTP server.')
    except Exception as e:
        logger.error('Failed to upload file to SFTP', exc_info=e)


if __name__ == "__main__":
    main()
