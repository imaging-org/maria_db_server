from flask import Flask
from flask_cors import CORS

from routes.user_crud_routes import get_user_list, get_user, add_user, delete_user, update_user, get_user_with_pwd
from routes.batch_routes import (get_batch_status, get_batch_list, create_batch, update_similar_image_batch_status,
                                 update_delete_image_batch_status, update_reset_db_batch_status,
                                 update_save_image_batch_status)
from routes.other_routes import fetch_image_list, update_table

from utils.constants import Endpoints, HTTPMethods
from utils.logger import logger

app = Flask(__name__)
CORS(app)

# Add user cred routes
app.add_url_rule(rule=Endpoints.ADD_USER, methods=HTTPMethods.POST_METHOD, view_func=add_user)
app.add_url_rule(rule=Endpoints.GET_USER_WITH_PWD, methods=HTTPMethods.POST_METHOD, view_func=get_user_with_pwd)
app.add_url_rule(rule=Endpoints.GET_USER, methods=HTTPMethods.GET_METHOD, view_func=get_user)
app.add_url_rule(rule=Endpoints.GET_USER_LIST, methods=HTTPMethods.GET_METHOD, view_func=get_user_list)
app.add_url_rule(rule=Endpoints.DELETE_USER, methods=HTTPMethods.DELETE_METHOD, view_func=delete_user)
app.add_url_rule(rule=Endpoints.UPDATE_USER, methods=HTTPMethods.POST_METHOD, view_func=update_user)

# Add Batch routes
app.add_url_rule(rule=Endpoints.CREATE_BATCH, methods=HTTPMethods.POST_METHOD, view_func=create_batch)
app.add_url_rule(rule=Endpoints.GET_BATCH_STATUS, methods=HTTPMethods.GET_METHOD, view_func=get_batch_status)
app.add_url_rule(rule=Endpoints.GET_BATCH_LIST, methods=HTTPMethods.GET_METHOD, view_func=get_batch_list)
app.add_url_rule(rule=Endpoints.UPDATE_SAVE_IMAGE_BATCH_STATUS, methods=HTTPMethods.POST_METHOD,
                 view_func=update_save_image_batch_status)
app.add_url_rule(rule=Endpoints.UPDATE_SIMILAR_IMAGE_BATCH_STATUS, methods=HTTPMethods.POST_METHOD,
                 view_func=update_similar_image_batch_status)
app.add_url_rule(rule=Endpoints.UPDATE_DELETE_IMAGE_BATCH_STATUS, methods=HTTPMethods.POST_METHOD,
                 view_func=update_delete_image_batch_status)
app.add_url_rule(rule=Endpoints.UPDATE_RESET_DB_BATCH_STATUS, methods=HTTPMethods.POST_METHOD,
                 view_func=update_reset_db_batch_status)

# Add Other routes
app.add_url_rule(rule=Endpoints.FETCH_IMAGE_LIST, methods=HTTPMethods.GET_METHOD, view_func=fetch_image_list)
app.add_url_rule(rule=Endpoints.UPDATE_TABLE, methods=HTTPMethods.POST_METHOD, view_func=update_table)

logger.info("MariaDB server is ready to accept requests")

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=7171)
