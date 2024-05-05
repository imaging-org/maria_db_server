from services.app_services import __return_success_response, __return_failure_response, __is_id_valid
from flask import request

from services.db_batch_services import DBBatchServices

from utils.constants import EventType
from utils.logger import logger

db_client = DBBatchServices()


def create_batch():
    try:
        logger.info("Hit route /create_batch")

        user_id = request.json.get("user_id")
        event_type = request.json.get("event_type")

        __is_id_valid(user_id, id_name="User ID")

        if event_type is None and event_type not in EventType.EVENT_LIST:
            raise ValueError("Event Type is INVALID")

        res = db_client.create_batch_db(user_id, event_type)

        return __return_success_response({
            "batch_id": res
        })

    except Exception as err:
        return __return_failure_response(str(err))


def get_batch_list():
    try:
        logger.info("Hit route /get_batch_list")

        user_data_flag = request.args.get("user_data_flag")
        if user_data_flag:
            if user_data_flag.lower() == "true":
                user_data_flag = True
            else:
                user_data_flag = False

        batch_list = db_client.get_batch_list_db(user_data_flag=user_data_flag)

        return __return_success_response({
            "batch_list": batch_list
        })

    except Exception as err:
        return __return_failure_response(str(err))


def get_batch_status():
    try:
        logger.info("Hit route /get_batch_status")

        batch_id = request.args.get("batch_id")
        user_data_flag = request.args.get("user_data_flag")

        if user_data_flag:
            if user_data_flag.lower() == "true":
                user_data_flag = True
            else:
                user_data_flag = False

        __is_id_valid(batch_id, id_name="Batch ID")

        batch_data = db_client.get_batch_by_id_db(batch_id, user_data_flag=user_data_flag)

        return __return_success_response({
            "batch_data": batch_data
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_save_image_batch_status():
    try:
        logger.info("Hit route /update_save_image_batch_status")

        user_id = request.json.get("user_id")
        batch_id = request.json.get("batch_id")
        image_url = request.json.get("image_url")
        status = request.json.get("status")
        minio_file_name = request.json.get("file_path")

        __is_id_valid(user_id, id_name="User ID")
        __is_id_valid(batch_id, id_name="Batch ID")

        db_client.update_save_image_db(batch_id, status, user_id, minio_file_name, image_url)

        return __return_success_response({
            "status": "Updated"
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_delete_image_batch_status():
    try:
        logger.info("Hit route /update_delete_image_batch_status")

        save_image_id = request.json.get("image_id")
        deleted_batch_id = request.json.get("batch_id")
        status = request.json.get("status")

        __is_id_valid(deleted_batch_id, id_name="Batch ID")

        db_client.update_delete_image_db(save_image_id, deleted_batch_id, status)

        return __return_success_response({
            "status": "Updated"
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_reset_db_batch_status():
    try:
        logger.info("Hit route /update_delete_image_batch_status")

        status = request.json.get("status")
        batch_id = request.json.get("batch_id")

        __is_id_valid(batch_id, id_name="Batch ID")

        db_client.reset_db(batch_id, status)

        return __return_success_response({
            "status": "Reset successful"
        })

    except Exception as err:
        return __return_failure_response(str(err))


def update_similar_image_batch_status():
    try:
        pass

        return __return_success_response({})

    except Exception as err:
        return __return_failure_response(str(err))
