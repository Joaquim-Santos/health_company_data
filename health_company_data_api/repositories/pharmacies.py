from sqlalchemy import func

from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import PharmaciesModel


class PharmaciesRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.pharmacies'
    model_class = 'PharmaciesModel'

    def _get_filter(self, field_name: str, field_value: str):
        model_filters = {
            'name': (func.lower(PharmaciesModel.name) == func.lower(field_value)),
            'city': (func.lower(PharmaciesModel.city) == func.lower(field_value))
        }

        return model_filters[field_name]

    def get_pharmacies(self, pharmacies_filters: dict) -> list:
        return self.get_entities_by_filter(pharmacies_filters)
