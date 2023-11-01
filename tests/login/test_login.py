def test_login_ok_and_get_private_endpoint_with_token(testclient_with_2_users):
    response = testclient_with_2_users.post(
        "/auth/login",
        data={"username": "alice", "password": "alice"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert len(token) > 0
    assert response.json()["token_type"].lower() == "bearer"

    response = testclient_with_2_users.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == "alice"
    assert user["email"] == "alice@alice.com"
    assert "password" not in user
    assert "token" not in user


def test_login_error_1(testclient_with_2_users):
    response = testclient_with_2_users.post(
        "/auth/login",
        data={"username": "alice", "password": "bob"}
    )
    assert response.status_code == 401


def test_login_error_2(testclient_with_2_users):
    response = testclient_with_2_users.post(
        "/auth/login",
        data={"username": "bob", "password": "alice"}
    )
    assert response.status_code == 401


def test_login_without_data(testclient_with_2_users):
    response = testclient_with_2_users.post("/auth/login")
    assert response.status_code == 422


def test_login_with_empty_data(testclient_with_2_users):
    response = testclient_with_2_users.post("/auth/login", data={})
    assert response.status_code == 422


def test_login_with_other_data(testclient_with_2_users):
    response = testclient_with_2_users.post(
        "/auth/login",
        data={"user": "alice", "pwd": "alice"}
    )
    assert response.status_code == 422
