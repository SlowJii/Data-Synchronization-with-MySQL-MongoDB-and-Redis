from config.mysql_config import get_database_config
import mysql.connector
from pathlib import Path
from mysql.connector import Error

DATABASE_NAME = "github_data"
URL_PATH = Path("/home/lehoang/PycharmProjects/Data-Synchronization-with-MySQL-MongoDB-and-Redis/src/schema.sql")

def connect_to_mysql(config):
    try:
        connection = mysql.connector.connect(**config)
        print("Successfully connected to MySQL")
        return connection
    except Error as e:
        raise Exception(f"Error connecting to MySQL: {e}")

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database {db_name} created")

def execute_schemaSQL(cursor, file_path):
    with open(file_path, "r") as file:
        sql_scripts = file.read()
    commands = [cmd.strip() for cmd in sql_scripts.split(";") if cmd.strip()]
    for command in commands:
        try:
            cursor.execute(command)
            print(f"Executed command: {command}")
        except Error as e:
            print(f"Error executing command: {command}: {e}")

def main():
    try:
        configMySQL = get_database_config()

        #connect to database
        connection = connect_to_mysql(configMySQL)
        cursor = connection.cursor()

        #create database
        create_database(cursor, DATABASE_NAME)
        connection.database = DATABASE_NAME

        #execute sql
        execute_schemaSQL(cursor, URL_PATH)
        connection.commit()
        print(f"Command executed successfully")
    except Error as e:
        print(f"--------------Error: {e}----------")
        if connection and connection.is_connected():
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()