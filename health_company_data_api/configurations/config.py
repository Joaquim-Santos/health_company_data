import importlib
import os


class BaseConfig:

    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    LOCAL_VALIDATION = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../company_data.db'

    LOGS_FOLDER = os.environ.get("LOGS_FOLDER")

    SWAGGER = {
        'title': "Health Company Data",
        'version': 1,
        'description': "Health Company Data Endpoints"
    }


class TestConfig(BaseConfig):
    DEBUG = True
    LOCAL_VALIDATION = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/databases/company_data_test.db'


class LocalConfig(BaseConfig):
    DEBUG = True
    LOCAL_VALIDATION = True

    SQLALCHEMY_ECHO = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config():
    return getattr(importlib.import_module('health_company_data_api.configurations.config'),
                   os.environ['STAGE'].capitalize() + 'Config')
