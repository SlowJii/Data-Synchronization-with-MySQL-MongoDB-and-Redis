import mysql.connector
from mysql.connector import Error

class MySQLConnect:

    def __init__(self, host, port, user, password, database):
        # self.host = host
        # self.port = port
        # self.user = user
        # self.password = password
        # self.database = database
        self.config = {"host" : host ,"port" : port,"user" : user,"password": password,"database" : database}
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            db_config = self.config.copy()
            db_name = db_config.pop('database', None)
            if not db_name:
                raise ValueError("Database name is missing in the Configuration !")
            # **db_config de truyen vao config kh co database
            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor()

            # Khoi tao Database neu chua ton tai, dung dau ` de ne ki tu dac biet
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            self.cursor.execute(f"USE `{db_name}`")

            print(f"---------------- Connected to MySQL Database -----------")
            return self.connection, self.cursor
        except Error as e:
            raise Exception(f"--------------Failed to connect to MySQL Database: {e}----------") from e

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(f"---------------- Connection Closed ----------------")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()





