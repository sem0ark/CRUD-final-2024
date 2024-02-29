from sqlalchemy.orm import Session

import src.auth.models as auth_models
import src.project.dto as project_dto
import src.project.models as project_models
import src.user.dao as user_dao
import src.user.models as user_models
from src.shared.logs import log


def create_project(
    db: Session, project: project_dto.ProjectCreate, owner: user_models.User
):
    log.debug(
        f"Creating a project with values: \
name='{project.name}', description='{project.description}'"
    )
    db_project = project_models.Project(**project.model_dump())
    db.add(db_project)

    log.debug(
        f"Adding the creator to the project: login='{owner.login}', id='{owner.id}'"
    )
    a = auth_models.Permission(permission=auth_models.PermissionType.owner.value)
    a.user = owner
    db_project.users.append(a)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_role(
    db: Session, project_id: int, user_id: int
) -> auth_models.Permission | None:
    return db.query(auth_models.Permission).get(
        {"user_id": user_id, "project_id": project_id}
    )


def get_accessible_projects(
    db: Session, user_id: int
) -> list[project_models.Project] | None:
    log.debug(f"Finding accessible projects from user: id='{user_id}'")
    user = user_dao.get_user(db, user_id)
    if not user:
        return None

    return [assoc.project for assoc in user.projects]


def get_project(db: Session, project_id: int) -> project_models.Project | None:
    return db.query(project_models.Project).get(project_id)


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