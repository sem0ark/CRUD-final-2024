import os

from fastapi import UploadFile
from fastapi.testclient import TestClient

import src.document.models
import src.project.models
import src.user.models

image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.jpg")


def test_get_logo_unauthorized(
    client: TestClient,
    logo_file: str,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get(
        f"/project/{project_data.id}/logo", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_get_logo_authorized(
    client: TestClient,
    logo_file: str,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        res = client.get(f"/project/{project_data.id}/logo", headers=user_header)
        assert res.status_code == 200


def test_get_logo_nonexistent_unauthorized(
    client: TestClient,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get(
        f"/project/{project_data.id}/logo", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_get_logo_nonexistent_authorized(
    client: TestClient,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        res = client.get(f"/project/{project_data.id}/logo", headers=user_header)
        assert res.status_code == 404


def test_update_logo(
    client: TestClient,
    logo_file: str,
    good_upload_logo: UploadFile,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                good_upload_logo.filename,
                good_upload_logo.file,
                "image/jpeg",
            )
        }

        res = client.put(
            f"/project/{project_data.id}/logo",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 201


def test_update_logo_failed(
    client: TestClient,
    logo_file: str,
    bad_upload_file: UploadFile,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                bad_upload_file.filename,
                bad_upload_file.file,
                "text/plain",
            )
        }

        res = client.put(
            f"/project/{project_data.id}/logo",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 422


def test_update_logo_unauthorized(
    client: TestClient,
    logo_file: str,
    good_upload_logo: UploadFile,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    data = {
        "file": (
            good_upload_logo.filename,
            good_upload_logo.file,
            "image/jpeg",
        )
    }

    res = client.put(
        f"/project/{project_data.id}/logo",
        headers=unauthorized_user_token_header,
        files=data,
    )

    assert res.status_code == 401


def test_create_logo(
    client: TestClient,
    good_upload_logo: UploadFile,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                good_upload_logo.filename,
                good_upload_logo.file,
                "image/jpeg",
            )
        }

        res = client.put(
            f"/project/{project_data.id}/logo",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 201


def test_create_logo_failed(
    client: TestClient,
    bad_upload_file: UploadFile,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                bad_upload_file.filename,
                bad_upload_file.file,
                "text/plain",
            )
        }

        res = client.put(
            f"/project/{project_data.id}/logo",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 422


def test_create_logo_unauthorized(
    client: TestClient,
    good_upload_logo: UploadFile,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    data = {
        "file": (
            good_upload_logo.filename,
            good_upload_logo.file,
            "image/jpeg",
        )
    }

    res = client.put(
        f"/project/{project_data.id}/logo",
        headers=unauthorized_user_token_header,
        files=data,
    )

    assert res.status_code == 401


def test_delete_logo_unauthorized(
    client: TestClient,
    logo_file: str,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_delete_logo_nonexistent_unauthorized(
    client: TestClient,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_delete_logo_participant(
    client: TestClient,
    logo_file: str,
    project_data: src.project.models.Project,
    participant_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=participant_user_token_header
    )
    assert res.status_code == 401


def test_delete_logo_nonexistent_participant(
    client: TestClient,
    project_data: src.project.models.Project,
    participant_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=participant_user_token_header
    )
    assert res.status_code == 401


def test_delete_logo_nonexistent(
    client: TestClient,
    project_data: src.project.models.Project,
    main_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=main_user_token_header
    )
    assert res.status_code == 204


def test_delete_logo_failed(
    client: TestClient,
    logo_file: str,
    project_data: src.project.models.Project,
    main_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/project/{project_data.id}/logo", headers=main_user_token_header
    )
    assert res.status_code == 204
