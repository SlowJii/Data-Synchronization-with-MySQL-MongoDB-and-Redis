import mysql.connector
from config.mysql_config import get_database_config
from pathlib import Path
from mysql.connector import Error

DATABASE_NAME = "github_data"
SQL_FILE_PATH = Path("/home/lehoang/PycharmProjects/Data-Synchronization-with-MySQL-MongoDB-and-Redis/src/schema.sql")

def connect_to_mysql(config):
    try:
        connection = mysql.connector.connect(**config)
        print("Successfully connected to MySQL")
        return connection
    except Error as e:
        raise Exception(f"Cannot connect to MySQL: {e}") from e

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"--------------Database {db_name} created successfully--------------")

def execute_sql(cursor, file_path):
    with open(file_path, "r") as file:
        sql_script = file.read()
    commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

    for cmd in commands:
        try:
            cursor.execute(cmd)
            print(f"Executed command: {cmd}")
        except Error as e:
            print(f"Cannot execute command: {cmd}: {e}")

def main():
    try:
        configMySQL = get_database_config()
        connection = connect_to_mysql(configMySQL)
        cursor = connection.cursor()

        # create database
        create_database(cursor, DATABASE_NAME)
        connection.database = DATABASE_NAME

        # execute command
        execute_sql(cursor, SQL_FILE_PATH)
        connection.commit()
        print(f"------------------Command executed successfully--------------")
    except Error as e:
        print(f"-----------------ERROR: {e}----------------------------")
        if connection and connection.is_connected():
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Disconnecting from MySQL")

if __name__ == "__main__":
    main()