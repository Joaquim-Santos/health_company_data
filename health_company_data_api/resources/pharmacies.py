from flasgger import swag_from
from flask import request
from marshmallow.exceptions import ValidationError

from health_company_data_api.common.abstract_resource import AbstractResource
from health_company_data_api.common.decorators import validate_request
from health_company_data_api.schemas import PharmaciesFiltersSchema
from health_company_data_api.common.exceptions import BadRequest


class PharmaciesResource(AbstractResource):
    service_module = "health_company_data_api.services.pharmacies"
    service_class = "PharmaciesService"

    @validate_request
    @swag_from(
        "../swagger/models/pharmacies/pharmacies-get.yml", endpoint="api.pharmacies"
    )
    def get(self, **kwargs):
        pharmacies_filters = {
            "name": request.args.get("name"),
            "city": request.args.get("city"),
        }

        patients_filters_schema = PharmaciesFiltersSchema()
        try:
            pharmacies_filters = patients_filters_schema.load(pharmacies_filters)
        except ValidationError as error:
            raise BadRequest(message=error.messages) from error

        return self.get_service().get_pharmacies(pharmacies_filters)
