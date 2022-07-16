from health_company_data_api.common.abstract_service import AbstractService


class PatientsService(AbstractService):
    repository_module = 'health_company_data_api.repositories.patients'
    repository_class = 'PatientsRepository'

    def get_patients(self, patients_filters: dict) -> list:
        return self.get_repository().get_patients(patients_filters)
