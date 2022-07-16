from health_company_data_api.common.abstract_service import AbstractService


class PharmaciesService(AbstractService):
    repository_module = 'health_company_data_api.repositories.pharmacies'
    repository_class = 'PharmaciesRepository'

    def get_pharmacies(self, pharmacies_filters: dict) -> list:
        return self.get_repository().get_pharmacies(pharmacies_filters)
