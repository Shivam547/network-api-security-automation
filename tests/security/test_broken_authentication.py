from datetime import datetime, timedelta, timezone

import jwt

from automation.utils.auth_utils import login


def test_missing_authentication_token(unauthenticated_client):

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401

def test_invalid_jwt(unauthenticated_client):

    unauthenticated_client.set_token(
        "this-is-not-a-valid-jwt"
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401

def test_malformed_jwt(unauthenticated_client):

    unauthenticated_client.set_token(
        "abc.def.ghi"
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401


def test_tampered_jwt(base_url, timeout, unauthenticated_client):

    admin_token = login(
        base_url=base_url,
        username="admin",
        password="admin123",
        timeout=timeout
    )

    parts = admin_token.split(".")

    assert len(parts) == 3

    # Modify the payload
    tampered_payload = parts[1][:-1] + (
        "A" if parts[1][-1] != "A" else "B"
    )

    tampered_token = ".".join(
        [
            parts[0],
            tampered_payload,
            parts[2]
        ]
    )

    unauthenticated_client.set_token(
        tampered_token
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401

def test_token_signed_with_wrong_secret(
    unauthenticated_client
):

    payload = {
        "sub": "1",
        "username": "admin",
        "role": "admin"
    }

    forged_token = jwt.encode(
        payload,
        "attacker-secret",
        algorithm="HS256"
    )

    unauthenticated_client.set_token(
        forged_token
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401

def test_expired_jwt_error_message(
    unauthenticated_client
):

    payload = {
        "sub": "1",
        "username": "admin",
        "role": "admin",
        "exp": datetime.now(timezone.utc) - timedelta(
            minutes=5
        )
    }

    token = jwt.encode(
        payload,
        "super-secret-test-key",
        algorithm="HS256"
    )

    unauthenticated_client.set_token(token)

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"