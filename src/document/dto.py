from pydantic import BaseModel, ConfigDict, Field

import src.document.models as document_models
from src.shared.dto import BaseTimestamp


class DocumentCreate(BaseModel):
    name: str = Field(max_length=200)


class Document(DocumentCreate, BaseTimestamp):
    id: str

    model_config = ConfigDict(from_attributes=True)
    # replacement for pydantic 2, see documentation on ConfigDict


def document(db_document: document_models.Document) -> Document:
    return Document(
        id=db_document.id,
        name=db_document.name,
        created_at=db_document.created_at,
        updated_at=db_document.updated_at,
    )
