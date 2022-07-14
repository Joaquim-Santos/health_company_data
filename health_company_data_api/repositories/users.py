from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import UsersModel


class UsersRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.users'
    model_class = 'UsersModel'

    def get_user_by_username(self, username: str):
        return self.find(filters=(UsersModel.username == username))
