from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.project.models
from src.shared.database import Base
from src.shared.models import BaseTimestamp

# standard import to solve cyclyc import problem
# https://stackoverflow.com/questions/5748946/pythonic-way-to-resolve-circular-import-statements


class Document(Base, BaseTimestamp):
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

    def __str__(self):
        return f"DocumentModel[{self.id}, {self.name}]"

    def __repr__(self):
        return self.__str__()
