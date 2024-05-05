from dataclasses import dataclass


@dataclass
class Status:
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class Endpoints:
    UPDATE_SAVE_IMAGE_BATCH_STATUS = "/update_save_image_batch_status"
    UPDATE_DELETE_IMAGE_BATCH_STATUS = "/update_delete_image_batch_status"
    UPDATE_RESET_DB_BATCH_STATUS = "/update_reset_db_batch_status"
    UPDATE_SIMILAR_IMAGE_BATCH_STATUS = "/update_similar_image_batch_status"
    CREATE_BATCH = "/create_batch"
    GET_BATCH_LIST = "/get_batch_list"
    GET_BATCH_STATUS = "/get_batch_status"

    ADD_USER = "/add_user"
    LOGIN_USER = "/login_user"
    UPDATE_USER = "/update_user"
    GET_USER_LIST = "/get_user_list"
    GET_USER = "/get_user"
    DELETE_USER = "/delete_user"

    FETCH_IMAGE_LIST = "/fetch_image_list"
    UPDATE_TABLE = "/update_table"


@dataclass
class HTTPMethods:
    GET_METHOD = ["GET"]
    POST_METHOD = ["POST"]
    DELETE_METHOD = ["DELETE"]


@dataclass
class TableConstants:
    USERS = "users"
    BATCH = "Batch"
    SAVED_IMAGES = "saved_images"
    SIMILAR_IMAGES = "similar_images"
    SIMILAR_IMAGE_SAVED_IMAGE = "similar_image_saved_image"


@dataclass
class EventType:
    EVENT_LIST = [
        "Save",
        "Delete",
        "Similar",
        "Reset"
    ]
