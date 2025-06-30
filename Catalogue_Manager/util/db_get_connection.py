import mysql.connector
from configparser import ConfigParser, NoSectionError
from exceptions.exceptions import DatabaseConnectionError
import os

def get_connection():
    try:
        config = ConfigParser()

        base_path = os.path.dirname(os.path.dirname(__file__)) 
        config_path = os.path.join(base_path, 'config', 'config.ini')

        files_read = config.read(config_path)

        if not files_read:
            raise DatabaseConnectionError(f"Config file not found at: {config_path}")

        if 'database' not in config:
            raise DatabaseConnectionError("Missing [database] section in config file.")

        host = config.get('database', 'host')
        user = config.get('database', 'user')
        password = config.get('database', 'password')
        database = config.get('database', 'database')

        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    except (NoSectionError, KeyError) as e:
        raise DatabaseConnectionError(f"Invalid config structure: {e}") from e
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database connection error: {e}") from e
