from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse

import src.auth.dependencies as auth_deps
import src.document.dao as document_dao
import src.document.dependencies as document_deps
import src.document.dto as document_dto
import src.document.models as document_models
import src.project.dependencies as project_deps
import src.project.models as project_models
from src.services import file_service
from src.shared.database import get_db
from src.shared.logs import log

router = APIRouter(
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/project/{project_id}/documents",
    dependencies=[Depends(auth_deps.is_project_participant)],
    response_model=list[document_dto.Document],
)
def get_available_documents(
    project_id: int,
    project: project_models.Project = Depends(project_deps.get_project_by_id),
):
    if not project.documents:
        return []

    log.debug(f"Received available documents {project.documents}")

    return list(map(document_dto.document, project.documents))


@router.post(
    "/project/{project_id}/documents",
    dependencies=[
        Depends(auth_deps.is_project_participant),
        Depends(document_deps.is_document),
    ],
    response_model=document_dto.Document,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile,
    db=Depends(get_db),
    project=Depends(project_deps.get_project_by_id),
):
    # filename can be None, so replace with default value of document's ID
    db_document = document_dao.create_document(db, project, file.filename)
    file_service.save_document(file, db_document.id)

    return db_document


@router.get(
    "/document/{document_id}",
    dependencies=[
        Depends(document_deps.get_document_by_id),
        Depends(project_deps.get_project_id_by_document_id),
        Depends(auth_deps.is_project_participant),
    ],
)
def download_document(document_id: str):
    return FileResponse(file_service.get_document(document_id))


@router.put(
    "/document/{document_id}",
    dependencies=[
        Depends(auth_deps.is_project_participant),
        Depends(document_deps.is_document),
    ],
)
def reupload_document(
    document_id: str,
    file: UploadFile,
    document: document_models.Document = Depends(document_deps.get_document_by_id),
    db=Depends(get_db),
):
    file_name = file.filename
    if not file_name:
        file_name = document.name

    db_document = document_dao.update_document(db, document, file_name)
    file_service.delete_document_by_id(db_document.id)
    file_service.save_document(file, db_document.id)

    return db_document


@router.delete(
    "/document/{document_id}",
    dependencies=[Depends(auth_deps.is_project_owner)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(document_id: str, db=Depends(get_db)):
    file_service.delete_document_by_id(document_id)