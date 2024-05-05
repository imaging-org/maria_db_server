import mariadb
from utils.config import MariaDBConfig
from utils.logger import logger


class MariaDBService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        logger.info("Establishing MariaDB connection")
        self._connection = mariadb.connect(
            user=MariaDBConfig.MARIA_DB_USER,
            password=MariaDBConfig.MARIA_DB_PASSWORD,
            host=MariaDBConfig.MARIA_DB_HOST,
            port=MariaDBConfig.MARIA_DB_PORT,
            database=MariaDBConfig.MARIA_DB_DATABASE
        )

        self._cursor = self._connection.cursor(dictionary=True)

        logger.info("MariaDB connection Established")

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor
