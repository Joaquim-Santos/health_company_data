from sqlalchemy import desc

from health_company_data_api.common.abstract_repository import AbstractRepository
from health_company_data_api.models import UsersModel


class UsersRepository(AbstractRepository):
    model_module = 'health_company_data_api.models.users'
    model_class = 'UsersModel'

    def __init__(self):
        self.__uuid_pattern = 'USER000'

    def get_user_by_username(self, username: str) -> dict:
        return self.find(filters=(UsersModel.username == username))

    def get_next_user_id(self) -> str:
        last_user = UsersModel.query.order_by(desc(UsersModel.uuid))\
            .first()

        try:
            last_user_id = last_user.to_json()['uuid']
            number = last_user_id.replace(self.__uuid_pattern, '')
            number = int(number) + 1
        except AttributeError:
            number = 1

        return f'{self.__uuid_pattern}{number}'

    def create_user(self, user: dict) -> dict:
        user['uuid'] = self.get_next_user_id()

        return self.create(user)
