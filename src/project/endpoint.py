from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.dto import converters
from src.permission.dao import grant_access_to_user
from src.permission.dependencies import is_project_owner, is_project_participant
from src.project.dao import (
    create_project as create_project_dao,
)
from src.project.dao import (
    delete_project as delete_project_dao,
)
from src.project.dao import (
    get_accessible_projects,
)
from src.project.dao import (
    update_project as update_project_dao,
)
from src.project.dependencies import get_project_by_id
from src.project.dto import (
    Project as ProjectSchema,
)
from src.project.dto import (
    ProjectCreate,
    ProjectInfo,
    ProjectUpdate,
)
from src.project.model import Project as ProjectModel
from src.shared.database import get_db
from src.user.dao import get_user_by_login
from src.user.dependencies import get_current_user
from src.user.models import User as UserModel

router = APIRouter(
    prefix="/project",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProjectInfo, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return create_project_dao(db, project, current_user)


@router.get("/", response_model=list[ProjectInfo])
async def read_projects(
    db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)
):
    accessible_projects = get_accessible_projects(db, user.id)
    if not accessible_projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return list(map(converters.project_info, accessible_projects))


@router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    dependencies=[Depends(is_project_participant)],
)
async def read_project(
    project_id: int,
    db_project=Depends(get_project_by_id),
):
    return converters.project(db_project)


# making an alias depending on the user's preferences
# @router.patch(
#     "/{project_id}",
#     response_model=schemas.Project,
#     dependencies=[Depends(is_project_participant)],
# )
@router.put(
    "/{project_id}",
    response_model=ProjectSchema,
    dependencies=[Depends(is_project_participant)],
)
async def update_project(
    project: ProjectUpdate,
    project_id: int,
    db: Session = Depends(get_db),
    db_project=Depends(get_project_by_id),
):
    updated = update_project_dao(db, db_project, project)
    if updated is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update the project",
        )

    return converters.project(updated)


@router.delete(
    "/{project_id}",
    dependencies=[Depends(is_project_owner), Depends(get_project_by_id)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    delete_project_dao(db, project_id)


@router.post(
    "/{project_id}/invite",
    dependencies=[Depends(is_project_owner)],
    status_code=status.HTTP_201_CREATED,
)
async def grant_project_access(
    login: Annotated[
        str, Query()
    ],  # used to define the value for dependency get_user_by_login
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_user_by_login),
    project: ProjectModel = Depends(get_project_by_id),
):
    project = grant_access_to_user(db, project, user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is already granted",
        )
    return {"message": f"Grated user '{user.login}' access to project '{project.name}'"}
