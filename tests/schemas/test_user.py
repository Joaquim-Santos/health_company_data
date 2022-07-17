import pytest

from health_company_data_api.schemas import UserPostSchema
from health_company_data_api.common.exceptions import BadRequest


class TestUserPostSchema:
    @pytest.fixture(autouse=True)
    def init_stuff(self):
        self.schema = UserPostSchema()
        self.data = {"authorization": "Basic dXNlcl90ZXN0OlBhc3N3b3JkQHRlc3QxMjM="}

    def test_user_post_schema_with_valid_data(self):
        result = self.schema.validate(self.data)
        assert result == {}

    def test_user_post_schema_with_missing_authorization_field(self):
        del self.data["authorization"]

        result = self.schema.validate(self.data)
        assert result == {"_schema": ["Campo de autorização não informado."]}

    def test_user_post_schema_with_invalid_username(self):
        self.data[
            "authorization"
        ] = "Basic Sm9hcXVpbUBTYW50b3M6UGFzc3dvcmRAdGVzdDEyMw=="

        with pytest.raises(
            BadRequest,
            match="Nome de usuário pode conter apenas letras, números e underline.",
        ):
            self.schema.load(self.data)

    def test_user_post_schema_with_invalid_password(self):
        self.data["authorization"] = "Basic Sm9hcXVpbVNhbnRvczpQYXNzMTIzNDU2"

        with pytest.raises(
            BadRequest, match="Senha não atende aos critérios de segurança."
        ):
            self.schema.load(self.data)
