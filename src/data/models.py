from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(Text, default="")
    logo_id = Column(String(length=255))

    documents = relationship("Document", back_populates="project")
    users = relationship("Permission", back_populates="project")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(length=255), unique=True, index=True)
    hashed_password = Column(String(length=100))

    projects = relationship("Permission", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(length=255), primary_key=True)
    name = Column(String(length=255), index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="documents")


# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object
class Permission(Base):
    # implemented through assiciation object structure
    __tablename__ = "permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)

    permission = Column(String(length=40))
    # permission is only a name (e.g. OWNER, PARTICIPANT), so it should be short
    # Implemented as a string if later additional roles appear

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="users")
