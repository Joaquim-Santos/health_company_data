from base64 import b64decode

from health_company_data_api import bcrypt
from health_company_data_api.common.abstract_service import AbstractService
from health_company_data_api.common.exceptions import EntityNotFound, CustomerNotIdentified


class UsersService(AbstractService):
    repository_module = 'health_company_data_api.repositories.users'
    repository_class = 'UsersRepository'

    def authenticate_user(self, authorization: str):
        user_and_password = b64decode(authorization).decode()
        username = user_and_password.split(':')[0]
        password = ':'.join(user_and_password.split(':')[1:])

        try:
            user = self.get_repository().get_user_by_username(username)
        except EntityNotFound as exception:
            raise EntityNotFound('Usuário não encontrado.') from exception

        if not bcrypt.check_password_hash(user['password'], password):
            raise CustomerNotIdentified("Senha inválida.")

        return user['username']
