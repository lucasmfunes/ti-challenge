import paramiko
import logging
from core.enum import EnvironmentVariables as EnvVariables

logger = logging.getLogger(__name__)

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
