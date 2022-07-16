from http import HTTPStatus


class TestSignUpResource:

    def test_methods_not_allowed(self, client):
        responses_status = []

        response = client.get("/api/signup")
        responses_status.append(response.status_code)

        response = client.put("/api/signup")
        responses_status.append(response.status_code)

        response = client.delete("/api/signup")
        responses_status.append(response.status_code)

        assert responses_status == [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.METHOD_NOT_ALLOWED
        ]

    def test_post_with_success(self, client):
        expected_data = {'username': 'joaquimsantos'}
        headers = {'Authorization': 'Basic Sm9hcXVpbVNhbnRvczpOYXRoQDI2MDIyMDIw'}

        response = client.post("/api/signup", headers=headers)

        assert (response.json, response.status_code) == (expected_data, HTTPStatus.OK)

    def test_post_with_bad_request(self, client):
        expected_data = {
            'digit_error': False,
            'error_message': 'Senha não atende aos critérios de segurança.',
            'length_error': False,
            'lowercase_error': False,
            'password_ok': False,
            'symbol_error': True,
            'uppercase_error': False
        }
        headers = {'Authorization': 'Basic Sm9hcXVpbVNhbnRvczpQYXNzMTIzNDU2'}

        response = client.post("/api/signup", headers=headers)

        assert (response.json, response.status_code) == (expected_data, HTTPStatus.BAD_REQUEST)
