import pytest

from health_company_data_api.schemas import TransactionsFiltersSchema


class TestTransactionsFiltersSchema:

    @pytest.fixture(autouse=True)
    def init_stuff(self):
        self.schema = TransactionsFiltersSchema()
        self.data = {
            'from_amount': 30.5,
            'from_timestamp': '2020-05-01 08:00:00'
        }

    def test_transactions_filters_schema_with_valid_data(self):
        result = self.schema.validate(self.data)
        assert result == {}

    def test_transactions_filters_schema_without_fields(self):
        self.data = {}

        result = self.schema.validate(self.data)
        assert result == {}

    def test_transactions_filters_schema_with_invalid_number_fields_type(self):
        self.data['from_amount'] = 'a'

        result = self.schema.validate(self.data)
        assert result == {
            'from_amount': ['Not a valid number.']
        }

    def test_transactions_filters_schema_with_invalid_number_fields_range(self):
        self.data['from_amount'] = -1

        result = self.schema.validate(self.data)
        assert result == {
            'from_amount': ['Must be greater than or equal to 0.']
        }

    def test_transactions_filters_schema_with_invalid_datetime_fields_format(self):
        self.data['from_timestamp'] = '2022/01/01'

        result = self.schema.validate(self.data)
        assert result == {
            'from_timestamp': ['Not a valid datetime.']
        }
