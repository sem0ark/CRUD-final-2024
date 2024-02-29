from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.document.dao as document_dao
import src.project.dao as project_dao
import src.project.models as project_models
from src.shared.database import get_db


def get_project_by_id(
    project_id: int, db: Session = Depends(get_db)
) -> project_models.Project:
    db_project = project_dao.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_project


def get_project_id_by_document_id(document_id: str, db=Depends(get_db)):
    project_id = document_dao.get_document_by_id(db, document_id)
    if not project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project_id
