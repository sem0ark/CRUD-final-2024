from uuid import uuid4

from sqlalchemy.orm import Session

import src.document.models as document_models
import src.project.dao as project_dao
import src.project.models as project_models


def get_document_by_id(
    db: Session, document_id: str
) -> document_models.Document | None:
    return db.query(document_models.Document).get(document_id)


def create_document(
    db: Session, project: project_models.Project, filename: str | None
) -> document_models.Document:
    db_document = document_models.Document(
        id=str(uuid4()), name=filename, project=project
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(
    db: Session, db_document: document_models.Document, filename: str
) -> document_models.Document:
    db_document.name = filename
    db.commit()
    db.refresh(db_document)
    return db_document


def get_project_by_document_id(
    db: Session, document_id: str
) -> project_models.Project | None:
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    return db_document.project


def get_available_documents(
    db: Session,
    project_id: int,
    limit: int = 10,
    offset: int = 0,
) -> list[document_models.Document] | None:
    db_project = project_dao.get_project(db, project_id)
    if not db_project:
        return None
    return list(db_project.documents)[offset : offset + limit]
