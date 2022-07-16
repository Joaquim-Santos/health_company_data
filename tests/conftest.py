import pytest
import os

from shutil import rmtree
from datetime import datetime

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

    patient_1 = {
        'uuid': 'PATIENT0001',
        'first_name': 'VITORIA',
        'last_name': 'CARVALHO',
        'date_of_birth': datetime(1990, 1, 1, 0, 0, 0, 0)
    }

    patient_model = PatientsModel(**patient_1)
    db.session.add(patient_model)

    patient_2 = {
        'uuid': 'PATIENT0002',
        'first_name': 'VITORIA',
        'last_name': 'SILVA',
        'date_of_birth': datetime(1986, 7, 12, 0, 0, 0, 0)
    }

    patient_model = PatientsModel(**patient_2)
    db.session.add(patient_model)

    patient_3 = {
        'uuid': 'PATIENT0003',
        'first_name': 'JOAQUIM',
        'last_name': 'SANTOS',
        'date_of_birth': datetime(1996, 7, 8, 0, 0, 0, 0)
    }

    patient_model = PatientsModel(**patient_3)
    db.session.add(patient_model)

    pharmacies_1 = {
        'uuid': 'PHARM0001',
        'name': 'DROGA MAIS',
        'city': 'RIBEIRAO PRETO'
    }

    pharmacies_model = PharmaciesModel(**pharmacies_1)
    db.session.add(pharmacies_model)

    pharmacies_2 = {
        'uuid': 'PHARM0002',
        'name': 'DROGA MAIS',
        'city': 'SAO PAULO'
    }

    pharmacies_model = PharmaciesModel(**pharmacies_2)
    db.session.add(pharmacies_model)

    pharmacies_3 = {
        'uuid': 'PHARM0003',
        'name': 'DROGARIA SAO SIMAO',
        'city': 'SAO PAULO'
    }

    pharmacies_model = PharmaciesModel(**pharmacies_3)
    db.session.add(pharmacies_model)

    db.session.commit()
