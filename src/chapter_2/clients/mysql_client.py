import pymysql
from chapter_2.interfaces.client_interface import ClientInterface

class MySQLClient(ClientInterface):
    def __init__(
        self,
        host="localhost",
        port=3306,
        user="testuser",
        password="testpass",
        database="testdb",
        charset="utf8mb4"
    ):
        self._config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": charset
        }
        self._conn = None

    def connect(self):
        if self._conn is None:
            self._conn = pymysql.connect(**self._config)
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None