import functools
import os

from flask import request

from health_company_data_api.common.exceptions import MissingData, CustomerNotIdentified
from health_company_data_api.services.users import UsersService


def validate_request(func):
    @functools.wraps(func)
    def wrapper_validate_request(*args, **kwargs):
        try:
            authorization = request.headers['Authorization'].replace('Basic ', '')
            send_access_token = request.headers['access-token']
        except KeyError:
            raise MissingData('Campos para autenticação do usuário não foram informados.')

        real_access_token = os.environ.get("access_token", "")
        if send_access_token != real_access_token:
            raise CustomerNotIdentified("Token de acesso inválido.")

        username = UsersService().authenticate_user(authorization)

        kwargs['user_credentials'] = {
                    'username': username,
                    'access-token': send_access_token
                }
        return func(*args, **kwargs)

    return wrapper_validate_request
