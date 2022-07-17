import pytest

from health_company_data_api.common.utils import Utils
from health_company_data_api.common.exceptions import BadRequest


class TestUtils:
    def test_get_decoded_user_and_password_with_valid_authorization(self):
        authorization = "Basic Sm9hcXVpbVNhbnRvczpQYXNzd29yZEB0ZXN0MTIz"
        expected_data = {"username": "JoaquimSantos", "password": "Password@test123"}

        assert expected_data == Utils.get_decoded_user_and_password(authorization)

    def test_get_decoded_user_and_password_with_invalid_authorization_encode(self):
        authorization = "a"

        with pytest.raises(BadRequest):
            Utils.get_decoded_user_and_password(authorization)

    def test_password_check_with_valid_password(self):
        password = "Pass@1234"
        expected_data = {
            "password_ok": True,
            "length_error": False,
            "digit_error": False,
            "uppercase_error": False,
            "lowercase_error": False,
            "symbol_error": False,
        }

        assert expected_data == Utils.password_check(password)

    def test_password_check_with_length_error_and_digit_error(self):
        password = "Pass@!@"
        expected_data = {
            "password_ok": False,
            "length_error": True,
            "digit_error": True,
            "uppercase_error": False,
            "lowercase_error": False,
            "symbol_error": False,
        }

        assert expected_data == Utils.password_check(password)

    def test_password_check_with_uppercase_error_and_symbol_error(self):
        password = "pass1234"
        expected_data = {
            "password_ok": False,
            "length_error": False,
            "digit_error": False,
            "uppercase_error": True,
            "lowercase_error": False,
            "symbol_error": True,
        }

        assert expected_data == Utils.password_check(password)

    def test_password_check_with_lowercase_error(self):
        password = "PASS@1234"
        expected_data = {
            "password_ok": False,
            "length_error": False,
            "digit_error": False,
            "uppercase_error": False,
            "lowercase_error": True,
            "symbol_error": False,
        }

        assert expected_data == Utils.password_check(password)

    def test_username_check_with_valid_username(self):
        username = "joaquim_santos1"

        assert Utils.username_check(username) is True

    def test_username_check_with_invalid_username(self):
        username = "joaquim@santos1"

        assert Utils.username_check(username) is False
