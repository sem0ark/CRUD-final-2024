from fastapi import UploadFile
from fastapi.testclient import TestClient

import src.document.models
import src.project.models
import src.user.models


def test_read_documents_authorized(
    client: TestClient,
    document_data: src.document.models.Document,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        res = client.get(f"/project/{project_data.id}/documents", headers=user_header)
        assert res.status_code == 200
        assert res.json() == [
            {
                "created_at": document_data.created_at.isoformat(sep="T"),
                "updated_at": document_data.updated_at.isoformat(sep="T"),
                "name": document_data.name,
                "id": document_data.id,
            }
        ]


def test_read_documents_unauthorized(
    client: TestClient,
    document_data: src.document.models.Document,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get(
        f"/project/{project_data.id}/documents", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


# https://github.com/tiangolo/fastapi/issues/1536#issuecomment-640781718
# https://stackoverflow.com/questions/60783222/how-to-test-a-fastapi-api-endpoint-that-consumes-images
def test_create_document(
    client: TestClient,
    good_upload_file: UploadFile,
    project_data: src.project.models.Project,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                good_upload_file.filename,
                good_upload_file.file,
                good_upload_file.content_type,
            )
        }

        res = client.post(
            f"/project/{project_data.id}/documents",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 201

        assert res.json() == {
            "created_at": res.json()["created_at"],
            "updated_at": res.json()["updated_at"],
            "name": good_upload_file.filename,
            "id": res.json()["id"],
        }

        assert res.json()["created_at"] == res.json()["updated_at"]


def test_create_document_failed(
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

        res = client.post(
            f"/project/{project_data.id}/documents",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 422


def test_create_document_unauthorized(
    client: TestClient,
    good_upload_file: UploadFile,
    project_data: src.project.models.Project,
    unauthorized_user_token_header: dict[str, str],
):
    data = {
        "file": (
            good_upload_file.filename,
            good_upload_file.file,
            "application/pdf",
        )
    }

    res = client.post(
        f"/project/{project_data.id}/documents",
        headers=unauthorized_user_token_header,
        files=data,
    )

    assert res.status_code == 401


# https://github.com/tiangolo/fastapi/issues/1536#issuecomment-640781718
# https://stackoverflow.com/questions/60783222/how-to-test-a-fastapi-api-endpoint-that-consumes-images
def test_update_document(
    client: TestClient,
    good_upload_file_2: UploadFile,
    authorized_users_token_header: list[dict[str, str]],
    document_data: src.document.models.Document,
):
    for user_header in authorized_users_token_header:
        data = {
            "file": (
                good_upload_file_2.filename,
                good_upload_file_2.file,
                "application/pdf",
            )
        }

        res = client.put(
            f"/document/{document_data.id}",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 200

        assert res.json() == {
            "created_at": document_data.created_at.isoformat(sep="T"),
            "updated_at": res.json()["updated_at"],
            "name": good_upload_file_2.filename,
            "project_id": document_data.project_id,
            "id": res.json()["id"],
        }

        assert res.json()["updated_at"] != document_data.created_at.isoformat(sep="T")
        assert res.json()["updated_at"] != document_data.updated_at.isoformat(sep="T")


def test_update_document_failed(
    client: TestClient,
    bad_upload_file: UploadFile,
    authorized_users_token_header: list[dict[str, str]],
    document_data: src.document.models.Document,
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
            f"/document/{document_data.id}",
            headers=user_header,
            files=data,
        )

        assert res.status_code == 422


def test_update_document_unauthorized(
    client: TestClient,
    good_upload_file_2: UploadFile,
    unauthorized_user_token_header: dict[str, str],
    document_data: src.document.models.Document,
):
    data = {
        "file": (
            good_upload_file_2.filename,
            good_upload_file_2.file,
            "application/pdf",
        )
    }

    res = client.put(
        f"/document/{document_data.id}",
        headers=unauthorized_user_token_header,
        files=data,
    )

    assert res.status_code == 401


def test_get_document_unauthorized(
    client: TestClient,
    document_data: src.document.models.Document,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.get(
        f"/document/{document_data.id}", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_get_document_authorized(
    client: TestClient,
    document_data: src.document.models.Document,
    authorized_users_token_header: list[dict[str, str]],
):
    for user_header in authorized_users_token_header:
        res = client.get(f"/document/{document_data.id}", headers=user_header)
        assert res.status_code == 200


def test_delete_document_unauthorized(
    client: TestClient,
    document_data: src.document.models.Document,
    unauthorized_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/document/{document_data.id}", headers=unauthorized_user_token_header
    )
    assert res.status_code == 401


def test_delete_document_participant(
    client: TestClient,
    document_data: src.document.models.Document,
    participant_user_token_header: dict[str, str],
):
    res = client.delete(
        f"/document/{document_data.id}", headers=participant_user_token_header
    )
    assert res.status_code == 401


def test_delete_document_failed(
    client: TestClient,
    document_data: src.document.models.Document,
    main_user_token_header: dict[str, str],
):
    res = client.delete("/document/1237989127398", headers=main_user_token_header)
    assert res.status_code == 404


def test_delete_document_owner(
    client: TestClient,
    document_data: src.document.models.Document,
    main_user_token_header: dict[str, str],
):
    res = client.delete(f"/document/{document_data.id}", headers=main_user_token_header)
    assert res.status_code == 204
