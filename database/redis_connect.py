import redis
from redis.exceptions import ConnectionError
"""
Mongo không có Username 
Redis có username vì có rất nhiều người sẽ sử dụng nó 
"""

class RedisConnect:
    """
    Một lớp context manager để quản lý kết nối tới Redis một cách an toàn,
    hỗ trợ cả username và password cho Redis 6+ ACLs.
    """
    def __init__(self, host, port, db, user, password):
        """
         Khởi tạo với thông tin cấu hình Redis.

         Args:
             host (str): Địa chỉ host của Redis server.
             port (int): Cổng của Redis server.
             db (int, optional): Số của database Redis để kết nối. Mặc định là 0.
             username (str, optional): Tên người dùng (cho Redis 6+). Mặc định là None.
             password (str, optional): Mật khẩu xác thực. Mặc định là None.
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.config = {
            "host": self.host,
            "port": self.port,
            "db": self.db,
            "username": self.user,
            "password": self.password
        }
        self.client = None

    def connect(self):
        try:
            self.client = redis.Redis(**self.config, decode_responses= True)
            self.client.ping() # Test connection
            print(f"-----------Connected to Redis---------------")
            return self.client
        except ConnectionError as e:
            raise Exception(f"Error connecting to Redis: {e}") from e

    def close(self):
        if self.client:
            self.client.close()
            print(f"-----------Closing Redis connection--------------")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

