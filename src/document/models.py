from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.project.models
from src.shared.database import Base

# standard import to solve cyclyc import problem
# https://stackoverflow.com/questions/5748946/pythonic-way-to-resolve-circular-import-statements


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(length=255), primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), index=True, nullable=False)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
    )
    # implemented like that to avoid import cycles + allowing mypy type checking
    project: Mapped["src.project.models.Project"] = relationship(
        back_populates="documents"
    )
