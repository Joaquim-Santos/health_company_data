import pytest

from health_company_data_api import application
from health_company_data_api.common.decorators.validate_request import validate_request
from health_company_data_api.common.exceptions import (
    MissingData,
    EntityNotFound,
    CustomerNotIdentified,
)
from flask import request


class TestValidateRequest:
    def test_validate_request_with_authorized_user(self):
        request_context = application.test_request_context()
        request_context.push()

        request.headers = {
            "Authorization": "dXNlcl90ZXN0OlBhc3N3b3JkQHRlc3QxMjM=",
            "access-token": "token_test",
        }

        @validate_request
        def get_value(**kwargs):
            return kwargs

        response = get_value()

        expected_value = {
            "user_credentials": {"username": "user_test", "access-token": "token_test"}
        }

        assert response == expected_value

    def test_validate_request_with_missing_header(self):
        request_context = application.test_request_context()
        request_context.push()

        request.headers = {
            "Authorization": "Basic dXNlcl90ZXN0OlBhc3N3b3JkQHRlc3QxMjM="
        }

        @validate_request
        def get_value(**kwargs):
            return kwargs

        with pytest.raises(
            MissingData,
            match="Campos para autenticação do usuário não foram informados.",
        ):
            get_value()

    def test_validate_request_with_invalid_access_token(self):
        request_context = application.test_request_context()
        request_context.push()

        request.headers = {
            "Authorization": "Basic dXNlcl90ZXN0OlBhc3N3b3JkQHRlc3QxMjM=",
            "access-token": "token_t",
        }

        @validate_request
        def get_value(**kwargs):
            return kwargs

        with pytest.raises(CustomerNotIdentified, match="Token de acesso inválido."):
            get_value()

    def test_validate_request_with_user_not_found(self):
        request_context = application.test_request_context()
        request_context.push()

        request.headers = {
            "Authorization": "Basic dXNlcl90ZXM6UGFzc3dvcmRAdGVzdDEyMw==",
            "access-token": "token_test",
        }

        @validate_request
        def get_value(**kwargs):
            return kwargs

        with pytest.raises(EntityNotFound, match="Usuário não encontrado."):
            get_value()

    def test_validate_request_with_invalid_password(self):
        request_context = application.test_request_context()
        request_context.push()

        request.headers = {
            "Authorization": "Basic dXNlcl90ZXN0OlBhc3N3b3JkQHRlc3QxMg==",
            "access-token": "token_test",
        }

        @validate_request
        def get_value(**kwargs):
            return kwargs

        with pytest.raises(CustomerNotIdentified, match="Senha inválida."):
            get_value()
