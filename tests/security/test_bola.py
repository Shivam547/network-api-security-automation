def test_user_can_access_own_resource(user_client):

    response = user_client.get("/users/3")

    assert response.status_code == 200

def test_user_cannot_access_another_users_resource(user_client):

    response = user_client.get("/users/1")

    assert response.status_code == 403