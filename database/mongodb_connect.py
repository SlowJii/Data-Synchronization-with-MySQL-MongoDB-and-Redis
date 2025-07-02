from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config.database_config import get_database_config
from database.schema_manager import create_mongodb_schema,validate_mongodb_schema

# step 1: def (get mongo config)
# step 2: def (connect)
# step 3: def (disconnect)
# step 4: def (reconnect)
# step 5: def (exit)
"""
Thuc te khi di lam se duoc set database cho phep bao nhieu ket noi vao
Quy trinh:
    Sau khi connect can disconnect de cho nguoi khac vao lam
    Can them ham reconnect de phong truong hop can ket noi lai
    Sau khi xong het viec roi thi can ham exit de thoat khoi tat ca cac ket noi

Tao cac Class nham quan ly va rut gon cac function, dam bao tinh clean code
"""

class MongoDBConnect:
    def __init__(self, mongo_uri, database):
        self.mongo_uri = mongo_uri
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.client.server_info()  # test connection
            #print(self.client.server_info())
            self.db = self.client[self.database]
            print(f"-------------Connected to MongoDB: {self.database} database-------------")
            return self.db
        except Exception as e:
            raise Exception(f"---------- Failed to connect to MongoDB: {self.database} database: {self.database} error: {e}")
    def close(self):
        if self.client:
            self.client.close()
        print(f"-------------MongoDB Connection Closed--------------")

    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def main():
    configMongo = get_database_config()
    with MongoDBConnect(configMongo['mongodb'].uri, configMongo['mongodb'].database) as mongo_client:
        create_mongodb_schema(mongo_client.connect())
        mongo_client.db.Users.insert_one({
            "user_id": 123456789012345,
            "login": "gemini_user",
            "gravatar_url": "https://i.pravatar.cc/150?u=a042581f4e29026704d",
            "url": "https://api.example.com/users/gemini_user",
            "avatar_url": "https://avatars.example.com/u/12345"
        })
        validate_mongodb_schema(mongo_client.db)
        print("-----------Inserted to MongoDB-------------")
if __name__ == '__main__':
    main()

