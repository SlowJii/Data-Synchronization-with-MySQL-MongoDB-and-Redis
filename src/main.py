from database.mongodb_connect import MongoDBConnect
from config.database_config import get_database_config
from database.redis_connect import RedisConnect
from database.schema_manager import create_mongodb_schema,validate_mongodb_schema,create_mysql_schema,validate_mysql_schema, create_redis_schema,validate_redis_schema
from database.mysql_connect import MySQLConnect
def main():

    # get config
    config = get_database_config()

# -------------------- MongoDB ---------------------
    with MongoDBConnect(config['mongodb'].uri, config['mongodb'].database) as mongo_client:
        create_mongodb_schema(mongo_client.connect())
        mongo_client.db.Users.insert_one({
            "user_id": 1234567890123451270,
            "login": "gemini_user_2",
            "gravatar_url": "https://i.pravatar.cc/150?u=a042581f4e29026704d1",
            "url": "https://api.example.com/users/gemini_user1",
            "avatar_url": "https://avatars.example.com/u/123451"
        })
        validate_mongodb_schema(mongo_client.db)
        print("----------Inserted to MongoDB-------------")

# -------------------- MySQL -------------------------
    with MySQLConnect(
            config['mysql'].host,
            config['mysql'].port,
            config['mysql'].user,
            config['mysql'].password,
            config['mysql'].database) as mysql_client:
        connection,cursor = mysql_client.connection, mysql_client.cursor
        create_mysql_schema(connection, cursor)
        # Su dung placeholder (%s) de chong SQL Injection
        sql_query = "INSERT INTO Users(user_id, login, gravatar_id, url, avatar_url) VALUES (%s, %s, %s, %s, %s)"
        new_sample = (
            123456781,
            "another_user_2",
            "some_gravatar_id_string_1",
            "https://api.github.com/users/another_user_1",
            "https://avatars.githubusercontent.com/u/98765432123"
        )
        cursor.execute(sql_query, new_sample)
        connection.commit()
        print("-----------------Inserted new sample to MySQL---------------")
        validate_mysql_schema(cursor)

# ------------------ Redis ---------------------------
    with RedisConnect(
            config["redis"].host,
            config["redis"].port,
            config["redis"].database,
            config["redis"].user,
            config["redis"].password) as redis_client:
        create_redis_schema(redis_client.connect())
        validate_redis_schema(redis_client.connect())



if __name__ == '__main__':
    main()

