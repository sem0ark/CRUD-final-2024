from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.project.dao import (
    get_project,
)
from src.project.dao import (
    get_project_id_by_document_id as get_by_document_id,
)
from src.project.model import Project
from src.shared.database import get_db


def get_project_by_id(project_id: int, db: Session = Depends(get_db)) -> Project:
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_project


def get_project_id_by_document_id(document_id: str, db=Depends(get_db)):
    project_id = get_by_document_id(db, document_id)
    if not project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project_id
