from pyspark.sql import DataFrame, SparkSession
from typing import Dict
from database.mysql_connect import MySQLConnect
from config.spark_config import get_spark_config


class SparkWriteDatabases:

    def __init__(self, spark, db_config : Dict):
        self.spark = spark
        self.db_config = db_config

    # ========================= SPARK WRITE SQL =========================
    def spark_write_mysql(self, df_write : DataFrame, table_name : str, jdbc_url : str, config : Dict[str,str], mode : str = "append"):
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
        print(f"--------------- Spark Write data to MySQL: {table_name}-----------------")

    #=============== VALIDATE SPARK WRITE TO MYSQL ========#
    def validate_spark_mysql(self,df_write : DataFrame, table_name : str, jdbc_url : str, config : Dict):

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
                    .mode("append") \
                    .save()
                print("--------------- Insert Missing Records Successfully--------------------")
        # So sanh DU truoc roi moi DUNG sau
        if df_write.count() == df_read.count():
            print(f"--------------- Validate Nums of Records Successfully: {df_write.count()} / {df_read.count()}--------------------")
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

    #=============== SPARK WRITE MONGODB ==================#
    def spark_write_mongodb(self, df : DataFrame, database : str, collection : str, uri : str, mode = "append"):
        # mongodb://slowjii:slowjii0211@localhost:27017
        # mongodb://<username>:<password>@<host>:<port>/<database>
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
        print("---------------- Spark Write data to MySQL -----------------")
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

