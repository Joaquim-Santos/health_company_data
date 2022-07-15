import pytest

from health_company_data_api.services.users import UsersService
from health_company_data_api.common.exceptions import IntegrityException


class TestUsersService:

    def test_create_user_with_success(self):
        expected_data = {'username': 'joaquim_santos'}
        new_user = {
            'username': 'Joaquim_Santos',
            'password': 'Password@test123'
        }

        assert UsersService().create_user(new_user) == expected_data

    def test_create_user_with_user_already_exists(self):
        new_user = {
            'username': 'user_test',
            'password': 'Password@test123'
        }

        with pytest.raises(IntegrityException,
                           match='Erro de integridade ao tentar criar ou atualizar a entidade users'):
            UsersService().create_user(new_user)
