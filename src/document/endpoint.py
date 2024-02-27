from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse

from src.document.dao import create_document, update_document
from src.document.dependencies import get_document_by_id, is_document
from src.document.dto import Document as DocumentScheme
from src.document.model import Document as DocumentModel
from src.dto import converters
from src.permission.dependencies import is_project_owner, is_project_participant
from src.project.dependencies import get_project_by_id, get_project_id_by_document_id
from src.project.model import Project as ProjectModel
from src.services import file_service
from src.shared.database import get_db
from src.shared.logs import log

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/project/{project_id}/documents",
    dependencies=[Depends(is_project_participant)],
    response_model=list[DocumentScheme],
)
def get_available_documents(
    project_id: int, project: ProjectModel = Depends(get_project_by_id)
):
    if not project.documents:
        return []

    log.debug(f"Received available documents {project.documents}")

    return list(map(converters.document, project.documents))


@router.post(
    "/project/{project_id}/documents",
    dependencies=[Depends(is_project_participant), Depends(is_document)],
    response_model=DocumentScheme,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile, db=Depends(get_db), project=Depends(get_project_by_id)
):
    # filename can be None, so replace with default value of document's ID
    db_document = create_document(db, project, file.filename)
    file_service.save_document(file, db_document.id)

    return db_document


@router.get(
    "/document/{document_id}",
    dependencies=[
        Depends(get_document_by_id),
        Depends(get_project_id_by_document_id),
        Depends(is_project_participant),
    ],
)
def download_document(document_id: str):
    return FileResponse(file_service.get_document(document_id))


@router.put(
    "/document/{document_id}",
    dependencies=[Depends(is_project_participant), Depends(is_document)],
)
def reupload_document(
    document_id: str,
    file: UploadFile,
    document: DocumentModel = Depends(get_document_by_id),
    db=Depends(get_db),
):
    file_name = file.filename
    if not file_name:
        file_name = document.name

    db_document = update_document(db, document, file_name)
    file_service.delete_document_by_id(db_document.id)
    file_service.save_document(file, db_document.id)

    return db_document


@router.delete(
    "/document/{document_id}",
    dependencies=[Depends(is_project_owner)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(document_id: str, db=Depends(get_db)):
    file_service.delete_document_by_id(document_id)
