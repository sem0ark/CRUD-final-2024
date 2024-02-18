from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str) -> models.User | None:
    return db.query(models.User).filter(models.User.id == login).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = user.password
    db_user = models.User(login=user.login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_project(db: Session, project_id: int) -> models.Project | None:
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def delete_project(db: Session, project_id: int) -> None:
    db_project = get_project(db, project_id)
    db.delete(db_project)


def create_project(
    db: Session,
    project: schemas.ProjectCreate,
    # owner: models.User
):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # turned off before implementing the authentication
    # a = models.Permission(permission=types.PermissionType.owner)
    # a.user = owner
    # db_project.users.append(a)
    return db_project


def create_document(db: Session, document: schemas.Document, project: models.Project):
    db_document = models.Document(**document.model_dump())
    db_document.project = project
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document
