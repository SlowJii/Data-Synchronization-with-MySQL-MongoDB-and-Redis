import os
from typing import Dict
# import loadenv
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    def validate(self) -> None:
        for key, value in self.__dict__.items():
            if value is None or value =="":
                raise ValueError(f"--------Missing config for {key}-----------")

"""
Lợi dụng tính Kế thừa (Inheritance), cho các lớp Config của các csdl kế thừa lớp 
DatabaseConfig để được chia sẻ chức năng chung validate, dễ dàng mở rộng hơn, ví dụ cần thêm 
hàm kiểu logging thì chỉ cần thêm vào lớp DatabaseConfig 
"""
@dataclass
class MySQLConfig(DatabaseConfig):
    host : str
    port : int
    user : str
    password : str
    database : str

@dataclass
class MongoDBConfig(DatabaseConfig):
    uri : str
    database : str

@dataclass
class RedisConfig(DatabaseConfig):
    host : str
    user : str
    password : str
    port : int
    database : int

def get_database_config() -> Dict[str, DatabaseConfig]:
    # Doc config tu file .env va tra ve Dict chua cac doi tuong DatabaseConfig
    load_dotenv()

    config = {
        "mongodb" : MongoDBConfig(
            uri = os.getenv("MONGO_URI"),
            database=os.getenv("MONGO_DB")
        ),
        "mysql" : MySQLConfig(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        ),
        "redis" : RedisConfig(
            host=os.getenv("REDIS_HOST"),
            user=os.getenv("REDIS_USER"),
            password=os.getenv("REDIS_PASSWORD"),
            port=int(os.getenv("REDIS_PORT")),
            database=os.getenv("REDIS_DB")
        )
    }

    for db, settings in config.items():
        settings.validate()

    return config

#dbConfig = get_database_config()
#print(dbConfig)
#print(dbConfig['mongodb'].uri)
#print(dbConfig['mongodb'].database)
"""
Vi ham get_database_config tra ve ket qua la mot Dict co 
key = str
value = class
Vay nen ket qua tra ve cua value se la mot class
VD: 
MongoDBConfig(uri='mongodb://slowjii:slowjii0211@localhost:27017', database='myapp_db')
=> Muon truy cap vao uri hay database thi phai .uri va .database
"""
