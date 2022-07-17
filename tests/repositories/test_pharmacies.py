from health_company_data_api.repositories.pharmacies import PharmaciesRepository


class TestPharmaciesRepository:
    def test_get_pharmacies_with_name_and_city_filter_with_data(self):
        expected_data = [
            {"uuid": "PHARM0002", "name": "DROGA MAIS", "city": "SAO PAULO"},
        ]

        pharmacies_filters = {"name": "droga mais", "city": "SAO PAULO"}

        assert (
            PharmaciesRepository().get_pharmacies(pharmacies_filters) == expected_data
        )
