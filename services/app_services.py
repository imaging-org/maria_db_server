from flask import Response
import json

from utils.logger import logger
from uuid import UUID


def __return_success_response(body: dict = None):
    return Response(status=200,
                    response=json.dumps(body))


def __return_failure_response(error: str = "", status_code=500):
    logger.error(f"Error : {error}")
    return Response(status=status_code,
                    response=json.dumps({
                        "error": error
                    }))


def __is_id_valid(id_, id_name):
    error_message = f"{id_name} is INVALID"
    if id_ is None:
        raise ValueError(error_message)
    else:
        try:
            UUID(id_, version=4)
        except ValueError:
            raise ValueError(error_message)
