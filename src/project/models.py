from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# changed to standard import to solve cyclyc imports problem
import src.auth.models
import src.document.models
from src.shared.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text, default="")

    logo_id: Mapped[str] = mapped_column(String(length=255), nullable=True)

    documents: Mapped[list["src.document.models.Document"]] = relationship(
        back_populates="project"
    )
    users: Mapped[list["src.auth.models.Permission"]] = relationship(
        back_populates="project"
    )
