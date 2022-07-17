from health_company_data_api.repositories.users import UsersRepository


class TestUsersRepository:
    def test_create_user_with_success(self):
        expected_data = {
            "uuid": "USER0002",
            "username": "Joaquim_Santos",
            "password": "Password@test123",
        }
        new_user = {"username": "Joaquim_Santos", "password": "Password@test123"}

        assert UsersRepository().create_user(new_user) == expected_data

    def test_get_next_user_id_with_third_user(self):
        assert UsersRepository().get_next_user_id() == "USER0003"
