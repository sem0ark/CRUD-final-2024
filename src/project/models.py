import enum

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

import src.document.models
import src.project.models
import src.user.models

# changed to standard import to solve cyclyc imports problem
from src.shared.database import Base
from src.shared.models import BaseTimestamp


class PermissionType(enum.Enum):
    owner = "OWNER"
    participant = "PARTICIPANT"


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
class Permission(Base, BaseTimestamp):
    # implemented through assiciation object structure
    __tablename__ = "permissions"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)

    type: Mapped[str] = mapped_column(Enum(PermissionType), nullable=False)

    user: Mapped["src.user.models.User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")

    def __str__(self):
        return f"PermissionModel[\
user {self.user_id} is {self.type} of project {self.project_id}]"

    def __repr__(self):
        return self.__str__()


class Project(Base, BaseTimestamp):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text, default="")

    logo_id: Mapped[str | None] = mapped_column(String(length=255), nullable=True)

    documents: Mapped[list["src.document.models.Document"]] = relationship(
        back_populates="project"
    )
    users: Mapped[list["Permission"]] = relationship(back_populates="project")

    def __str__(self):
        return f"ProjectModel[{self.id}, {self.name}, {self.description}]"

    def __repr__(self):
        return self.__str__()
