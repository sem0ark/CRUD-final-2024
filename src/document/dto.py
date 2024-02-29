from pydantic import BaseModel, ConfigDict, Field

import src.document.models as document_models


class DocumentCreate(BaseModel):
    name: str = Field(max_length=200)


class Document(DocumentCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)
    # replacement for pydantic 2, see documentation on ConfigDict


def document(db_document: document_models.Document) -> Document:
    return Document(id=db_document.id, name=db_document.name)
