from http import HTTPStatus
from datetime import datetime


class TestHealthResource:

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

    def test_get_with_success(self, client):
        data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        response = client.get("/api/health")
        assert (response.json, response.status_code) == (data, HTTPStatus.OK)
