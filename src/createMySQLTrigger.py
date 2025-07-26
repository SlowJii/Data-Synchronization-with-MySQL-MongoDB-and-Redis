from config.database_config import get_database_config
from database.schema_manager import create_mysql_trigger
from database.mysql_connect import MySQLConnect
config = get_database_config()
with MySQLConnect(
        config['mysql'].host,
        config['mysql'].port,
        config['mysql'].user,
        config['mysql'].password,
        config['mysql'].database) as mysql_client:
    connection, cursor = mysql_client.connection, mysql_client.cursor
    create_mysql_trigger(connection, cursor)
