from health_company_data_api.common.decorators.validate_request_local import (
    validate_request_local,
)


class TestValidateRequestLocal:
    def test_validate_request_local_with_success(self):
        @validate_request_local
        def get_value(**kwargs):
            return kwargs

        response = get_value()

        expected_value = {
            "user_credentials": {"username": "user_test", "access-token": "token_test"}
        }

        assert response == expected_value
