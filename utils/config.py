from dataclasses import dataclass
from os import getenv


@dataclass
class MariaDBConfig:
    MARIA_DB_HOST = getenv("MARIA_DB_HOST", "localhost")
    MARIA_DB_PORT = getenv("MARIA_DB_PORT", 3808)
    MARIA_DB_USER = getenv("MARIA_DB_USER", "test_user")
    MARIA_DB_PASSWORD = getenv("MARIA_DB_PASSWORD", "test_user_123")
    MARIA_DB_DATABASE = getenv("MARIA_DB_DATABASE", "imageservicedb")

