from pydantic import BaseModel, ConfigDict, Field

from src.document.dto import Document as DocumentSchema
from src.document.model import Document as DocumentModel


class DocumentCreate(BaseModel):
    name: str = Field(max_length=200)


class Document(DocumentCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)
    # replacement for pydantic 2, see documentation on ConfigDict


def document(db_document: DocumentModel) -> DocumentSchema:
    return DocumentSchema(id=db_document.id, name=db_document.name)
