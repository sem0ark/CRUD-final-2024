from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.project.model import Project
from src.shared.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(length=255), primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), index=True, nullable=False)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="documents")
