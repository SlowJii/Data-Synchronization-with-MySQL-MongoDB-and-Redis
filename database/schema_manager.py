


def create_mongodb_schema(db):
    db.drop_collection("Users")
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
    db.User.create_index("user_id", unique=True)

def validate_mongodb_schema(db):
    collections = db.list_collection_names()
    #print(collections)
    if "Users" not in collections:
        raise Exception("Missing 'Users' collection")
    user = db.Users.find_one({"user_id": 123456789012345})
    if not user:
        raise Exception("user_id not found in MongoDB")
    print("MongoDB schema validated")