from database.mongodb_connect import MongoDBConnect
from config.database_config import get_database_config
from database.schema_manager import create_mongodb_schema,validate_mongodb_schema

def main():
    configMongoDB = get_database_config()
    with MongoDBConnect(configMongoDB['mongodb'].uri, configMongoDB['mongodb'].database) as mongo_client:
        create_mongodb_schema(mongo_client.connect())
        mongo_client.db.Users.insert_one({
            "user_id": 123456789012345,
            "login": "gemini_user",
            "gravatar_url": "https://i.pravatar.cc/150?u=a042581f4e29026704d",
            "url": "https://api.example.com/users/gemini_user",
            "avatar_url": "https://avatars.example.com/u/12345"
        })
        validate_mongodb_schema(mongo_client.db)
        print("----------Inserted to MongoDB-------------")


if __name__ == '__main__':
    main()

