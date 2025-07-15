from typing import Optional, List, Dict
import os
from pyspark.sql import SparkSession
from config.database_config import get_database_config

class SparkConnect:
    def __init__(
            self,
            app_name : str,
            master_url: str = "local[*]",
            executor_memory: Optional[str] = "4G",
            executor_cores: Optional[int] = 2,
            num_executor: Optional[int] = 3,
            driver_memory: Optional[str] = "2G",
            jar_packages: Optional[List[str]] = None,
            spark_conf: Optional[Dict[str, str]] = None,
            log_level: str = "INFO"):
        self.app_name = app_name
        self.spark = self.create_spark_session(master_url, executor_memory, executor_cores, num_executor, driver_memory, jar_packages, spark_conf, log_level)

    def create_spark_session(
            self,
            master_url: str = "local[*]",
            executor_memory : Optional[str] = "4G" ,
            executor_cores: Optional[int] = 2,
            num_executor: Optional[int] = 3,
            driver_memory: Optional[str] = "2G",
            jar_packages: Optional[List[str]] = None,
            spark_conf: Optional[Dict[str,str]] = None,
            log_level: str = "INFO"
    ) -> SparkSession:
        builder = SparkSession.builder \
            .appName(self.app_name) \
            .master(master_url)
        if executor_memory:
            builder.config("spark.executor.memory", executor_memory)
        if executor_cores:
            builder.config("spark.executor.cores", executor_cores)
        if driver_memory:
            builder.config("spark.driver.memory", driver_memory)
        if num_executor:
            builder.config("spark.executor.instances", num_executor)

        if jar_packages:
            jar_packages_url = ",".join([jar_package for jar_package in jar_packages])
            builder.config("spark.jars.packages", jar_packages_url)

        if spark_conf:
            for key,value in spark_conf.items():
                builder.config(key,value)

        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel(log_level)
        return spark

    def stop(self):
        if self.spark:
            self.spark.stop()
            print("--------------------Stopping Spark Session---------------------")

def get_spark_config() -> Dict:

    db_configs = get_database_config()

    return {
        "mysql" : {
            "table": db_configs["mysql"].table,
            "jdbc_url": "jdbc:mysql://{}:{}/{}".format(db_configs["mysql"].host, db_configs["mysql"].port, db_configs["mysql"].database),
            "config" : {
                "host" : db_configs["mysql"].host,
                "port" : db_configs["mysql"].port,
                "user" : db_configs["mysql"].user,
                "password" : db_configs["mysql"].password,
                "database" : db_configs["mysql"].database
            }
        },
        "mongodb" : {
            "database" : db_configs["mongodb"].database,
            "collection" : db_configs["mongodb"].collection,
            "uri" : db_configs["mongodb"].uri
        },
        "redis" : {

        }
    }


# if jars:
#     jars_path = ",".join([os.path.abspath(jar) for jar in jars])
#     builder.config("spark.jars.packages", jars_path)


"""
{
'mysql': {
    'table': 'users',
    'jdbc_url': 'jdbc:mysql://172.17.0.2:3306/github_data',
    'config': {
        'host': '172.17.0.2',
        'port': 3306,
        'user': 'root',
        'password': '3Vh^ff/#j11aF%K%Z8&1V6vg7.1Gjo+M',
    'database': 'github_data'
    }
},
'mongodb': {},
'redis': {}
}
"""




# from typing import Optional, List, Dict
# import os
# from pyspark.sql import SparkSession
# from config.database_config import get_database_config
#
#
# class SparkConnect:
#     def __init__(
#             self,
#             app_name: str,
#             master_url: str = "local[*]",
#             executor_memory: Optional[str] = "4G",
#             executor_cores: Optional[int] = 2,
#             num_executor: Optional[int] = 3,
#             driver_memory: Optional[str] = "2G",
#             spark_conf: Optional[Dict[str, str]] = None,  # Bỏ 'jar_packages'
#             log_level: str = "INFO"):
#         self.app_name = app_name
#         # Sửa lại để chỉ nhận spark_conf
#         self.spark = self.create_spark_session(master_url, executor_memory, executor_cores, num_executor, driver_memory,
#                                                spark_conf, log_level)
#
#     def create_spark_session(
#             self,
#             master_url: str = "local[*]",
#             executor_memory: Optional[str] = "4G",
#             executor_cores: Optional[int] = 2,
#             num_executor: Optional[int] = 3,
#             driver_memory: Optional[str] = "2G",
#             spark_conf: Optional[Dict[str, str]] = None,  # Bỏ 'jar_packages'
#             log_level: str = "INFO"
#     ) -> SparkSession:
#         builder = SparkSession.builder \
#             .appName(self.app_name) \
#             .master(master_url)
#
#         if executor_memory:
#             builder.config("spark.executor.memory", executor_memory)
#         if executor_cores:
#             builder.config("spark.executor.cores", executor_cores)
#         if driver_memory:
#             builder.config("spark.driver.memory", driver_memory)
#         if num_executor:
#             builder.config("spark.executor.instances", num_executor)
#
#         # Cấu hình chung từ spark_conf
#         if spark_conf:
#             for key, value in spark_conf.items():
#                 builder.config(key, value)
#
#         spark = builder.getOrCreate()
#         spark.sparkContext.setLogLevel(log_level)
#         return spark
#
#     def stop(self):
#         if self.spark:
#             self.spark.stop()
#             print("--------------------Stopping Spark Session---------------------")
#
#
# # Hàm này vẫn giữ nguyên
# def get_spark_config() -> Dict:
#     db_configs = get_database_config()
#     return {
#         "mysql": {
#             "table": db_configs["mysql"].table,
#             "jdbc_url": f"jdbc:mysql://{db_configs['mysql'].host}:{db_configs['mysql'].port}/{db_configs['mysql'].database}",
#             "config": {
#                 "host": db_configs["mysql"].host,
#                 "port": db_configs["mysql"].port,
#                 "user": db_configs["mysql"].user,
#                 "password": db_configs["mysql"].password,
#                 "database": db_configs["mysql"].database
#             }
#         },
#         "mongodb": {
#             "database": db_configs["mongodb"].database,
#             "collection": db_configs["mongodb"].collection,
#             "uri": db_configs["mongodb"].uri
#         },
#         "redis": {}
#     }
#
