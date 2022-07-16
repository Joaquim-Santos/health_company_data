from datetime import datetime

from health_company_data_api.repositories.patients import PatientsRepository


class TestPatientsRepository:

    def test_get_patients_with_first_name_and_last_name_filter_with_data(self):
        expected_data = [
            {'uuid': 'PATIENT0001', 'first_name': 'VITORIA', 'last_name': 'CARVALHO',
             'date_of_birth': '1990-01-01T00:00:00'}
        ]

        patients_filters = {
            'first_name': 'Vitoria',
            'last_name': 'CARVALHO'
        }

        assert PatientsRepository().get_patients(patients_filters) == expected_data

    def test_get_patients_with_end_age_filter_with_data(self):
        expected_data = [
            {'uuid': 'PATIENT0003', 'first_name': 'JOAQUIM', 'last_name': 'SANTOS',
             'date_of_birth': '1996-07-08T00:00:00'}
        ]

        patients_filters = {
            'end_age': datetime(1990, 1, 1, 0, 0, 0, 0)
        }

        assert PatientsRepository().get_patients(patients_filters) == expected_data
