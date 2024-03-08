from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.responses import FileResponse

import src.auth.dependencies as auth_deps
import src.document.dao as document_dao
import src.document.dependencies as document_deps
import src.document.dto as document_dto
import src.document.models as document_models
import src.project.dependencies as project_deps
import src.user.dependencies as user_deps
import src.user.models as user_models
from src.services import file_service
from src.shared.database import Session, get_db

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
    db: Session = Depends(get_db),
    limit: int = Query(default=10),
    offset: int = Query(default=0),
):
    documents = document_dao.get_available_documents(db, project_id, limit, offset)
    if documents is None:
        return []
    return list(map(document_dto.document, documents))


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
    file_service.documents.save_file(file.file, db_document.id)

    return db_document


@router.get(
    "/document/{document_id}",
)
def download_document(
    document_id: str,
    document: document_models.Document = Depends(document_deps.get_document_by_id),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
):
    auth_deps.is_project_participant(
        auth_deps.project_role(document.project_id, db, current_user)
    )
    return FileResponse(
        file_service.documents.download_file(document.id), filename=document.name
    )


@router.put(
    "/document/{document_id}",
    dependencies=[
        Depends(document_deps.is_document),
    ],
)
def reupload_document(
    document_id: str,
    file: UploadFile,
    document: document_models.Document = Depends(document_deps.get_document_by_id),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
):
    auth_deps.is_project_participant(
        auth_deps.project_role(document.project_id, db, current_user)
    )

    file_name = file.filename
    if not file_name:
        file_name = document.name

    db_document = document_dao.update_document(db, document, file_name)
    file_service.documents.save_file(file.file, db_document.id)

    return db_document


@router.delete(
    "/document/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: str,
    document: document_models.Document = Depends(document_deps.get_document_by_id),
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
):
    auth_deps.is_project_owner(
        auth_deps.project_role(document.project_id, db, current_user)
    )
    document_dao.delete_document(db, document_id)
    file_service.documents.delete_file_by_id(document_id)
