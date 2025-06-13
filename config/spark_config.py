from typing import Optional, List, Dict
import os
from pyspark.sql import SparkSession
from config.mysql_config import get_database_config

# Cac worker deu duoc kiem soat va chi phoi boi master_url
def create_spark_session(
    app_name : str,
    master_url : str = "local[*]",           # di lam kh dc chay tren local, chi dc chay tren server, log vao bang dia chi ip, port cua spark master
    executor_memory : Optional[str] = "4g",  # RAM
    executor_cores : Optional[int] = 2,    # CPU
    driver_memory : Optional[str] = "2g",    # Drive memory
    num_executors : Optional[int] = 3,       # Set so luong executor
    jars : Optional[List[str]] = None,       # Config goi jar duoi dang LIST nham luu tru nhieu goi jar khac nhau
    spark_conf : Optional[Dict[str,str]] = None,
    log_level : str = "INFO"
) -> SparkSession:

    builder = SparkSession.builder \
        .appName(app_name) \
        .master(master_url)
    if executor_memory:
        builder.config("spark.executor.memory", executor_memory)
    if executor_cores:
        builder.config("spark.executor.cores", executor_cores)
    if driver_memory:
        builder.config("spark.driver.memory", driver_memory)
    if num_executors:
        builder.config("spark.executor.instances", num_executors)
    if jars:
        jars_path = ",".join([os.path.abspath(jar) for jar in jars])
        builder.config("spark.jars", jars_path)

    # {"spark.sql.shuffle.partitions" : "10"} == spark_conf
    if spark_conf:
        for key,value in spark_conf.items():
            builder.config(key,value)

    spark = builder.getOrCreate()
    # Start he thong truoc khi set Log Level
    spark.sparkContext.setLogLevel(log_level)

    return spark

"""
spark = create_spark_session(
    app_name = "SlowJii",
    master_url = "local[*]",
    executor_memory = "4g",
    executor_cores = 2,
    driver_memory = "2g",
    num_executors = 3,
    jars = None,
    spark_conf = {"spark.sql.shuffle.partitions" : "10"},
    log_level = "INFO"
)
"""

def connect_to_mysql(spark : SparkSession, config : Dict[str,str], table_name : str):
    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://172.17.0.2:3306/github_data") \
        .option("dbtable", table_name) \
        .option("user", config["user"]) \
        .option("password", config["password"]) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .load()
    return df

jarPath = "../lib/mysql-connector-j-9.2.0.jar"

spark = create_spark_session(
    app_name = "SlowJii",
    master_url = "local[*]",
    executor_memory = "4g",
    jars = [jarPath],
    log_level = "INFO"
)
db_config = get_database_config()
mysql_table = "Repositories"

df = connect_to_mysql(spark, db_config, mysql_table)
df.printSchema()


