from fastapi.testclient import TestClient

import src.project.models
import src.user.models


def test_projects_accessible_to_authorized(
    client: TestClient,
    authorized_users_token_header: list[dict[str, str]],
    project_data_list: list[src.project.models.Project],
):
    for user_header in authorized_users_token_header:
        res = client.get("/project/", headers=user_header)

        assert res.json() == [
            {"name": p.name, "description": p.description, "id": p.id}
            for p in project_data_list
        ]


def test_projects_accessible_to_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get("/project/", headers=unauthorized_user_token_header)

    assert res.json() == []


def test_project_info_authorized(
    client: TestClient,
    authorized_users_token_header: list[dict[str, str]],
    project_data_list: list[src.project.models.Project],
):
    for user_header in authorized_users_token_header:
        for p in project_data_list:
            res = client.get(f"/project/{p.id}", headers=user_header)

            assert res.json() == {
                "created_at": p.created_at.isoformat(sep="T"),
                "updated_at": p.updated_at.isoformat(sep="T"),
                "name": p.name,
                "description": p.description,
                "id": p.id,
            }


def test_project_info_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
    project_data_list: list[src.project.models.Project],
):
    for p in project_data_list:
        res = client.get(f"/project/{p.id}", headers=unauthorized_user_token_header)
        assert res.status_code == 401


def test_project_info_not_found(
    client: TestClient,
    all_users_token_header: list[dict[str, str]],
):
    for user_header in all_users_token_header:
        res = client.get("/project/1237987", headers=user_header)
        assert res.status_code == 401


def test_create_project_owner(
    client: TestClient,
    all_users_token_header: list[dict[str, str]],
):
    for user_header in all_users_token_header:
        data = {"name": "project name"}
        res = client.post("/project/", json=data, headers=user_header)

        assert res.json()["name"] == data["name"]
        assert res.json()["description"] == ""


def test_update_project_owner(
    client: TestClient,
    main_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    data = {"name": "new project name", "description": "new project description"}
    res = client.put(
        f"/project/{project_data.id}", json=data, headers=main_user_token_header
    )

    assert res.json()["name"] == data["name"]
    assert res.json()["description"] == data["description"]
    assert res.json()["created_at"] == project_data.created_at.isoformat(sep="T")
    assert res.json()["created_at"] != res.json()["updated_at"]


def test_update_project_participant(
    client: TestClient,
    participant_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    data = {"name": "new project name", "description": "new project description"}
    res = client.put(
        f"/project/{project_data.id}", json=data, headers=participant_user_token_header
    )

    assert res.json()["name"] == data["name"]
    assert res.json()["description"] == data["description"]
    assert res.json()["created_at"] == project_data.created_at.isoformat(sep="T")
    assert res.json()["created_at"] != res.json()["updated_at"]


def test_update_project_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    data = {"name": "new project name", "description": "new project description"}
    res = client.put(
        f"/project/{project_data.id}", json=data, headers=unauthorized_user_token_header
    )

    assert res.status_code == 401


def test_delete_project_owner(
    client: TestClient,
    main_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    res = client.delete(f"/project/{project_data.id}", headers=main_user_token_header)

    assert res.status_code == 204


def test_delete_project_participant(
    client: TestClient,
    participant_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    res = client.delete(
        f"/project/{project_data.id}", headers=participant_user_token_header
    )

    assert res.status_code == 401


def test_delete_project_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
    project_data: src.project.models.Project,
):
    res = client.delete(
        f"/project/{project_data.id}", headers=unauthorized_user_token_header
    )

    assert res.status_code == 401


def test_project_invite_authorized(
    client: TestClient,
    main_user_token_header: dict[str, str],
    unauthorized_user: src.user.models.User,
    project_data: src.project.models.Project,
):
    res = client.post(
        f"/project/{project_data.id}/invite",
        headers=main_user_token_header,
        params={
            "login": unauthorized_user.login,
        },
    )

    assert res.status_code == 201


def test_project_invite_participant(
    client: TestClient,
    participant_user_token_header: dict[str, str],
    unauthorized_user: src.user.models.User,
    project_data: src.project.models.Project,
):
    res = client.post(
        f"/project/{project_data.id}/invite",
        headers=participant_user_token_header,
        params={
            "login": unauthorized_user.login,
        },
    )

    assert res.status_code == 401


def test_project_invite_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
    unauthorized_user: src.user.models.User,
    project_data: src.project.models.Project,
):
    res = client.post(
        f"/project/{project_data.id}/invite",
        headers=unauthorized_user_token_header,
        params={
            "login": unauthorized_user.login,
        },
    )

    assert res.status_code == 401
