from pyspark.sql import DataFrame, SparkSession
from typing import Dict
from database.mysql_connect import MySQLConnect
from config.spark_config import get_spark_config


class SparkWriteDatabases:

    def __init__(self, spark, db_config : Dict):
        self.spark = spark
        self.db_config = db_config

    def spark_write_mysql(self, df : DataFrame, table_name : str, jdbc_url : str, config : Dict[str,str], mode : str = "append"):
        # try:
        #     mysql_client = MySQLConnect(config)
        #     mysql_client.connect()
        #     mysql_client.close()
        #     """
        #     Trong spark_write_mysql, bạn tạo một MySQLConnect, kết nối rồi đóng ngay lập tức (mysql_client.close()).
        #     Việc này chỉ kiểm tra xem driver node của Spark có thể kết nối tới MySQL tại thời điểm đó hay không.
        #     Nó không đảm bảo rằng các executor node của Spark (nơi thực sự xử lý việc ghi dữ liệu) có thể kết nối.
        #     """
        # except Exception as e:
        #     raise Exception(f"-------------Fail to Connect to MySQL: {e}")

        df.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", table_name) \
            .option("user", config["user"]) \
            .option("password", config["password"]) \
            .mode(mode) \
            .save()
        print(f"--------------- Spark Write data to MySQL: {table_name}-----------------")
    #=============== SPARK WRITE MONGODB ==================#
    def spark_write_mongodb(self, df : DataFrame, database : str, collection : str, uri : str, mode = "append"):
        # mongodb://slowjii:slowjii0211@localhost:27017
        # mongodb://<username>:<password>@<host>:<port>/<database>
        # df.write \
        #     .format("mongodb") \
        #     .option("uri", uri) \
        #     .option("database", database) \
        #     .option("collection", collection) \
        #     .mode(mode) \
        #     .save()
        df.write \
            .format("mongo") \
            .option("uri", uri) \
            .option("database", database) \
            .option("collection", collection) \
            .mode(mode) \
            .save()
        print(f"---------------- Spark Write data to MongoDB: {database}/{collection}-----------------")

    def spark_write_databases(self, df : DataFrame, mode : str = "append"):
        # table_name : str, jdbc_url : str, config : Dict[str,str], mode : str = "append"
        self.spark_write_mysql(
            df,
            self.db_config["mysql"]["table"],
            self.db_config["mysql"]["jdbc_url"],
            self.db_config["mysql"]["config"],
            mode
        )
        self.spark_write_mongodb(
            df,
            self.db_config["mongodb"]["database"],
            self.db_config["mongodb"]["collection"],
            self.db_config["mongodb"]["uri"],
            mode
        )
        print("--------------- Spark Write data to MongoDB ------------------")

"""
Có hai cách để Spark ghi vào CSDL
    - Ghi lần lượt vào MySQL, MongoDB rồi đến Redis
    - Ghi đồng loạt vào cả 3 csdl
"""

