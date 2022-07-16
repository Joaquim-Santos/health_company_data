from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import TransactionsModel, PatientsModel, PharmaciesModel


class TransactionsRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.transactions'
    model_class = 'TransactionsModel'

    def _get_filter(self, field_name: str, field_value: str):
        model_filters = {
            'from_amount': (TransactionsModel.amount >= field_value),
            'from_timestamp': (TransactionsModel.timestamp >= field_value)
        }

        return model_filters[field_name]

    def get_transactions(self, transactions_filters: dict) -> list:
        join_query = TransactionsModel.query. \
            join(PatientsModel, TransactionsModel.patient_uuid == PatientsModel.uuid). \
            join(PharmaciesModel, TransactionsModel.pharmacy_uuid == PharmaciesModel.uuid)\
            .add_columns(PatientsModel.uuid.label('patient_id'), PatientsModel.first_name, PatientsModel.last_name,
                         PatientsModel.date_of_birth,
                         PharmaciesModel.uuid.label('pharmacy_id'), PharmaciesModel.name, PharmaciesModel.city,
                         TransactionsModel.uuid.label('transaction_id'), TransactionsModel.amount,
                         TransactionsModel.timestamp)

        return self.get_entities_by_filter(transactions_filters, join_query)
