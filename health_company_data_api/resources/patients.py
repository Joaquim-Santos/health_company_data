from flasgger import swag_from
from flask import request
from marshmallow.exceptions import ValidationError

from health_company_data_api.common.abstract_resource import AbstractResource
from health_company_data_api.common.decorators import validate_request
from health_company_data_api.schemas import UserPostSchema
from health_company_data_api.common.exceptions import BadRequest


class PatientsResource(AbstractResource):
    service_module = 'health_company_data_api.services.patients'
    service_class = 'PatientsService'

    @validate_request
    @swag_from("../swagger/models/patients/patients-get.yml", endpoint="api.patients")
    def get(self, **kwargs):
        patients_filters = {
            'first_name': request.args.get('first_name'),
            'last_name': request.args.get('last_name'),
            'start_age': request.args.get('start_age'),
            'end_age': request.args.get('end_age')
        }

        # user_schema = UserPostSchema()
        # try:
        #     user_credentials = {
        #         'authorization': self.get_headers_request().get('Authorization', '')
        #     }
        #     user = user_schema.load(user_credentials)
        # except ValidationError as error:
        #     raise BadRequest(message=error.messages) from error

        return self.get_service().get_patients(patients_filters)
