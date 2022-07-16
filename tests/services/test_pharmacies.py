from health_company_data_api.services.pharmacies import PharmaciesService


class TestPharmaciesService:

    def test_get_pharmacies_with_city_filter_without_data(self):
        pharmacies_filters = {
            'city': 'Viçosa'
        }

        assert PharmaciesService().get_pharmacies(pharmacies_filters) == []

    def test_get_pharmacies_with_city_filter_with_data(self):
        expected_data = [
            {'uuid': 'PHARM0001', 'name': 'DROGA MAIS', 'city': 'RIBEIRAO PRETO'}
        ]

        pharmacies_filters = {
            'city': 'RIBEIRAO PRETO'
        }

        assert PharmaciesService().get_pharmacies(pharmacies_filters) == expected_data
