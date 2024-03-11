from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.project.dto as project_dto
import src.project.models as project_models
import src.user.dao as user_dao
import src.user.models as user_models
from src.shared.logs import log


def get_project(db: Session, project_id: int) -> project_models.Project | None:
    return db.get(project_models.Project, project_id)  # type: ignore


def get_accessible_projects(
    db: Session,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
) -> list[project_models.Project] | None:
    log.debug(f"Finding accessible projects from user: id='{user_id}'")
    user = user_dao.get_user(db, user_id)

    if not user:
        return None

    return [
        permission.project
        for permission in db.query(project_models.Permission)
        .filter_by(user_id=user_id)
        .limit(limit)
        .offset(offset)
        .all()
    ]


def create_project(
    db: Session, project: project_dto.ProjectCreate, owner: user_models.User
) -> project_models.Project:
    log.debug(
        f"Creating a project with values: \
name='{project.name}', description='{project.description}'"
    )
    db_project = project_models.Project(
        **project.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
    )
    db.add(db_project)

    log.debug(
        f"Adding the creator to the project: login='{owner.login}', id='{owner.id}'"
    )
    a = project_models.Permission(type=project_models.PermissionType.owner)
    a.user = owner
    db_project.users.append(a)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
    db: Session,
    db_project: project_models.Project,
    update_data: project_dto.ProjectUpdate,
) -> project_models.Project | None:
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


def get_project_role(
    db: Session, project_id: int, user_id: int
) -> project_models.Permission | None:
    return db.get(  # type: ignore
        project_models.Permission, {"user_id": user_id, "project_id": project_id}
    )


def grant_access_to_user(
    db: Session, project: project_models.Project, user: user_models.User
):
    log.debug(f"Giving {user.login} access to project [{project.id}]")
    if get_project_role(db, project.id, user.id):
        return None

    try:
        a = project_models.Permission(type=project_models.PermissionType.participant)
        a.user = user
        project.users.append(a)
        db.commit()
        db.refresh(project)
    except IntegrityError:
        log.info(f"Failed to grant access to user {user.login}, access already exists")
        db.rollback()
        db.commit()
        return None
    return project
