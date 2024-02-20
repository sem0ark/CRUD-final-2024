from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas, types


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


def create_project(db: Session, project: schemas.ProjectCreate, owner: models.User):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    a = models.Permission(permission=types.PermissionType.owner)
    a.user = owner
    db_project.users.append(a)
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
) -> types.PermissionType | None:
    return db.query(models.Permission).get((user_id, project_id))


def get_accessible_projects(db: Session, user_id: int) -> list[models.Project] | None:
    user = get_user(db, user_id)
    if not user:
        return None

    return [assoc.project for assoc in user.projects]
