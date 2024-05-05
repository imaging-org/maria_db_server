from services.maria_db_services import MariaDBService
from utils.constants import TableConstants

from utils.logger import logger


class DBBatchServices:
    def __init__(self):
        self._db_client = MariaDBService.get_instance()
        self._connection = self._db_client.get_connection()
        self._cursor = self._db_client.get_cursor()

    def update_table(self, sql_string):
        self._cursor.execute(sql_string)
        self._connection.commit()

    def fetch_image_list_by_user_id_db(self, user_id):
        sql_query_string = (f"SELECT * FROM {TableConstants.SAVED_IMAGES} CROSS JOIN {TableConstants.USERS} "
                            f"CROSS JOIN {TableConstants.BATCH} WHERE user_id = {user_id}")
        self._cursor.execute(sql_query_string)
        res = self._cursor.fetchall()
        logger.info(res)
        return res
