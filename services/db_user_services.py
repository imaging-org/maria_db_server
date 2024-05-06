from services.maria_db_services import MariaDBService

from datetime import datetime
import uuid

from utils.constants import TableConstants


class DBUserServices:
    def __init__(self):
        self._db_client = MariaDBService.get_instance()
        self._connection = self._db_client.get_connection()
        self._cursor = self._db_client.get_cursor()

    def add_user_db(self, user_name, password):
        id_ = str(uuid.uuid4())
        created_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_query_string = (f"INSERT INTO {TableConstants.USERS} (id, user_name, password, created_date_time) VALUES ("
                            f"%s, %s, %s, %s)")
        values = (id_, user_name, password, created_date_time)
        self._cursor.execute(sql_query_string, values)
        self._connection.commit()

        return self._cursor.rowcount

    def get_user_list_db(self):
        sql_query_string = f"SELECT * FROM {TableConstants.USERS}"
        self._cursor.execute(sql_query_string)
        res = self._cursor.fetchall()
        for user in res:
            user["created_date_time"] = user["created_date_time"].strftime('%Y-%m-%d %H:%M:%S')
            del user["password"]
        return res

    def get_user_by_id_db(self, user_id):
        sql_query_string = f"SELECT * FROM {TableConstants.USERS} WHERE id = ?"
        self._cursor.execute(sql_query_string, (user_id,))
        res = self._cursor.fetchone()

        if res is None:
            return res

        res["created_date_time"] = res["created_date_time"].strftime('%Y-%m-%d %H:%M:%S')
        del res["password"]
        return res

    def get_user_by_name_db(self, user_name):
        sql_query_string = f"SELECT * FROM {TableConstants.USERS} WHERE user_name = ?"
        self._cursor.execute(sql_query_string, (user_name,))
        res = self._cursor.fetchone()

        if res is None:
            return res

        res["created_date_time"] = res["created_date_time"].strftime('%Y-%m-%d %H:%M:%S')
        return res

    def delete_user_by_id(self, user_id):
        sql_query_string = f"DELETE FROM {TableConstants.USERS} WHERE id = ?"
        self._cursor.execute(sql_query_string, (user_id,))
        self._connection.commit()
        return self._cursor.rowcount

    def update_user_by_id_db(self, user_id, user_name=None, password=None):
        query_string_table_name = f"UPDATE {TableConstants.USERS}"
        query_string_where_clause = f" WHERE id = %s"
        query_string_set_clause = ""
        values = None

        if user_name is not None:
            query_string_set_clause = " SET user_name = %s"
            values = (user_name, user_id)
        if password is not None:
            if query_string_set_clause != "":
                query_string_set_clause = " SET user_name = %s, password = %s"
                values = (user_name, password, user_id)
            else:
                query_string_set_clause = " SET password = %s"
                values = (password, user_id)

        sql_query_string = query_string_table_name + query_string_set_clause + query_string_where_clause
        self._cursor.execute(sql_query_string, values)
        self._connection.commit()

        return self._cursor.rowcount

