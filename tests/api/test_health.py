def test_health_check(unauthenticated_client):

    response = unauthenticated_client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "UP"