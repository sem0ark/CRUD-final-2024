from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..data import crud, models, schemas
from .dependencies import get_current_user, get_db, is_participant

router = APIRouter(
    prefix="/project",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.ProjectInfo)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_project(db, project, current_user)


@router.get("/", response_model=schemas.ProjectListing)
async def read_projects(
    db: Session = Depends(get_db), user: models.User = Depends(get_current_user)
):
    accessible_porojects = crud.get_accessible_projects(db, user.id)
    return {"projects": accessible_porojects}


@router.get(
    "/{project_id}",
    response_model=schemas.ProjectInfo,
    dependencies=[Depends(is_participant)],
)
async def read_project(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project(db, project_id)
