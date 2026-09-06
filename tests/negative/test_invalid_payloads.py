def test_create_order_missing_customer_name(admin_client):

    response = admin_client.post(
        "/orders/",
        json={}
    )

    assert response.status_code == 422

def test_create_order_invalid_customer_name_type(admin_client):

    response = admin_client.post(
        "/orders/",
        json={
            "customer_name": 12345
        }
    )

    assert response.status_code == 422

def test_update_order_missing_version(admin_client):

    create_response = admin_client.post(
        "/orders/",
        json={
            "customer_name": "Negative Test Order"
        }
    )

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    response = admin_client.put(
        f"/orders/{order_id}",
        json={
            "status": "APPROVED"
        }
    )

    assert response.status_code == 422