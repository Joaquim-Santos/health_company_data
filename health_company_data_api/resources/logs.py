from flasgger import swag_from
from flask import request
from flask import Response

from health_company_data_api.common.abstract_resource import BaseResource
from health_company_data_api.common.file_handler import get_log_files, load_file
from health_company_data_api.configurations.config import get_config


class LogsResource(BaseResource):

    @swag_from("../swagger/models/logs_files/logs-files.yml", endpoint="api.logs")
    def get(self, **kwargs):
        content = get_log_files(get_config().LOGS_FOLDER)
        return {"log_files": content}


class LogsFileNameResource(BaseResource):

    @swag_from("../swagger/models/logs_filename/logs-filename-get.yml", endpoint="api.logs_filename")
    def get(self, **kwargs):
        content = load_file(get_config().LOGS_FOLDER, request.view_args['filename'], False)
        return Response(content, mimetype="application/text")
