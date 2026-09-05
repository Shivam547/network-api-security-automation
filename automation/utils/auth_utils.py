import requests


def login(base_url, username, password, timeout=10):

    response = requests.post(
        f"{base_url}/auth/login",
        json={
            "username": username,
            "password": password
        },
        timeout=timeout
    )

    response.raise_for_status()

    return response.json()["access_token"]