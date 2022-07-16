from sqlalchemy import func
from datetime import datetime
from typing import Union

from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import PatientsModel


class PatientsRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.patients'
    model_class = 'PatientsModel'

    @staticmethod
    def _get_filter(field_name: str, field_value: Union[str, datetime]):
        model_filters = {
            'first_name': (func.lower(PatientsModel.first_name) == func.lower(field_value)),
            'last_name': (func.lower(PatientsModel.last_name) == func.lower(field_value)),
            'start_age': (PatientsModel.date_of_birth <= field_value),
            'end_age': (PatientsModel.date_of_birth >= field_value)
        }

        return model_filters[field_name]

    def get_patients(self, patients_filters: dict) -> list:
        filters = ()

        for field_name, field_value in patients_filters.items():
            try:
                filters &= self._get_filter(field_name, field_value)
            except TypeError:
                filters = self._get_filter(field_name, field_value)

        return self.find_many(filters=filters)
