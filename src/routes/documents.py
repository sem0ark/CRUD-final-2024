from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse

from ..data import crud, models, schemas
from ..services import file_service
from ..utils import renders
from ..utils.logs import log
from . import dependencies as dep

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/project/{project_id}/documents",
    dependencies=[Depends(dep.is_project_participant)],
    response_model=list[schemas.Document],
)
def get_available_documents(
    project_id: int, project: models.Project = Depends(dep.get_project_by_id)
):
    if not project.documents:
        return []

    log.debug(f"Received available documents {project.documents}")

    return list(map(renders.render_document, project.documents))


@router.post(
    "/project/{project_id}/documents",
    dependencies=[Depends(dep.is_project_participant), Depends(dep.is_document)],
    response_model=schemas.Document,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile, db=Depends(dep.get_db), project=Depends(dep.get_project_by_id)
):
    # filename can be None, so replace with default value of document's ID
    db_document = crud.create_document(db, project, file.filename)
    file_service.save_document(file, db_document.id)

    return db_document


@router.get(
    "/document/{document_id}",
    dependencies=[
        Depends(dep.get_document_by_id),
        Depends(dep.get_project_id_by_document_id),
        Depends(dep.is_project_participant),
    ],
)
def download_document(document_id: str):
    return FileResponse(file_service.get_document(document_id))


@router.put(
    "/document/{document_id}",
    dependencies=[Depends(dep.is_project_participant), Depends(dep.is_document)],
)
def reupload_document(
    document_id: str,
    file: UploadFile,
    document: models.Document = Depends(dep.get_document_by_id),
    db=Depends(dep.get_db),
):
    file_name = file.filename
    if not file_name:
        file_name = document.name

    db_document = crud.update_document(db, document, file_name)
    file_service.delete_document_by_id(db_document.id)
    file_service.save_document(file, db_document.id)

    return db_document


@router.delete(
    "/document/{document_id}",
    dependencies=[Depends(dep.is_project_owner)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(document_id: str, db=Depends(dep.get_db)):
    file_service.delete_document_by_id(document_id)
