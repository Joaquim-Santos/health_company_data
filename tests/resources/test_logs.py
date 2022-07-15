from http import HTTPStatus


class TestLogsResource:

    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/logs")
        responses_status.append(response.status_code)

        response = client.put("/api/logs")
        responses_status.append(response.status_code)

        response = client.delete("/api/logs")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED
        ]

    def test_get_with_success(self, client):
        expected_data = {
            'log_files': ['health_company_data_api.log']
        }

        response = client.get("/api/logs")

        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)


class TestLogsFileNameResource:

    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/logs/health_company_data_api.log")
        responses_status.append(response.status_code)

        response = client.put("/api/logs/health_company_data_api.log")
        responses_status.append(response.status_code)

        response = client.delete("/api/logs/health_company_data_api.log")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.INTERNAL_SERVER_ERROR
        ]

    def test_get_with_success(self, client):
        # Gerar exceção para preencher o arquivo de log (PUT não é permitido).
        client.put("/api/logs/health_company_data_api.log")

        response = client.get("/api/logs/health_company_data_api.log")
        log_validation = 'put() got an unexpected keyword argument \'filename\'' in response.data.decode("utf-8")

        assert (log_validation, response.status_code) == (True, HTTPStatus.OK)

    def test_get_with_file_not_found(self, client):
        expected_message = {'error_message': 'Arquivo health_company_data_api.txt não encontrado.'}

        response = client.get("/api/logs/health_company_data_api.txt")

        assert (response.json, response.status_code) == (expected_message, HTTPStatus.NOT_FOUND)
