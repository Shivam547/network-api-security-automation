import pytest


def test_missing_token(unauthenticated_client):

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401


def test_invalid_token(unauthenticated_client):

    unauthenticated_client.set_token(
        "this-is-an-invalid-jwt"
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401


def test_malformed_token(unauthenticated_client):

    unauthenticated_client.set_token(
        "abc.def"
    )

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401