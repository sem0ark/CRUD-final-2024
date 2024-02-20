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


def create_document(db: Session, document: schemas.Document, project: models.Project):
    db_document = models.Document(**document.model_dump())
    db_document.project = project
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


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
