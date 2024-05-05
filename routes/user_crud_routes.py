from services.app_services import __return_success_response, __return_failure_response, __is_id_valid
from flask import request

from utils.logger import logger
from services.db_user_services import DBUserServices

db_client = DBUserServices()


def add_user():
    try:
        logger.info("Hit route /add_user")

        user_name = request.json.get("user_name")
        password = request.json.get("password")

        if user_name is None:
            raise ValueError("User name is INVALID")

        if password is None:
            raise ValueError("Password is INVALID")

        db_client.add_user_db(user_name, password)

        return __return_success_response({
            "status": "user added"
        })

    except Exception as err:
        return __return_failure_response(str(err))


def login_user():
    try:
        logger.info("Hit route /login_user")

        resp_json = request.json
        logger.info(resp_json)

        return __return_success_response({
            "status": "user added"
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_user():
    try:
        logger.info("Hit route /update_user")

        user_id = request.json.get("user_id")
        user_name = request.json.get("user_name")
        password = request.json.get("password")

        __is_id_valid(user_id, id_name="User ID")

        if user_name is None and password is None:
            raise ValueError("User name or password should be supplied")

        logger.info(f" {user_id} ; {user_name} ; {password}")

        res = db_client.update_user_by_id_db(user_id, user_name, password)

        return __return_success_response({
            "updated_user_count": res
        })

    except Exception as err:
        return __return_failure_response(str(err))


def get_user_list():
    try:
        logger.info("Hit route /get_user_list")

        user_list = db_client.get_user_list_db()

        return __return_success_response({
            "user_list": user_list
        })

    except Exception as err:
        return __return_failure_response(str(err))


def get_user():
    try:
        logger.info("Hit route /get_user")

        user_id = request.args.get("user_id")

        __is_id_valid(user_id, id_name="User ID")

        user_data = db_client.get_user_by_id_db(user_id)

        return __return_success_response({
            "user_data": user_data
        })

    except Exception as err:
        return __return_failure_response(str(err))


def delete_user():
    try:
        logger.info("Hit route /delete_user")

        user_id = request.args.get("user_id")
        __is_id_valid(user_id, id_name="User ID")

        res = db_client.delete_user_by_id(user_id)

        return __return_success_response({
            "deleted_users": res
        })

    except Exception as err:
        return __return_failure_response(str(err))
