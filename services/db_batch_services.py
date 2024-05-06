from utils.logger import logger

from services.maria_db_services import MariaDBService

from time import time
from datetime import datetime
import uuid

from utils.constants import TableConstants, Status


class DBBatchServices:
    def __init__(self):
        self._db_client = MariaDBService.get_instance()
        self._connection = self._db_client.get_connection()
        self._cursor = self._db_client.get_cursor()

    def create_batch_db(self, user_id, event_type, status=Status.PENDING):
        id_ = str(uuid.uuid4())
        created_timestamp = int(round(time() * 1000))
        sql_query_string = (f"INSERT INTO {TableConstants.BATCH} (id, user_id, event_type, created_timestamp, status) "
                            f"VALUES (%s, %s, %s, %s, %s)")
        values = (id_, user_id, event_type, created_timestamp, status)
        self._cursor.execute(sql_query_string, values)
        self._connection.commit()

        return id_

    def get_batch_list_db(self, user_data_flag=False):
        sql_query_string = f"SELECT * FROM {TableConstants.BATCH}"
        if user_data_flag:
            sql_query_string = f"SELECT * FROM {TableConstants.BATCH} CROSS JOIN {TableConstants.USERS} "

        self._cursor.execute(sql_query_string)
        res = self._cursor.fetchall()

        if user_data_flag:
            for data in res:
                data["created_date_time"] = data["created_date_time"].strftime('%Y-%m-%d %H:%M:%S')
                del data["password"]

        return res

    def get_batch_by_id_db(self, batch_id, user_data_flag=False):
        sql_query_string = f"SELECT * FROM {TableConstants.BATCH} WHERE id = ?"
        if user_data_flag:
            sql_query_string = (f"SELECT * FROM {TableConstants.BATCH} CROSS JOIN {TableConstants.USERS} "
                                f"WHERE {TableConstants.BATCH}.id = ? ;")

        logger.info(sql_query_string)
        self._cursor.execute(sql_query_string, (batch_id,))
        res = self._cursor.fetchone()

        if res is None:
            return res

        if user_data_flag:
            res["created_date_time"] = res["created_date_time"].strftime('%Y-%m-%d %H:%M:%S')
            del res["password"]

        return res

    def create_save_image_db(self, user_id, batch_id, minio_file_name, image_url):
        id_ = str(uuid.uuid4())
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_query_string = (f"INSERT INTO {TableConstants.SAVED_IMAGES} (id, user_id, batch_id, created_date_time, "
                            f"minio_file_name, image_url, deleted_flag)"
                            f"VALUES (%s, %s, %s, %s, %s)")
        values = (id_, user_id, batch_id, created_date_time, minio_file_name, image_url, False)
        self._cursor.execute(sql_query_string, values)
        self._connection.commit()

    def delete_save_image_db(self, save_image_id, deleted_batch_id):
        sql_query_string = (f"UPDATE {TableConstants.SAVED_IMAGES} SET deleted_batch_id = {deleted_batch_id}, "
                            f"deleted_flag = {True} WHERE id = {save_image_id}")
        self._cursor.execute(sql_query_string)
        self._connection.commit()

    def update_save_image_db(self, batch_id, status, user_id=None, minio_file_name=None, image_url=None):
        completion_timestamp = int(round(time() * 1000))
        query_string_batch = (f"UPDATE {TableConstants.BATCH} SET status = {status}, "
                              f"completion_timestamp = {completion_timestamp} WHERE id = {batch_id}")
        self._cursor.execute(query_string_batch)
        self._connection.commit()

        if status == Status.SUCCESS:
            self.create_save_image_db(user_id, batch_id, minio_file_name, image_url)

    def update_delete_image_db(self, save_image_id, deleted_batch_id, status):
        completion_timestamp = int(round(time() * 1000))
        query_string_batch = (f"UPDATE {TableConstants.BATCH} SET status = {status}, "
                              f"completion_timestamp = {completion_timestamp} WHERE id = {deleted_batch_id}")
        self._cursor.execute(query_string_batch)
        self._connection.commit()

        if status == Status.SUCCESS:
            self.delete_save_image_db(save_image_id, deleted_batch_id)

    def reset_db(self, batch_id, status):
        if status == Status.SUCCESS:
            query_string_batch = f"DELETE FROM {TableConstants.BATCH};"
            query_string_batch = query_string_batch + f" DELETE FROM {TableConstants.SAVED_IMAGES};"
            query_string_batch = query_string_batch + f" DELETE FROM {TableConstants.SIMILAR_IMAGES};"
            query_string_batch = query_string_batch + f" DELETE FROM {TableConstants.SIMILAR_IMAGE_SAVED_IMAGE};"

            self._cursor.execute(query_string_batch)
            self._connection.commit()
        else:
            completion_timestamp = int(round(time() * 1000))
            query_string_batch = (f"UPDATE {TableConstants.BATCH} SET status = {Status.FAILED}, "
                                  f"completion_timestamp = {completion_timestamp} WHERE id = {batch_id}")
            self._cursor.execute(query_string_batch)
            self._connection.commit()
