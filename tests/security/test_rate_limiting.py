def test_rate_limit(
    user_client
):

    responses = []

    for _ in range(6):

        response = user_client.get(
            "/rate-limit/test"
        )

        responses.append(response)

    statuses = [
        response.status_code
        for response in responses
    ]

    assert statuses[:5] == [200, 200, 200, 200, 200]
    assert statuses[5] == 429

# def test_rate_limit_returns_retry_after(
#     user_client
# ):

#     for _ in range(5):

#         response = user_client.get(
#             "/rate-limit/test"
#         )

#         assert response.status_code == 200

#     response = user_client.get(
#         "/rate-limit/test"
#     )

#     assert response.status_code == 429

#     assert "Retry-After" in response.headers

#     retry_after = int(
#         response.headers["Retry-After"]
#     )

#     assert retry_after > 0