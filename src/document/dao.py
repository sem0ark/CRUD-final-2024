from uuid import uuid4

from sqlalchemy.orm import Session

from src.document.model import Document
from src.project.model import Project


def get_document_by_id(db: Session, document_id: str) -> Document | None:
    return db.query(Document).get(document_id)


def create_document(db: Session, project: Project, filename: str | None) -> Document:
    db_document = Document(id=str(uuid4()), name=filename, project=project)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(db: Session, db_document: Document, filename: str) -> Document:
    db_document.name = filename
    db.commit()
    db.refresh(db_document)
    return db_document
