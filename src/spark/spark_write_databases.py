from pyspark.sql import DataFrame, SparkSession
from typing import Dict
from database.mysql_connect import MySQLConnect
from database.mongodb_connect import MongoDBConnect
from config.database_config import get_database_config
from config.spark_config import get_spark_config
from pyspark.sql.functions import *


class SparkWriteDatabases:

    def __init__(self, spark, db_config : Dict):
        self.spark = spark
        self.db_config = db_config

    # ========================= SPARK WRITE SQL =========================
    def spark_write_mysql(self, df_write : DataFrame, table_name : str, jdbc_url : str, config : Dict[str,str], mode : str = "append"):
        print("------------------------------ Spark start WRITE to MySQL --------------------------------")
        try:
            with MySQLConnect(config["host"], config["port"], config["user"], config["password"], config["database"]) as mysql_client:
                connection, cursor = mysql_client.connection, mysql_client.cursor
                database = "github_data"
                connection.database = database
                # Kiem tra Cot Spark da co chua
                check_spark_column_query = f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = '{database}' AND table_name = '{table_name}' AND column_name = 'spark'"
                cursor.execute(check_spark_column_query)
                column_exists = cursor.fetchone()[0]
                if not column_exists:
                    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN spark VARCHAR(255)")
                    connection.commit()
                else:
                    print(f"Table spark already exists")
                mysql_client.close()
        except Exception as e:
            raise Exception(f"-------------Fail to Connect to MySQL: {e}")

        df_write.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .mode(mode) \
            .save()


    #=============== VALIDATE SPARK WRITE TO MYSQL ========#
    def validate_spark_mysql(self,df_write : DataFrame, table_name : str, jdbc_url : str, config : Dict, mode : str = "append"):

        df_read = self.spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", f"(SELECT * FROM {table_name} WHERE spark='spark_write') AS subquery") \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .load()

        def subtract_dataframe(df_write: DataFrame, df_read: DataFrame):
            # Spark write chi co the dua thieu hoac du nen phai dung df_write - df_read
            result = df_write.exceptAll(df_read)
            if not result.isEmpty():
                print(f"--------------- Missing {result.count()} rows in {table_name} -----------------")
                result.write \
                    .format("jdbc") \
                    .option("url", jdbc_url) \
                    .option("driver", "com.mysql.cj.jdbc.Driver") \
                    .option("dbtable", table_name) \
                    .option("user", config["user"]) \
                    .option("password", config["password"]) \
                    .mode(mode) \
                    .save()
                print("--------------- Insert Missing Records to MySQL Successfully--------------------")
        # So sanh DU truoc roi moi DUNG sau
        if df_write.count() == df_read.count():
            print(f"--------------- Validate Nums of Records in MySQL Successfully: {df_write.count()} / {df_read.count()}--------------------")
            subtract_dataframe(df_write, df_read)
        else:
            subtract_dataframe(df_write, df_read)

        # Sau khi Validate thanh cong thi xoa cot danh dau Spark_Write
        with MySQLConnect(config["host"], config["port"], config["user"], config["password"], config["database"]) as mysql_client:
            connection, cursor = mysql_client.connection, mysql_client.cursor
            drop_spark_query = f"ALTER TABLE {table_name} DROP COLUMN spark"
            cursor.execute(drop_spark_query)
            connection.commit()
            print("--------------- DROP SPARK_WRITE TEMP ----------------")
            mysql_client.close()
        print("--------------- Validate Nums of Records in MySQL DONE !!! --------------------")

    #====================================== SPARK WRITE MONGODB ==========================================#
    def spark_write_mongodb(self, df_write : DataFrame,uri : str, database : str, collection : str, mode : str = "append"):
        # mongodb://slowjii:slowjii0211@localhost:27017
        # mongodb://<username>:<password>@<host>:<port>/<database>
        print("---------------------- Spark start WRITE to MongoDB -----------------")
        df_write.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()
        print(f"---------------- Spark Write data to MongoDB: {database}/{collection}-----------------")

    def validate_spark_mongodb(self, df_write : DataFrame, uri : str, database : str, collection : str, mode : str = "append"):
        query = {"spark": "spark_write"}
        df_read = self.spark.read \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .option("pipeline", str([{"$match": query}])) \
            .load()
        df_read = df_read.select(
            col("user_id"),
            col("login"),
            col("gravatar_id"),
            col("url"),
            col("avatar_url"),
            col("spark")
        )
        # column_order = df_write.columns
        # df_read_aligned = df_read.select(column_order)
        # print("-------------------- DF_READ_ALIGNED --------------------")
        # df_read_aligned.printSchema()

        def subtract_dataframe(df_write : DataFrame, df_read: DataFrame):
            result = df_write.exceptAll(df_read)
            if not result.isEmpty():
                result.write \
                    .format("mongo") \
                    .option("uri", uri) \
                    .option("database", database) \
                    .option("collection", collection) \
                    .mode(mode) \
                    .save()
                print("--------------- Insert Missing Records to MongoDB Successfully--------------------")

        # Truyền ĐỦ trước, ĐÚNG sau
        if df_read.count() == df_write.count():
            print(f"--------------- Validate Nums of Records in MongoDB Successfully: {df_write.count()} / {df_read.count()}--------------------")
            subtract_dataframe(df_write, df_read)
        else:
            subtract_dataframe(df_write, df_read)
        print("----------------------- Validate Data in MongoDB Successfully !!! ----------------------")
        config = get_database_config()
        #drop spark column
        try:
            with MongoDBConnect(config['mongodb'].uri, config['mongodb'].database) as mongo_client:
                target_collection = mongo_client.db[collection]
                filter_query = {"spark": "spark_write"}
                update_operation = {"$unset": {"spark": ""}}
                update_result = target_collection.update_many(filter_query, update_operation)
        except Exception as e:
            print(f"An error occurred while dropping 'spark' column from MongoDB: {e}")

    def spark_write_databases(self, df : DataFrame, mode : str = "append"):
        # table_name : str, jdbc_url : str, config : Dict[str,str], mode : str = "append"
        self.spark_write_mysql(
            df,
            self.db_config["mysql"]["table"],
            self.db_config["mysql"]["jdbc_url"],
            self.db_config["mysql"]["config"],
            mode
        )
        print("---------------- Spark Write data to MySQL -----------------")
        self.spark_write_mongodb(
            df,
            self.db_config["mongodb"]["uri"],
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            mode
        )
        print("--------------- Spark Write data to MongoDB ------------------")
    def validate_spark_write_databases(self, df : DataFrame, mode : str = "append"):
        self.validate_spark_mysql(
            df,
            self.db_config["mysql"]["table"],
            self.db_config["mysql"]["jdbc_url"],
            self.db_config["mysql"]["config"],
            mode
        )

        self.validate_spark_mongodb(
            df,
            self.db_config["mongodb"]["uri"],
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            mode
        )
        print("--------------- Validate Data Successfully with Spark in MySQL & MongoDB -----------------")

"""
Có hai cách để Spark ghi vào CSDL
    - Ghi lần lượt vào MySQL, MongoDB rồi đến Redis
    - Ghi đồng loạt vào cả 3 csdl
Tại sao trong hàm Spark write lại không dùng self.spark mà hàm validata lại dùng ?
=> Bởi vì Spark Write bằng DataFrame đã được định nghĩa bởi df= spark_connect.spark bên hàm main.py rồi 
Còn việc validate data là đọc dataframe từ database (kh dùng df dc khởi tạo bên main.py) nên cần self.spark để khởi tạo sparksession (hàm __init__)
"""

