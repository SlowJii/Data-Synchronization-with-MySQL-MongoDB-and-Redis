from pathlib import Path
from mysql.connector import Error

# ----------------------  MongoDB  ---------------------------
def create_mongodb_schema(db):
    #db.drop_collection("Users")
    try:
        db.create_collection("Users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["user_id", "login"],
                "properties": {
                    "user_id": {
                        "bsonType": "long"
                    },
                    "login": {
                        "bsonType": "string"
                    },
                    "gravatar_url": {
                        "bsonType": ["string", "null"]
                    },
                    "url": {
                        "bsonType": ["string", "null"]
                    },
                    "avatar_url": {
                        "bsonType": ["string", "null"]
                    }
                }
            }
        })
        print("--------------Collection Users created------------")
    except Exception as e:
        print(f"-------------Collection Users already exists or other error: {e}-----------")
    db.Users.create_index("user_id", unique=True)

def validate_mongodb_schema(db):
    collections = db.list_collection_names()
    #print(collections)
    if "Users" not in collections:
        raise Exception("Missing 'Users' collection")
    # user = db.Users.find_one({"user_id": 123456789012345})
    # if not user:
    #     raise Exception("user_id not found in MongoDB")
    print("MongoDB schema validated")

# ----------------------  MySQL  --------------------------
SQL_FILE_PATH = Path("../src/schema.sql")
DATABASE_NAME = "github_data"
def create_mysql_schema(connection, cursor):
    # khoi tao database neu chua ton tai
    cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(DATABASE_NAME))
    cursor.execute(f"USE {DATABASE_NAME}")
    try:
        cursor.execute("SHOW TABLES LIKE 'Users'")
        if cursor.fetchone():
            print("-------------MySQL schema already exists----------------")
            return
        else:
            with open(SQL_FILE_PATH, "r", encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
            commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]
            for command in commands:
                cursor.execute(command)

            connection.commit()
            print("--------- Create Schema success -------------")
    except Error as e:
        connection.rollback()
        raise Exception(f"-----------Failed to create MySQL schema: {e}-------------")

def validate_mysql_schema (cursor):
    cursor.execute("SHOW TABLES")
#    tables = cursor.fetchall()
#   [('Repositories',), ('Users',)]
    tables = [row[0] for row in cursor.fetchall()]
    if "Users" not in tables or "Repositories" not in tables:
        raise ValueError("-----------Table does not exist && Wrong Schema ----------------")
    else:
        print("--------------MySQL schema validated----------------")

