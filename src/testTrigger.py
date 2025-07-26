from database.mysql_connect import MySQLConnect
from config.database_config import get_database_config

config = get_database_config()
TEST_TRIGGER_PATH = "/home/lehoang/PycharmProjects/Data-Synchronization-with-MySQL-MongoDB-and-Redis/sql/test-trigger.sql"

with MySQLConnect(
    config['mysql'].host,
    config['mysql'].port,
    config['mysql'].user,
    config['mysql'].password,
    config['mysql'].database) as mysql_client:
    connection, cursor = mysql_client.connection, mysql_client.cursor
    with open(TEST_TRIGGER_PATH, "r", encoding='utf-8') as sql_file:
        sql_scripts = sql_file.read()
    commands = [cmd.strip() for cmd in sql_scripts.split(";") if cmd.strip()]
    for command in commands:
        cursor.execute(command)
    connection.commit()



