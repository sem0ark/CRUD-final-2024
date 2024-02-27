from sqlalchemy.orm import Session

from src.document.dao import get_document_by_id
from src.permission.models import Permission, PermissionType
from src.project.dto import ProjectCreate, ProjectUpdate
from src.project.model import Project
from src.shared.logs import log
from src.user.dao import get_user
from src.user.models import User


def create_project(db: Session, project: ProjectCreate, owner: User):
    log.debug(
        f"Creating a project with values: \
name='{project.name}', description='{project.description}'"
    )
    db_project = Project(**project.model_dump())
    db.add(db_project)

    log.debug(
        f"Adding the creator to the project: login='{owner.login}', id='{owner.id}'"
    )
    a = Permission(permission=PermissionType.owner.value)
    a.user = owner
    db_project.users.append(a)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_role(db: Session, project_id: int, user_id: int) -> Permission | None:
    return db.query(Permission).get({"user_id": user_id, "project_id": project_id})


def get_accessible_projects(db: Session, user_id: int) -> list[Project] | None:
    log.debug(f"Finding accessible projects from user: id='{user_id}'")
    user = get_user(db, user_id)
    if not user:
        return None

    return [assoc.project for assoc in user.projects]


def get_project_by_document_id(db: Session, document_id: str) -> Project | None:
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    return db_document.project


def get_project_id_by_document_id(db: Session, document_id: str) -> int | None:
    project = get_project_by_document_id(db, document_id)
    if not project:
        return None
    return project.id


def get_project(db: Session, project_id: int) -> Project | None:
    return db.query(Project).get(project_id)


def update_project(
    db: Session, db_project: Project, update_data: ProjectUpdate
) -> Project | None:
    # TODO: refactor, search for a better solution, because .update(dict) doesn't work
    if update_data.name is not None:
        db_project.name = update_data.name

    if update_data.description is not None:
        db_project.description = update_data.description

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> None:
    db_project = get_project(db, project_id)
    db.delete(db_project)
