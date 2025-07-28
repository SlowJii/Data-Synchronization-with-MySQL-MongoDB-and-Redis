from database.mysql_connect import MySQLConnect
from config.database_config import get_database_config
import json
from kafka import KafkaProducer

def get_data_trigger(mysql_client, last_timestamp):

    connection, cursor = mysql_client.connection, mysql_client.cursor

    query = """
        SELECT 
            user_id,
            login,
            gravatar_id,
            url,
            avatar_url,
            action_type,
            DATE_FORMAT(log_timestamp,'%Y-%m-%d %H:%i:%s.%f') AS log_timestamp
        FROM 
            user_log_after
    """

    if last_timestamp:
        query += f"WHERE DATE_FORMAT(log_timestamp,'%Y-%m-%d %H:%i:%s.%f') > '{last_timestamp}'"
        cursor.execute(query)
    else:
        cursor.execute(query)

    rows = cursor.fetchall()
    connection.commit()
    schema = ["user_id", "login", "gravatar_id", "url", "avatar_url", "action_type", "log_timestamp"]
    data = [dict(zip(schema,row)) for row in rows]

    if data:
        max_timestamp = max((row["log_timestamp"] for row in data),default = last_timestamp)
    else:
        max_timestamp = last_timestamp

    return data, max_timestamp

def main():
    config = get_database_config()
    last_timestamp = None
    while True:
        with MySQLConnect(
            config['mysql'].host,
            config['mysql'].port,
            config['mysql'].user,
            config['mysql'].password,
            config['mysql'].database
        ) as mysql_client:
            producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            while True:
                data, max_timestamp = get_data_trigger(mysql_client, last_timestamp)
                last_timestamp = max_timestamp
                for record in data:
                    producer.send("slowjii", record)
                    producer.flush()

if __name__ == "__main__":
    main()

