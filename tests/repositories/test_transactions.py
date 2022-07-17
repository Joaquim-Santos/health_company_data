from health_company_data_api.repositories.transactions import TransactionsRepository
from datetime import datetime


class TestTransactionsRepository:
    def test_get_transactions_with_amount_and_timestamp_filter_with_data(self):
        expected_data = [
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
            }
        ]
        transactions_filters = {
            "from_amount": 31,
            "from_timestamp": datetime(2022, 5, 1, 13, 0, 0, 0),
        }

        assert (
            TransactionsRepository().get_transactions(transactions_filters)
            == expected_data
        )
