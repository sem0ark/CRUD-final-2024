from fastapi.testclient import TestClient

import src.project.models
import src.user.models


def test_user_create_cannot_make_same_login(
    client: TestClient,
    main_user: src.user.models.User,
):
    data = {"login": main_user.login, "password": "123456"}
    res = client.post("/auth", json=data)
    assert res.status_code == 403


def test_user_create(
    client: TestClient,
):
    data = {"login": "some user login", "password": "123456"}
    res = client.post("/auth", json=data)
    assert res.status_code == 201
    assert res.json() == {
        "id": res.json()["id"],
        "login": data["login"],
    }


def test_user_login(
    client: TestClient,
    all_users: src.user.models.User,
):
    for user in all_users:
        data = {"login": user.login, "password": "C0mplex P455w0rd"}
        res = client.post("/login", json=data)

        assert res.status_code == 200
        assert res.json() == {
            "access_token": res.json()["access_token"],
            "token_type": "bearer",
        }
