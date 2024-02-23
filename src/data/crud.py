from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..utils.logs import getLogger
from . import models, schemas, types

log = getLogger()


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).get(user_id)


def get_user_by_login(db: Session, login: str) -> models.User | None:
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(db: Session, user: schemas.UserDB) -> models.User | None:
    db_user = models.User(login=user.login, hashed_password=user.hashed_password)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    db.refresh(db_user)
    return db_user


def get_project(db: Session, project_id: int) -> models.Project | None:
    return db.query(models.Project).get(project_id)


def update_project(
    db: Session, db_project: models.Project, update_data: schemas.ProjectUpdate
) -> models.Project | None:
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


def grant_access_to_user(db: Session, project: models.Project, user: models.User):
    log.debug(
        f"Giving user[{user.id}, {user.login}] \
access to project [{project.id}, {project.name}]"
    )
    try:
        a = models.Permission(permission=types.PermissionType.participant.value)
        a.user = user
        project.users.append(a)
        db.commit()
        db.refresh(project)
    except IntegrityError:
        db.rollback()
        return None
    return project


def create_project(db: Session, project: schemas.ProjectCreate, owner: models.User):
    log.debug(
        f"Creating a project with values: \
name='{project.name}', description='{project.description}'"
    )
    db_project = models.Project(**project.model_dump())
    db.add(db_project)

    log.debug(
        f"Adding the creator to the project: login='{owner.login}', id='{owner.id}'"
    )
    a = models.Permission(permission=types.PermissionType.owner.value)
    a.user = owner
    db_project.users.append(a)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_role(
    db: Session, project_id: int, user_id: int
) -> models.Permission | None:
    return db.query(models.Permission).get(
        {"user_id": user_id, "project_id": project_id}
    )


def get_accessible_projects(db: Session, user_id: int) -> list[models.Project] | None:
    log.debug(f"Finding accessible projects from user: id='{user_id}'")
    user = get_user(db, user_id)
    if not user:
        return None

    return [assoc.project for assoc in user.projects]


def get_document_by_id(db: Session, document_id: str) -> models.Document | None:
    return db.query(models.Document).get(document_id)


def get_project_by_document_id(db: Session, document_id: str) -> models.Project | None:
    db_document = get_document_by_id(db, document_id)
    if not db_document:
        return None
    return db_document.project


def get_project_id_by_document_id(db: Session, document_id: str) -> int | None:
    project = get_project_by_document_id(db, document_id)
    if not project:
        return None
    return project.id


def create_document(
    db: Session, project: models.Project, filename: str | None
) -> models.Document:
    db_document = models.Document(id=str(uuid4()), name=filename, project=project)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(
    db: Session, db_document: models.Document, filename: str
) -> models.Document:
    db_document.name = filename
    db.commit()
    db.refresh(db_document)
    return db_document
