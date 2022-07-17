from datetime import datetime
from flasgger import swag_from

from health_company_data_api.common.abstract_resource import BaseResource
from health_company_data_api.common.decorators import validate_request


class HealthResource(BaseResource):
    @validate_request
    @swag_from("../swagger/models/health/health.yml", endpoint="api.health")
    def get(self, **kwargs):
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S")
