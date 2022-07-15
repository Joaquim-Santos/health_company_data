import pytest
import os

from shutil import rmtree

from health_company_data_api import application, db
from health_company_data_api.models import *
from health_company_data_api import bcrypt


@pytest.fixture(scope="session")
def app():
    with application.app_context():
        yield application


@pytest.fixture(scope="session", autouse=True)
def create_db():
    rmtree('tests/databases', ignore_errors=True)
    os.mkdir('tests/databases')

    db.create_all()
    db.session.commit()


@pytest.fixture(scope="module", autouse=True)
def create_required_tables_data():
    db.session.query(UsersModel).delete()
    db.session.query(TransactionsModel).delete()
    db.session.query(PharmaciesModel).delete()
    db.session.query(PatientsModel).delete()

    user_1 = {
        'uuid': 'USER0001',
        'username': 'user_test',
        'password': bcrypt.generate_password_hash('Password@test123')
    }

    user_model = UsersModel(**user_1)
    db.session.add(user_model)

    db.session.commit()
