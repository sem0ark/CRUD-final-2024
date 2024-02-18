from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data import crud, schemas

from .dependencies import get_db

router = APIRouter(
    prefix="/project",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.ProjectInfo)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)


@router.get("/{project_id}", response_model=schemas.ProjectInfo)
async def read_projects(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project(db, project_id)
