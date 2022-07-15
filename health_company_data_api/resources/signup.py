from flasgger import swag_from
from marshmallow.exceptions import ValidationError

from health_company_data_api.common.abstract_resource import AbstractResource
from health_company_data_api.common.decorators import validate_request
from health_company_data_api.schemas import UserPostSchema
from health_company_data_api.common.exceptions import BadRequest


class SignUpResource(AbstractResource):
    service_module = 'health_company_data_api.services.users'
    service_class = 'UsersService'

    @validate_request
    @swag_from("../swagger/models/signup/signup.yml", endpoint="api.signup")
    def post(self, **kwargs):
        user_schema = UserPostSchema()
        try:
            user_credentials = {
                'authorization': self.get_headers_request().get('Authorization', '')
            }
            user = user_schema.load(user_credentials)
        except ValidationError as error:
            raise BadRequest(message=error.messages) from error

        return self.get_service().create_user(user)
