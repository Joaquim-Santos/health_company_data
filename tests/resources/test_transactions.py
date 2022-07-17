from http import HTTPStatus


class TestTransactionsResource:
    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.post("/api/transactions")
        responses_status.append(response.status_code)

        response = client.put("/api/transactions")
        responses_status.append(response.status_code)

        response = client.delete("/api/transactions")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
        ]

    def test_get_without_filter_with_success(self, client):
        expected_data = [
            {
                "patient_id": "PATIENT0001",
                "first_name": "VITORIA",
                "last_name": "CARVALHO",
                "date_of_birth": "1990-01-01T00:00:00",
                "pharmacy_id": "PHARM0001",
                "name": "DROGA MAIS",
                "city": "RIBEIRAO PRETO",
                "transaction_id": "TRAN0001",
                "amount": 29.0,
                "timestamp": "2022-05-01T08:00:00",
            },
            {
                "patient_id": "PATIENT0001",
                "first_name": "VITORIA",
                "last_name": "CARVALHO",
                "date_of_birth": "1990-01-01T00:00:00",
                "pharmacy_id": "PHARM0002",
                "name": "DROGA MAIS",
                "city": "SAO PAULO",
                "transaction_id": "TRAN0002",
                "amount": 30.5,
                "timestamp": "2022-05-01T13:00:00",
            },
            {
                "patient_id": "PATIENT0002",
                "first_name": "VITORIA",
                "last_name": "SILVA",
                "date_of_birth": "1986-07-12T00:00:00",
                "pharmacy_id": "PHARM0003",
                "name": "DROGARIA SAO SIMAO",
                "city": "SAO PAULO",
                "transaction_id": "TRAN0003",
                "amount": 40.0,
                "timestamp": "2022-05-10T08:00:00",
            },
        ]

        response = client.get("/api/transactions")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_amount_filter_with_success(self, client):
        expected_data = [
            {
                "patient_id": "PATIENT0001",
                "first_name": "VITORIA",
                "last_name": "CARVALHO",
                "date_of_birth": "1990-01-01T00:00:00",
                "pharmacy_id": "PHARM0002",
                "name": "DROGA MAIS",
                "city": "SAO PAULO",
                "transaction_id": "TRAN0002",
                "amount": 30.5,
                "timestamp": "2022-05-01T13:00:00",
            },
            {
                "patient_id": "PATIENT0002",
                "first_name": "VITORIA",
                "last_name": "SILVA",
                "date_of_birth": "1986-07-12T00:00:00",
                "pharmacy_id": "PHARM0003",
                "name": "DROGARIA SAO SIMAO",
                "city": "SAO PAULO",
                "transaction_id": "TRAN0003",
                "amount": 40.0,
                "timestamp": "2022-05-10T08:00:00",
            },
        ]

        response = client.get("/api/transactions?from_amount=30.1")
        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_get_with_bad_requests(self, client):
        expected_data = {
            "error_message": {"from_amount": ["Must be greater than or equal to 0."]}
        }

        response = client.get("/api/transactions?from_amount=-1")
        assert (response.json, response.status_code) == (
            expected_data,
            HTTPStatus.BAD_REQUEST,
        )
