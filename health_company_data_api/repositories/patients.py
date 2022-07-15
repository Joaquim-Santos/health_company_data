from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import PatientsModel


class PatientsRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.patients'
    model_class = 'PatientsModel'

    def get_patients(self, patients_filters: dict) -> list:
        return self.all()
