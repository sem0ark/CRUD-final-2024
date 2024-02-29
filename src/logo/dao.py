from uuid import uuid4

from sqlalchemy.orm import Session

import src.project.models as project_models


def create_logo(db: Session, project: project_models.Project) -> str:
    filename = str(uuid4())
    project.logo_id = filename
    db.commit()
    db.refresh(project)
    return filename


def delete_logo(db: Session, project: project_models.Project) -> None:
    project.logo_id = None
    db.commit()
    db.refresh(project)
