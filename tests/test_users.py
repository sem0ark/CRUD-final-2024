import pytest
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


@pytest.mark.parametrize(
    "login, password",
    [
        ("some user login", "123456"),
        (" some 123 Lo0in ", "123456"),
        ("some", "123456"),
    ],
)
def test_user_create(
    login: str,
    password: str,
    client: TestClient,
):
    data = {"login": login, "password": password}
    res = client.post("/auth", json=data)
    assert res.status_code == 201
    assert res.json() == {
        "id": res.json()["id"],
        "login": login,
    }


@pytest.mark.parametrize(
    "login, password",
    [
        ("some user login", ""),
        ("something", "12s"),
        ("some", "asd"),
    ],
)
def test_user_create_fails(
    login: str,
    password: str,
    client: TestClient,
):
    data = {"login": login, "password": password}
    res = client.post("/auth", json=data)
    assert res.status_code == 422


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


@pytest.mark.parametrize(
    "login, password",
    [
        ("some", "asdqweqwe"),
        ("some", "asd12846987"),
        ("main_test_user", "asd12846987"),
    ],
)
def test_user_login_fails(
    login: str,
    password: str,
    client: TestClient,
):
    data = {"login": login, "password": password}
    res = client.post("/login", json=data)

    assert res.status_code == 403
