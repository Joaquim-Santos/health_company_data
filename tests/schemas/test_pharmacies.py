import pytest

from health_company_data_api.schemas import PharmaciesFiltersSchema


class TestPharmaciesFiltersSchema:

    @pytest.fixture(autouse=True)
    def init_stuff(self):
        self.schema = PharmaciesFiltersSchema()
        self.data = {
            'name': 'DROGA MAIS',
            'city': 'RIBEIRAO PRETO'
        }

    def test_pharmacies_filters_schema_with_valid_data(self):
        result = self.schema.validate(self.data)
        assert result == {}

    def test_pharmacies_filters_schema_without_fields(self):
        self.data = {}

        result = self.schema.validate(self.data)
        assert result == {}

    def test_pharmacies_filters_schema_with_invalid_str_fields_type(self):
        self.data['name'] = self.data['city'] = 1

        result = self.schema.validate(self.data)
        assert result == {
            'name': ['Not a valid string.'],
            'city': ['Not a valid string.']
        }

    def test_pharmacies_filters_schema_with_invalid_str_fields_length(self):
        validations = []

        self.data['name'] = self.data['city'] = 'dr'
        result = self.schema.validate(self.data)
        validations.append(result)

        self.data['name'] = self.data['city'] = 'v' * 51
        result = self.schema.validate(self.data)
        validations.append(result)

        assert validations == [
            {
                'name': ['Length must be between 3 and 50.'],
                'city': ['Length must be between 3 and 50.']
            },
            {
                'name': ['Length must be between 3 and 50.'],
                'city': ['Length must be between 3 and 50.']
            }
        ]
