from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.auth.models as auth_models
import src.auth.utils as auth_utils
import src.project.models as project_models
import src.user.dao as user_dao
import src.user.models as user_models
from src.shared.logs import log


def grant_access_to_user(
    db: Session, project: project_models.Project, user: user_models.User
):
    log.debug(
        f"Giving user[{user.id}, {user.login}] \
access to project [{project.id}, {project.name}]"
    )
    try:
        a = auth_models.Permission(
            permission=auth_models.PermissionType.participant.value
        )
        a.user = user
        project.users.append(a)
        db.commit()
        db.refresh(project)
    except IntegrityError:
        db.rollback()
        return None
    return project


def authenticate_user(db: Session, login: str, password: str):
    user = user_dao.get_user_by_login(db, login)
    if not user:
        return False
    if not auth_utils.verify_password(password, user.hashed_password):
        return False
    return user
