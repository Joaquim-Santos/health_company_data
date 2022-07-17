from http import HTTPStatus


class TestPharmaciesResource:
    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/pharmacies")
        responses_status.append(response.status_code)

        response = client.put("/api/pharmacies")
        responses_status.append(response.status_code)

        response = client.delete("/api/pharmacies")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
        ]

    def test_get_without_filter_with_success(self, client):
        expected_data = [
            {"uuid": "PHARM0001", "name": "DROGA MAIS", "city": "RIBEIRAO PRETO"},
            {"uuid": "PHARM0002", "name": "DROGA MAIS", "city": "SAO PAULO"},
            {"uuid": "PHARM0003", "name": "DROGARIA SAO SIMAO", "city": "SAO PAULO"},
        ]

        response = client.get("/api/pharmacies")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_name_filter_with_success(self, client):
        expected_data = [
            {"uuid": "PHARM0001", "name": "DROGA MAIS", "city": "RIBEIRAO PRETO"},
            {"uuid": "PHARM0002", "name": "DROGA MAIS", "city": "SAO PAULO"},
        ]

        response = client.get("/api/pharmacies?name=droga MAIS")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_bad_requests(self, client):
        expected_data = {
            "error_message": {"city": ["Length must be between 3 and 50."]}
        }

        response = client.get("/api/pharmacies?city=a")
        assert (response.json, response.status_code) == (
            expected_data,
            HTTPStatus.BAD_REQUEST,
        )
