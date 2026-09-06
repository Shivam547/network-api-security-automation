from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

def acquire_lock(client, order_id, barrier):
    """
    Wait until all concurrent workers are ready,
    then attempt to acquire the lock / update order.
    """
    barrier.wait()
    return client.post(
        f"/orders/{order_id}/lock"
    )


# def update_order(client, order_id, status):
#     return client.put(
#         f"/orders/{order_id}",
#         json={
#             "status": status
#         }
#     )

# 2 separate users updating the same order
def test_concurrent_order_updates(admin_client, manager_client):
    """
    Verify that only one user can acquire the same
    order lock when both requests happen concurrently.
    """

    # ------------------------------------------------
    # Create a fresh order for this test
    # ------------------------------------------------
    create_response = admin_client.post(
        "/orders/",
        json={
            "customer_name": "Concurrent Lock Test"
        }
    )

    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    # ------------------------------------------------
    # Barrier ensures both threads are ready
    # before sending the requests.
    # ------------------------------------------------
    barrier = Barrier(2)

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_approved = executor.submit(
            acquire_lock,
            admin_client,
            order_id,
            barrier
        )

        future_cancelled = executor.submit(
            acquire_lock,
            manager_client,
            order_id,
            barrier
        )

        response_approved = future_approved.result()
        response_cancelled = future_cancelled.result()

    # ------------------------------------------------
    # Validate result
    # ------------------------------------------------
    statuses = {
        response_approved.status_code,
        response_cancelled.status_code
    }

    assert statuses == {200, 429}

    # Exactly one request must succeed
    assert (
        response_approved.status_code == 200
        or response_cancelled.status_code == 200
    )

    # Exactly one request must fail
    assert (
        response_approved.status_code == 429
        or response_cancelled.status_code == 429
    )