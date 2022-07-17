from health_company_data_api.services.transactions import TransactionsService
from datetime import datetime


class TestTransactionsService:
    def test_get_transactions_with_amount_filter_without_data(self):
        transactions_filters = {"from_amount": 40.1}

        assert TransactionsService().get_transactions(transactions_filters) == []

    def test_get_transactions_with_timestamp_filter_with_data(self):
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
        transactions_filters = {"from_timestamp": datetime(2022, 5, 1, 13, 0, 0, 0)}

        assert (
            TransactionsService().get_transactions(transactions_filters)
            == expected_data
        )
