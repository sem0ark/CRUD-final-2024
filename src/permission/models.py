import enum

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

from src.project.model import Project
from src.shared.database import Base
from src.user.models import User


class PermissionType(enum.Enum):
    owner = "OWNER"
    participant = "PARTICIPANT"


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
class Permission(Base):
    # implemented through assiciation object structure
    __tablename__ = "permissions"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)

    type: Mapped[str] = mapped_column(Enum(PermissionType), nullable=False)

    user: Mapped["User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")
