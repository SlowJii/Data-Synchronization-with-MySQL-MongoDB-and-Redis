from dotenv import load_dotenv
import os
from urllib.parse import urlparse

def get_database_config():
    load_dotenv()
    jdbc_url = os.getenv('DB_URL')
    parser_url = urlparse(jdbc_url.replace('jdbc:', '',1))

    # user, password, host, port, database
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = parser_url.hostname
    port = parser_url.port
    database = parser_url.path.replace('/', '')

    return {
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "database": database
    }