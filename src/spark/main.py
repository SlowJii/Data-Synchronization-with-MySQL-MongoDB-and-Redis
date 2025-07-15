from pyspark.sql.functions import col
from config.spark_config import get_spark_config
from config.database_config import get_database_config
from config.spark_config import SparkConnect
from pyspark.sql.types import *
from src.spark.spark_write_databases import SparkWriteDatabases

def main():
    db_configs = get_database_config()

    # JAR
    jars = [
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
        "mysql:mysql-connector-java:8.0.33"
    ]

    # Cau hinh Spark
    spark_connect = SparkConnect(
        app_name="SlowJii",
        master_url="local[*]",
        executor_memory= "4G",
        executor_cores= 2,
        num_executor= 3,
        driver_memory= "2G",
        jar_packages = jars,
        #spark_conf= spark_conf,
        log_level= "INFO"
    ).spark

    schema = StructType([
        # ============ACTOR==================
        StructField("actor", StructType([
            StructField("id", LongType(), True),
            StructField("login", StringType(), True),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("avatar_url", StringType(), True)
        ]), True),
        # ============REPO====================
        StructField("repo", StructType([
            StructField("id", LongType(), True),
            StructField("name", StringType(), True),
            StructField("url", StringType(), True)
        ]), True)
    ])

    df = spark_connect.read.schema(schema).json("/home/lehoang/PycharmProjects/Data-Synchronization-with-MySQL-MongoDB-and-Redis/data/2015-03-01-17.json")
    #df.show()
    # ========= TAO DATAFRAME DE WRITE =============
    df_write_table = df.select(
        col('actor.id').alias('user_id'),
        col('actor.login').alias('login'),
        col('actor.gravatar_id').alias('gravatar_id'),
        col('actor.url').alias('url'),
        col('actor.avatar_url').alias('avatar_url')
    )

    # ============= SPARK WRITE ================
    spark_config = get_spark_config()
    df_write = SparkWriteDatabases(spark_connect, spark_config)
    df_write.spark_write_databases(df_write_table, mode = "append")

    spark_connect.stop()

if __name__ == "__main__":
    main()


# from pyspark.sql.functions import col
# from config.spark_config import SparkConnect
# from pyspark.sql.types import *
# from src.spark.spark_write_databases import SparkWriteDatabases
# from config.database_config import get_database_config
# from config.spark_config import get_spark_config as get_db_write_config
#
#
# def main():
#
#     db_config = get_db_wri()
#
#
#     # 2. Tạo Spark Session
#     # Bỏ tham số 'jar_packages' và truyền trực tiếp 'spark_conf'
#     spark_session = SparkConnect(
#         app_name="SlowJii",
#         master_url="local[*]",
#         executor_memory="4G",
#         executor_cores=2,
#         num_executor=3,
#         driver_memory="2G",
#         spark_conf=spark_conf,  # <-- Truyền cấu hình vào đây
#         log_level="INFO"
#     ).spark
#
#     # 3. Đọc và xử lý dữ liệu (Giữ nguyên)
#     schema = StructType([
#         StructField("actor", StructType([
#             StructField("id", IntegerType(), True),
#             StructField("login", StringType(), True),
#             StructField("gravatar_id", StringType(), True),
#             StructField("url", StringType(), True),
#             StructField("avatar_url", StringType(), True)
#         ]), True),
#         StructField("repo", StructType([
#             StructField("id", LongType(), True),
#             StructField("name", StringType(), True),
#             StructField("url", StringType(), True)
#         ]), True)
#     ])
#     df = spark_session.read.schema(schema).json(
#         "/home/lehoang/PycharmProjects/Data-Synchronization-with-MySQL-MongoDB-and-Redis/data/2015-03-01-17.json")
#     df_write_table = df.select(
#         col('actor.id').alias('user_id'),
#         col('actor.login').alias('login'),
#         col('actor.gravatar_id').alias('gravatar_id'),
#         col('actor.url').alias('url'),
#         col('actor.avatar_url').alias('avatar_url')
#     )
#
#     # 4. Ghi dữ liệu
#     db_write_config = get_db_write_config()
#     data_writer = SparkWriteDatabases(spark_session, db_write_config)
#
#     # Chỉ test ghi vào MongoDB
#     data_writer.spark_write_mongodb(
#         df_write_table,
#         db_write_config["mongodb"]["database"],
#         db_write_config["mongodb"]["collection"],
#         db_write_config["mongodb"]["uri"],
#         mode="append"
#     )
#
#     spark_session.stop()
#
#
# if __name__ == "__main__":
#     main()