from fastapi.testclient import TestClient

import src.project.models


def test_projects_accessible_to_owner(
    client: TestClient,
    main_user_token_header: dict[str, str],
    project_data: list[src.project.models.Project],
):
    res = client.get("/project/", headers=main_user_token_header)

    assert res.json() == [
        {"name": p.name, "description": p.description, "id": p.id} for p in project_data
    ]


def test_projects_accessible_to_participant(
    client: TestClient,
    participant_user_token_header: dict[str, str],
    project_data: list[src.project.models.Project],
):
    res = client.get("/project/", headers=participant_user_token_header)

    assert res.json() == [
        {"name": p.name, "description": p.description, "id": p.id} for p in project_data
    ]


def test_projects_accessible_to_unauthorized(
    client: TestClient,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get("/project/", headers=unauthorized_user_token_header)

    assert res.json() == []


def test_project_info_owner(
    client: TestClient,
    main_user_token_header: dict[str, str],
    project_data: list[src.project.models.Project],
):
    for p in project_data:
        res = client.get(f"/project/{p.id}", headers=main_user_token_header)

        assert res.json() == {
            "created_at": p.created_at.isoformat(sep="T"),
            "updated_at": p.updated_at.isoformat(sep="T"),
            "name": p.name,
            "description": p.description,
            "id": p.id,
        }


def test_project_info_participant(
    client: TestClient,
    participant_user_token_header: dict[str, str],
    project_data: list[src.project.models.Project],
):
    for p in project_data:
        res = client.get(f"/project/{p.id}", headers=participant_user_token_header)

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
    project_data: list[src.project.models.Project],
):
    for p in project_data:
        res = client.get(f"/project/{p.id}", headers=unauthorized_user_token_header)
        assert res.status_code == 401
