from health_company_data_api import bcrypt
from health_company_data_api.common.abstract_service import AbstractService
from health_company_data_api.common.exceptions import (
    EntityNotFound,
    CustomerNotIdentified,
)
from health_company_data_api.common.utils import Utils


class UsersService(AbstractService):
    repository_module = "health_company_data_api.repositories.users"
    repository_class = "UsersRepository"

    @staticmethod
    def set_username_in_pattern(username: str) -> str:
        return username.lower()

    def authenticate_user(self, authorization: str):
        username, password = Utils.get_decoded_user_and_password(authorization).values()
        username = self.set_username_in_pattern(username)

        try:
            user = self.get_repository().get_user_by_username(username)
        except EntityNotFound as exception:
            raise EntityNotFound("Usuário não encontrado.") from exception

        if not bcrypt.check_password_hash(user["password"], password):
            raise CustomerNotIdentified("Senha inválida.")

        return user["username"]

    def create_user(self, user: dict) -> dict:
        user["username"] = self.set_username_in_pattern(user["username"])
        user["password"] = bcrypt.generate_password_hash(user["password"])

        new_user = self.get_repository().create_user(user)

        return {"username": new_user["username"]}
