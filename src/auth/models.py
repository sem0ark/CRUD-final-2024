import enum

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

import src.project.models
import src.user.models
from src.shared.database import Base


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

    user: Mapped["src.user.models.User"] = relationship(back_populates="projects")
    project: Mapped["src.project.models.Project"] = relationship(back_populates="users")
