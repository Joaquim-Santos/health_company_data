import pytest

from decimal import Decimal
from datetime import datetime, date

from health_company_data_api.common.serializer import Serializer
from health_company_data_api.common.exceptions.type_not_identified import (
    TypeNotIdentified,
)


class TestSerializer:
    @staticmethod
    def test_json_serialize_str():
        serializer = Serializer()
        assert isinstance(serializer.json_serialize("valor"), str)

    @staticmethod
    def test_json_serialize_dict():
        serializer = Serializer()
        patient = {
            "first_name": "Joaquim",
            "last_name": "Santos",
            "date_of_birth": "2020-07-08",
        }

        assert isinstance(serializer.json_serialize(patient), str)

    @staticmethod
    def test_json_serialize_datetime():
        serializer = Serializer()
        assert isinstance(serializer.json_serialize(datetime.now()), str)

    @staticmethod
    def test_json_serialize_date():
        serializer = Serializer()
        assert isinstance(serializer.json_serialize(date(2022, 1, 1)), str)

    @staticmethod
    def test_json_serialize_decimal():
        serializer = Serializer()
        assert isinstance(serializer.json_serialize(Decimal(1.2)), float)

    @staticmethod
    def test_json_serialize_bytes():
        serializer = Serializer()
        assert isinstance(serializer.json_serialize(b"aaa"), bytes)

    @staticmethod
    def test_json_serialize_type_not_identified():
        serializer = Serializer()
        with pytest.raises(TypeNotIdentified):
            serializer.json_serialize(Serializer)
