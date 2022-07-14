from flask import Flask
from flask import jsonify
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask import request

from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

from health_company_data_api.configurations.routes_builder import RoutesBuilder
from health_company_data_api.common import exceptions
from health_company_data_api.configurations.config import get_config
from health_company_data_api.common.logger import Logger


application = Flask(__name__)
application.config.from_object(get_config())
Compress(application)


swagger = Swagger(application, template_file='swagger/template.yml')

db = SQLAlchemy(application)
db.init_app(application)

# Adiciona-se as rotas da aplicação com base no ambiente.
builder = RoutesBuilder()
builder.add_resources(application=application, router_file_path='health_company_data_api/configurations/routes.json')

# Configuração das opções de CORS para cada rota.
builder.add_cors(application=application, router_file_path='health_company_data_api/configurations/routes.json')

logger = Logger(get_config(), "health_company_data_api", 'health_company_data_api.log')


def handle_exception(error):
    """
        Função que trata exceções lançadas pela aplicação.

        Parameters
        ----------
        error: AbstractException
            Exceção a ser tratada.

        Return
        ----------
        response: JSON
            Objeto JSON com dados da exceção.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    logger.log.exception(f'endpoint: {request.method} {request.url}\n{error.message}', exc_info=error)
    return response


def handle_integrity_error(error):
    """
        Função que trata exceção do tipo sqlalchemy.exc.IntegrityError lançada pela aplicação.

        Parameters
        ----------
        error: IntegrityError
            Exceção a ser tratada.

        Return
        ----------
        response: JSON
            Objeto JSON com dados da exceção.
    """
    logger.log.exception(f'endpoint: {request.method} {request.url}\n{error.orig}', exc_info=error)
    return jsonify({'error_message': 'IntegrityError: ' + str(error.orig)}), 422


def handle_generic_error(error):
    """
        Função que trata exceção genéricas lançadas pela aplicação.

        Parameters
        ----------
        error: Exception
            Exceção a ser tratada.

        Return
        ----------
        response: JSON
            Objeto JSON com dados da exceção.
    """
    logger.log.exception(f'endpoint: {request.method} {request.url}\n{error}', exc_info=error)
    return jsonify({'error_message': 'generic_error: ' + str(error)}), 500


# Configura a aplicação para tratar as exceções especificadas com o método informado.
application.register_error_handler(exceptions.IntegrityException, handle_exception)
application.register_error_handler(exceptions.GenericException, handle_exception)
application.register_error_handler(exceptions.EntityNotFound, handle_exception)
application.register_error_handler(exceptions.ConnectionFailed, handle_exception)
application.register_error_handler(exceptions.MissingData, handle_exception)
application.register_error_handler(exceptions.CannotBeBlank, handle_exception)
application.register_error_handler(exceptions.CustomerNotIdentified, handle_exception)
application.register_error_handler(exceptions.BadRequest, handle_exception)
application.register_error_handler(exceptions.MethodNotAllowed, handle_exception)
application.register_error_handler(ValidationError, handle_exception)
application.register_error_handler(Exception, handle_generic_error)
application.register_error_handler(IntegrityError, handle_integrity_error)


@application.before_request
def log_request_info():
    logger.log.info(f'Acesso ao endpoint: {request.method} {request.url}\n'
                    f'Headers:\n{request.headers}'
                    f'Args: {dict(request.args)}\n'
                    f'Data: {request.get_data()}\n')


@application.after_request
def after_request(response):
    logger.log.info(f'Resposta com sucesso do endpoint: {request.method} {request.url}\n'
                    f'data:\n{response}')

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,chave-petrobras')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
