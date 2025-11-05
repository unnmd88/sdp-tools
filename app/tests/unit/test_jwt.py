import pytest

from auth.utils import encode_jwt, decode_jwt


class TestJWT:

    @pytest.fixture
    def jwt_payloads(self):
        return [
            {'iss': 'sdp'},
            {'sub': "1"},
            {'uname': "2"},
            {'sub': "3", 'uname': "2", "blabla": "bla"},
        ]

    def test_encode_jwt(self, jwt_payloads):
        for payload in jwt_payloads:
            assert isinstance(encode_jwt(payload=payload), str)

    def test_decode_jwt(self, jwt_payloads):
        for payload in jwt_payloads:
            encoded_token = encode_jwt(payload=payload)
            decoded_payload: dict = decode_jwt(token=encoded_token)
            assert 'iat' in decoded_payload
            assert 'exp' in decoded_payload
            iat = decoded_payload['iat']
            exp = decoded_payload['exp']
            assert all(isinstance(k, int) for k in (exp, iat))
            assert exp > iat
            # Все ключи и значения словаря payload присутствуют в decoded_payload
            for k, v in payload.items():
                assert decoded_payload.get(k) == v




