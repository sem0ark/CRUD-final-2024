from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

import src.document.dao as document_dao
import src.document.models as document_models
from src.shared.config import (
    ALLOWED_DOCUMENT_EXTENCIONS,
    ALLOWED_DOCUMENT_MIME_TYPES,
    ALLOWED_LOGO_EXTENCIONS,
    ALLOWED_LOGO_MIME_TYPES,
)
from src.shared.database import get_db


def get_document_by_id(
    document_id: str, db: Session = Depends(get_db)
) -> document_models.Document:
    db_document = document_dao.get_document_by_id(db, document_id)
    if not db_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return db_document


# https://fastapi.tiangolo.com/advanced/advanced-dependencies/#create-an-instance


class MIMETypeChecker:
    def __init__(self, allowed_mime, allowed_extencions):
        self.allowed_mime = allowed_mime
        self.allowed_extencions = allowed_extencions

    def __call__(self, file: UploadFile):
        if file.content_type in self.allowed_mime:
            return True

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Allowed file formats are: {', '.join(self.allowed_extencions)}",
        )


is_document = MIMETypeChecker(ALLOWED_DOCUMENT_MIME_TYPES, ALLOWED_DOCUMENT_EXTENCIONS)
is_logo = MIMETypeChecker(ALLOWED_LOGO_MIME_TYPES, ALLOWED_LOGO_EXTENCIONS)
