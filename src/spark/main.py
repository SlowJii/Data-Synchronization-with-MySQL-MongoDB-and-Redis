from pyspark.sql.functions import *
from config.spark_config import get_spark_config
from config.database_config import get_database_config
from config.spark_config import SparkConnect
from pyspark.sql.types import *
from src.spark.spark_write_databases import SparkWriteDatabases

def main():
    db_configs = get_spark_config()

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
    # Them mot cot spark_write vao de danh dau la ban ghi nay do Spark ghi vao database
    df_write_table = df.withColumn(
        'spark', lit('spark_write')
    ).select(
        col('actor.id').alias('user_id'),
        col('actor.login').alias('login'),
        col('actor.gravatar_id').alias('gravatar_id'),
        col('actor.url').alias('url'),
        col('actor.avatar_url').alias('avatar_url'),
        col('spark').alias('spark')
    )

    # df_write_table = df.select(
    #     col('actor.id').alias('user_id'),
    #     col('actor.login').alias('login'),
    #     col('actor.gravatar_id').alias('gravatar_id'),
    #     col('actor.url').alias('url'),
    #     col('actor.avatar_url').alias('avatar_url')
    # )
    # ============= SPARK WRITE ================
    spark_config = get_spark_config()
    df_write = SparkWriteDatabases(spark_connect, spark_config)
    df_write.spark_write_databases(df_write_table, mode = "append")

    df_read = SparkWriteDatabases(spark_connect, spark_config)
    df_read.validate_spark_mysql(df_write_table,db_configs["mysql"]["table"], db_configs["mysql"]["jdbc_url"], db_configs["mysql"]["config"])

    spark_connect.stop()

if __name__ == "__main__":
    main()

