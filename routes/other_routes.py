from services.app_services import __return_success_response, __return_failure_response, __is_id_valid
from services.db_other_services import DBBatchServices

from utils.logger import logger
from flask import request

db_client = DBBatchServices()


def fetch_image_list():
    try:
        logger.info("Hit route /fetch_image_list")

        user_id = request.args.get("user_id")
        __is_id_valid(user_id, id_name="User ID")

        res = db_client.update_table(user_id)

        return __return_success_response({
            "image_list": res
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_table():
    try:
        logger.info("Hit route /update_table")

        sql_string = request.json.get("sql_string")

        db_client.update_table(sql_string)

        return __return_success_response({
            "status": "updated table"
        })

    except Exception as err:
        return __return_failure_response(str(err))
