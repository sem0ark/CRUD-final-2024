import enum

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

from src.data.database import Base


class PermissionType(enum.Enum):
    owner = "OWNER"
    participant = "PARTICIPANT"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text, default="")

    logo_id: Mapped[str] = mapped_column(String(length=255), nullable=True)

    documents: Mapped[list["Document"]] = relationship(back_populates="project")
    users: Mapped[list["Permission"]] = relationship(back_populates="project")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(
        String(length=255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=100), nullable=False)

    projects: Mapped[list["Permission"]] = relationship(back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(length=255), primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), index=True, nullable=False)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id"), nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="documents")


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
class Permission(Base):
    # implemented through assiciation object structure
    __tablename__ = "permissions"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)

    type: Mapped[str] = mapped_column(Enum(PermissionType), nullable=False)

    user: Mapped["User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")
