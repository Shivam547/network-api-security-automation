def test_get_nonexistent_order(admin_client):

    response = admin_client.get(
        "/orders/999999"
    )

    assert response.status_code == 404


def test_get_nonexistent_user(admin_client):

    response = admin_client.get(
        "/users/999999"
    )

    assert response.status_code == 404