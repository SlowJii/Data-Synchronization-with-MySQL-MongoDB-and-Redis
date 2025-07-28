from kafka import KafkaConsumer

# Thuc te khi di lam thi bootstrap_servers cua Producer va Consumer se khac nhau, nma day la tu hoc nen de localhost
# Khoi tao Consumer voi Topic subcribe va port
consumer = KafkaConsumer(
    "slowjii",
    bootstrap_servers = "localhost:9092"
)
running = True
count_messages = 0
while running:
    msg_pack = consumer.poll(timeout_ms=500)
    for topic, messages in msg_pack.items():
        for msg in messages:
            print(msg.value.decode('utf-8'))
            count_messages += 1
            print(f"----------------{count_messages}--------------------")
