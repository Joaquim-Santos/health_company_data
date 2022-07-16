import binascii
import re

from base64 import b64decode
from typing import Dict

from health_company_data_api.common.exceptions import BadRequest


class Utils:
    """
        Classe que fornece métodos genéricos úteis.
    """

    @staticmethod
    def get_decoded_user_and_password(authorization: str) -> Dict[str, str]:
        try:
            authorization = authorization.replace('Basic ', '')
            user_and_password = b64decode(authorization).decode()

            username = user_and_password.split(':')[0]
            password = ':'.join(user_and_password.split(':')[1:])
        except binascii.Error as error:
            raise BadRequest('Dados de autorização em codificação inválida de base 64.') from error

        return {
            'username': username,
            'password': password
        }

    @staticmethod
    def password_check(password: str) -> Dict[str, bool]:
        """
        Verifica a 'força' da senha. Retorna um dicionário indicando o critério inválido.
        Uma senha é considerada forte se tem pelo menos:
            Tamanho de 8 caracteres.
            1 número.
            1 símbolo especial.
            1 letra maiúscula.
            1 letra minúscula.
        """

        # Verificação de tamanho.
        length_error = len(password) < 8

        # Busca por números.
        digit_error = re.search(r"\d", password) is None

        # Busca por letras maiúsculas.
        uppercase_error = re.search(r"[A-Z]", password) is None

        # Busca por letras minúsculas.
        lowercase_error = re.search(r"[a-z]", password) is None

        # Busca por caracteres especiais.
        symbol_error = re.search(r"[ !#$%&@:'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

        # Resultado geral
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        return {
            'password_ok': password_ok,
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'symbol_error': symbol_error
        }

    @staticmethod
    def username_check(username: str) -> bool:
        """
        Verifica se um nome de usuário possui caracteres não permitidos.
        O nome pode conter apenas letras, números e underline.
        """

        return re.search(r"[ !#$%&@:'()*+,-./[\\\]^`{|}~" + r'"]', username) is None
