from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

import src.auth.dependencies as auth_deps
import src.document.dependencies as document_deps
import src.logo.dao as logo_dao
import src.project.dependencies as project_deps
import src.project.models as project_models
from src.services import file_service
from src.shared.database import Session, get_db
from src.shared.logs import log

router = APIRouter(
    tags=["logos"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/project/{project_id}/logo",
    dependencies=[Depends(auth_deps.is_project_participant)],
)
def download_project_logo(
    project: project_models.Project = Depends(project_deps.get_project_by_id),
):
    if not project.logo_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project does not have a logo"
        )
    return FileResponse(file_service.get_document(project.logo_id), filename="logo.jpg")


@router.put(
    "/project/{project_id}/logo",
    dependencies=[
        Depends(auth_deps.is_project_participant),
        Depends(document_deps.is_logo),
    ],
    status_code=status.HTTP_201_CREATED,
)
def upload_project_logo(
    file: UploadFile,
    project: project_models.Project = Depends(project_deps.get_project_by_id),
    db: Session = Depends(get_db),
) -> None:
    if project.logo_id is not None:  # if exists, remove previous image
        try:
            file_service.delete_document_by_id(project.logo_id)
        except FileNotFoundError as e:
            log.error(f"Failed to delete file {project.logo_id}")
            log.error(e)

    try:
        file_id = logo_dao.create_logo(db, project)
        file_service.save_image(file.file, file_id)
    except Exception as e:
        logo_dao.delete_logo(db, project)
        log.error("Failed to update logo")
        log.error(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update logo",
        ) from e


@router.delete(
    "/project/{project_id}/logo",
    dependencies=[Depends(auth_deps.is_project_owner)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_logo(
    project: project_models.Project = Depends(project_deps.get_project_by_id),
    db: Session = Depends(get_db),
) -> None:
    if project.logo_id is None:
        return

    try:
        file_service.delete_document_by_id(project.logo_id)
        logo_dao.delete_logo(db, project)
    except FileNotFoundError as e:
        log.error(f"Failed to delete file {project.logo_id}")
        log.error(e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete logo",
        ) from e
