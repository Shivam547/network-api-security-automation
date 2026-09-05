def test_admin_can_access_users(admin_client):
    response = admin_client.get("/users/")
    assert response.status_code == 200

def test_manager_can_access_users(manager_client):
    response = manager_client.get("/users")
    assert response.status_code == 200

def test_user_can_access_users(user_client):
    response = user_client.get("/users/")
    assert response.status_code == 200

def test_readonly_can_access_users(readonly_client):
    response = readonly_client.get("/users/")
    assert response.status_code == 200

# TEST RESTRICTED ACCESS
def test_readonly_cannot_delete_user(readonly_client):

    response = readonly_client.delete("/users/3")

    assert response.status_code == 403

def test_admin_can_delete_user(admin_client):

    response = admin_client.delete("/users/999")

    assert response.status_code == 404