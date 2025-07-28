from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("SlowJii") \
    .master("local[*]") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:10.5.0") \
    .config("spark.driver.memory", "2G") \
    .getOrCreate()

# Offset la cai danh dau Consumer dang doc den dau cua Topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("startingOffsets", "latest") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "slowjii") \
  .load()

schemaKafka = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("login", StringType(), True),
    StructField("gravatar_url", StringType(), True),
    StructField("url", StringType(), True),
    StructField("avatar_url", StringType(), True),
    StructField("action_type", StringType(), True),
    StructField("log_timestamp", StringType(), True)
])

data_decode = df.selectExpr("CAST(value AS STRING)")

data_decode.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start() \
    .awaitTermination()

# data_decode = df.select(col("value").cast("string"))
#
# data = data_decode.select(from_json(col("value"), schemaKafka).alias("data")) \
#     .select("data.*")

# data.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .option("truncate", False) \
#     .start() \
#     .awaitTermination()
