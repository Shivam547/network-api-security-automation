from automation.clients.api_client import APIClient

def test_admin_can_login(admin_client):

    response = admin_client.get("/users/")

    assert response.status_code == 200

"""
This might look simple, but what's happening is:
Pytest
   ↓
admin_client fixture
   ↓
login()
   ↓
POST /auth/login
   ↓
JWT returned
   ↓
APIClient
   ↓
Authorization: Bearer <JWT>
   ↓
GET /users/
   ↓
200
"""

def test_get_users_without_token(unauthenticated_client):

    response = unauthenticated_client.get("/users/")

    assert response.status_code == 401

def test_invalid_token(base_url, timeout):
    client = APIClient(
        base_url=base_url,
        token = "this is invalid token",
        timeout = timeout
    )

    response = client.get("/users/")

    assert response.status_code == 401