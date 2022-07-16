from flasgger import swag_from
from flask import request
from marshmallow.exceptions import ValidationError

from health_company_data_api.common.abstract_resource import AbstractResource
from health_company_data_api.common.decorators import validate_request
from health_company_data_api.schemas import TransactionsFiltersSchema
from health_company_data_api.common.exceptions import BadRequest


class TransactionsResource(AbstractResource):
    service_module = 'health_company_data_api.services.transactions'
    service_class = 'TransactionsService'

    @validate_request
    @swag_from("../swagger/models/transactions/transactions-get.yml", endpoint="api.transactions")
    def get(self, **kwargs):
        transactions_filters = {
            'from_amount': request.args.get('from_amount'),
            'from_timestamp': request.args.get('from_timestamp')
        }

        transactions_filters_schema = TransactionsFiltersSchema()
        try:
            transactions_filters = transactions_filters_schema.load(transactions_filters)
        except ValidationError as error:
            raise BadRequest(message=error.messages) from error

        return self.get_service().get_transactions(transactions_filters)
