import os
from enum import Enum


class EnvironmentVariables(str, Enum):
    KAFKA_TOPIC_NAME = 'KAFKA_TOPIC_NAME'
    KAFKA_SERVER = 'KAFKA_SERVER'
    KAFKA_PORT = 'KAFKA_PORT'
    SFTP_USER = 'SFTP_USER'
    SFTP_PASSWORD = 'SFTP_PASSWORD'
    SFTP_PORT= 'SFTP_PORT'

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
