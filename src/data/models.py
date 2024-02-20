from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(length=255))
    description = mapped_column(Text, default="")
    logo_id = mapped_column(String(length=255))

    documents: Mapped["Document"] = relationship(back_populates="project")
    users: Mapped[list["Permission"]] = relationship(back_populates="project")


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    login = mapped_column(String(length=255), unique=True, index=True)
    hashed_password = mapped_column(String(length=100))

    projects: Mapped[list["Permission"]] = relationship(back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = mapped_column(String(length=255), primary_key=True)
    name = mapped_column(String(length=255), index=True)

    project_id = mapped_column(Integer, ForeignKey("projects.id"))

    project: Mapped["Project"] = relationship(back_populates="documents")


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
class Permission(Base):
    # implemented through assiciation object structure
    __tablename__ = "permissions"

    user_id = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = mapped_column(Integer, ForeignKey("projects.id"), primary_key=True)

    permission: Mapped[str] = mapped_column(String(length=40))
    # permission is only a name (e.g. OWNER, PARTICIPANT), so it should be short
    # Implemented as a string if later additional roles appear

    user: Mapped["User"] = relationship(back_populates="projects")
    project: Mapped["Project"] = relationship(back_populates="users")
