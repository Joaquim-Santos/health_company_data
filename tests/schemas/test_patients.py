import pytest

from health_company_data_api.schemas import PatientsFiltersSchema
from marshmallow.exceptions import ValidationError


class TestPatientsFiltersSchema:

    @pytest.fixture(autouse=True)
    def init_stuff(self):
        self.schema = PatientsFiltersSchema()
        self.data = {
            'first_name': 'Vitoria',
            'last_name': 'Silva',
            'start_age': 20,
            'end_age': 40
        }

    def test_patients_filters_schema_with_valid_data(self):
        result = self.schema.validate(self.data)
        assert result == {}

    def test_patients_filters_schema_without_fields(self):
        self.data = {}

        result = self.schema.validate(self.data)
        assert result == {}

    def test_patients_filters_schema_with_invalid_str_fields_type(self):
        self.data['first_name'] = self.data['last_name'] = 1

        result = self.schema.validate(self.data)
        assert result == {
            'first_name': ['Not a valid string.'],
            'last_name': ['Not a valid string.']
        }

    def test_patients_filters_schema_with_invalid_str_fields_length(self):
        validations = []

        self.data['first_name'] = self.data['last_name'] = 'vi'
        result = self.schema.validate(self.data)
        validations.append(result)

        self.data['first_name'] = self.data['last_name'] = 'v' * 31
        result = self.schema.validate(self.data)
        validations.append(result)

        assert validations == [
            {
                'first_name': ['Length must be between 3 and 30.'],
                'last_name': ['Length must be between 3 and 30.']
            },
            {
                'first_name': ['Length must be between 3 and 30.'],
                'last_name': ['Length must be between 3 and 30.']
            }
        ]

    def test_patients_filters_schema_with_invalid_int_fields_type(self):
        self.data['start_age'] = self.data['end_age'] = 'a'

        result = self.schema.validate(self.data)
        assert result == {
            'start_age': ['Not a valid integer.'],
            'end_age': ['Not a valid integer.']
        }

    def test_patients_filters_schema_with_invalid_int_fields_range(self):
        self.data['start_age'] = self.data['end_age'] = 17

        result = self.schema.validate(self.data)
        assert result == {
            'start_age': ['Must be greater than or equal to 18.'],
            'end_age': ['Must be greater than or equal to 18.']
        }

    def test_patients_filters_schema_with_start_age_bigger_than_end_age(self):
        self.data['start_age'] = 41

        with pytest.raises(ValidationError, match="Idade inicial não pode ser maior do que a final."):
            self.schema.load(self.data)
