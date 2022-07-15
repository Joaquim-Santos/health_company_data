from marshmallow import Schema, fields, EXCLUDE, validate, post_load, pre_load
from marshmallow.exceptions import ValidationError

from health_company_data_api.common.utils import Utils
from health_company_data_api.common.exceptions import BadRequest


# Senha tem tamanho máximo de 72 caracteres por se ruma limitação da lib flask-bcrypt, para criptografar.
class UserPostSchema(Schema):
    username = fields.Str(required=True, validate=[validate.Length(min=3, max=50)])
    password = fields.Str(required=True, validate=[validate.Length(min=8, max=72)])

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def pre_load(self, data, many, **kwargs):
        try:
            data['username'], data['password'] = Utils.get_decoded_user_and_password(data['authorization'])\
                .values()
        except KeyError:
            raise ValidationError("Campo de autorização não informado.")

        return data

    @post_load
    def post_load(self, data, many, **kwargs):
        user_criteria = Utils.username_check(data['username'])
        password_criteria = Utils.password_check(data['password'])

        if not user_criteria:
            raise BadRequest('Nome de usuário pode conter apenas letras, números e underline.')
        if not password_criteria['password_ok']:
            raise BadRequest('Senha não atende aos critérios de segurança.', payload=password_criteria)

        return data
