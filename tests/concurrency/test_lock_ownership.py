def test_locked_order_reject_other_user(
    admin_client,
    manager_client
):

    # -----------------------------------------
    # Create order
    # -----------------------------------------

    create_response = admin_client.post(
        "/orders/",
        json={
            "customer_name": "Concurrent Lock Test for rejected user"
        }
    )

    assert create_response.status_code == 201

    order = create_response.json()

    order_id = order["id"]
    version = order["version"]

    # -----------------------------------------
    # Admin acquires lock
    # -----------------------------------------

    lock_response = admin_client.post(
        f"/orders/{order_id}/lock"
    )

    assert lock_response.status_code == 200

    # -----------------------------------------
    # Manager attempts update
    # -----------------------------------------

    update_response = manager_client.put(
        f"/orders/{order_id}",
        json={
            "status": "CANCELLED",
            "version": version
        }
    )

    # Manager should be rejected
    assert update_response.status_code == 429, "user rejected!"

    lock_owner_update_response = admin_client.put(
        f"/orders/{order_id}",
        json={
            "status": "CANCELLED",
            "version": version
        }
    )

    # lock owner should be able to update the response
    assert lock_owner_update_response.status_code == 200, "user allowed to update the response!"