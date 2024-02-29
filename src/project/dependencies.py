from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

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
