from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..data import crud, models, schemas
from ..utils.logs import getLogger
from . import dependencies as dep

router = APIRouter(
    prefix="/project",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

log = getLogger()


@router.post(
    "/", response_model=schemas.ProjectInfo, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(dep.get_db),
    current_user: models.User = Depends(dep.get_current_user),
):
    return crud.create_project(db, project, current_user)


@router.get("/", response_model=list[schemas.ProjectInfo])
async def read_projects(
    db: Session = Depends(dep.get_db), user: models.User = Depends(dep.get_current_user)
):
    accessible_projects = crud.get_accessible_projects(db, user.id)
    if not accessible_projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return list(map(render_project_info, accessible_projects))


def render_project(db_project: models.Project) -> schemas.Project:
    project_documents = list(db_project.documents) if db_project.documents else []

    return schemas.Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
        documents=project_documents,
    )


# TODO: search for a better solution of
#   transforming SQLAlchemy model into Pydantic schema
def render_project_info(db_project: models.Project) -> schemas.ProjectInfo:
    return schemas.ProjectInfo(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
    )


@router.get(
    "/{project_id}",
    response_model=schemas.Project,
    dependencies=[Depends(dep.is_project_participant)],
)
async def read_project(
    project_id: int,
    db_project=Depends(dep.get_project_by_id),
):
    return render_project(db_project)


# making an alias depending on the user's preferences
@router.patch(
    "/{project_id}",
    response_model=schemas.Project,
    dependencies=[Depends(dep.is_project_participant)],
)
@router.put(
    "/{project_id}",
    response_model=schemas.Project,
    dependencies=[Depends(dep.is_project_participant)],
)
async def update_project(
    project: schemas.ProjectUpdate,
    project_id: int,
    db: Session = Depends(dep.get_db),
    db_project=Depends(dep.get_project_by_id),
):
    updated = crud.update_project(db, db_project, project)
    if updated is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update the project",
        )

    return render_project(updated)


@router.post("/{project_id}/invite", dependencies=[Depends(dep.is_project_owner)])
async def grant_project_access(
    login: Annotated[
        str, Query()
    ],  # used to define the value for dependency dep.get_user_by_login
    db: Session = Depends(dep.get_db),
    user: models.User = Depends(dep.get_user_by_login),
    project: models.Project = Depends(dep.get_project_by_id),
):
    project = crud.grant_access_to_user(db, project, user)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission is already granted",
        )
    return {"message": f"Grated user '{user.login}' access to project '{project.name}'"}
