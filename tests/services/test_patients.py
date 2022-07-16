from health_company_data_api.services.patients import PatientsService


class TestPatientsService:

    def test_get_patients_with_first_name_filter_without_data(self):
        patients_filters = {
            'first_name': 'Lucas'
        }

        assert PatientsService().get_patients(patients_filters) == []

    def test_get_patients_with_first_name_filter_with_data(self):
        expected_data = [
            {'uuid': 'PATIENT0001', 'first_name': 'VITORIA', 'last_name': 'CARVALHO',
             'date_of_birth': '1990-01-01T00:00:00'},
            {'uuid': 'PATIENT0002', 'first_name': 'VITORIA', 'last_name': 'SILVA',
             'date_of_birth': '1986-07-12T00:00:00'}
        ]

        patients_filters = {
            'first_name': 'Vitoria'
        }

        assert PatientsService().get_patients(patients_filters) == expected_data
