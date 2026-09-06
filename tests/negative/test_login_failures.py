def test_invalid_username(base_url, timeout):

    import requests

    response = requests.post(
        f"{base_url}/auth/login",
        json={
            "username": "does_not_exist",
            "password": "admin123"
        },
        timeout=timeout
    )

    assert response.status_code == 401


def test_invalid_password(base_url, timeout):

    import requests

    response = requests.post(
        f"{base_url}/auth/login",
        json={
            "username": "admin",
            "password": "wrong-password"
        },
        timeout=timeout
    )

    assert response.status_code == 401