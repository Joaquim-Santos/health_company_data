from http import HTTPStatus


class TestPatientsResource:

    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/health")
        responses_status.append(response.status_code)

        response = client.put("/api/health")
        responses_status.append(response.status_code)

        response = client.delete("/api/health")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED
        ]

    def test_get_without_filter_with_success(self, client):
        expected_data = [
            {'uuid': 'PATIENT0001', 'first_name': 'VITORIA', 'last_name': 'CARVALHO',
             'date_of_birth': '1990-01-01T00:00:00'},
            {'uuid': 'PATIENT0002', 'first_name': 'VITORIA', 'last_name': 'SILVA',
             'date_of_birth': '1986-07-12T00:00:00'},
            {'uuid': 'PATIENT0003', 'first_name': 'JOAQUIM', 'last_name': 'SANTOS',
             'date_of_birth': '1996-07-08T00:00:00'}
        ]

        response = client.get("/api/patients")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_first_name_filter_with_success(self, client):
        expected_data = [
            {'uuid': 'PATIENT0003', 'first_name': 'JOAQUIM', 'last_name': 'SANTOS',
             'date_of_birth': '1996-07-08T00:00:00'}
        ]

        response = client.get("/api/patients?first_name=joaquim")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_start_age_and_end_age_filter_with_success(self, client):
        expected_data = [
            {'uuid': 'PATIENT0001', 'first_name': 'VITORIA', 'last_name': 'CARVALHO',
             'date_of_birth': '1990-01-01T00:00:00'},
            {'uuid': 'PATIENT0003', 'first_name': 'JOAQUIM', 'last_name': 'SANTOS',
             'date_of_birth': '1996-07-08T00:00:00'}
        ]

        response = client.get("/api/patients?start_age=26&end_age=32")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_bad_requests(self, client):
        expected_data = {
            'error_message': {'start_age': ['Not a valid integer.']}
        }

        response = client.get("/api/patients?start_age=a")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.BAD_REQUEST)
