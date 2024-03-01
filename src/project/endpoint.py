from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import src.auth.dao as auth_dao
import src.auth.dependencies as auth_deps
import src.project.dao as project_dao
import src.project.dependencies as project_deps
import src.project.dto as project_dto
import src.project.models as project_models
import src.user.dependencies as user_deps
import src.user.models as user_models
from src.shared.database import get_db

router = APIRouter(
    prefix="/project",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=project_dto.ProjectInfo, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project: project_dto.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
):
    return project_dao.create_project(db, project, current_user)


@router.get("/", response_model=list[project_dto.ProjectInfo])
async def get_accessible_projects(
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_deps.get_current_user),
    limit: int = Query(default=10),
    offset: int = Query(default=0),
):
    accessible_projects = project_dao.get_accessible_projects(
        db, user.id, limit, offset
    )
    if accessible_projects is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return list(map(project_dto.project_info, accessible_projects))


@router.get(
    "/{project_id}",
    response_model=project_dto.Project,
    dependencies=[Depends(auth_deps.is_project_participant)],
)
async def read_project(
    project_id: int,
    db_project=Depends(project_deps.get_project_by_id),
):
    return project_dto.project(db_project)


@router.put(
    "/{project_id}",
    response_model=project_dto.Project,
    dependencies=[Depends(auth_deps.is_project_participant)],
)
async def update_project(
    project: project_dto.ProjectUpdate,
    project_id: int,
    db: Session = Depends(get_db),
    db_project=Depends(project_deps.get_project_by_id),
):
    updated = project_dao.update_project(db, db_project, project)
    if updated is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update the project",
        )

    return project_dto.project(updated)


@router.delete(
    "/{project_id}",
    dependencies=[
        Depends(auth_deps.is_project_owner),
        Depends(project_deps.get_project_by_id),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    project_dao.delete_project(db, project_id)


@router.post(
    "/{project_id}/invite",
    dependencies=[Depends(auth_deps.is_project_owner)],
    status_code=status.HTTP_201_CREATED,
)
async def grant_project_access(
    login: Annotated[
        str, Query()
    ],  # used to define the value for dependency get_user_by_login
    db: Session = Depends(get_db),
    user: user_models.User = Depends(user_deps.get_user_by_login),
    project: project_models.Project = Depends(project_deps.get_project_by_id),
):
    project = auth_dao.grant_access_to_user(db, project, user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Permission is already granted",
        )
    return {"message": f"Grated user '{user.login}' access to project '{project.name}'"}
