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
    log.debug(f"Giving {user.login} access to project [{project.id}]")
    try:
        a = auth_models.Permission(type=auth_models.PermissionType.participant)
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


def authenticate_user(db: Session, login: str, password: str):
    user = user_dao.get_user_by_login(db, login)
    log.debug(f"Authenticating user {login}")
    if not user:
        log.info(f"Was not able to find user {login}")
        return False
    if not auth_utils.verify_password(password, user.hashed_password):
        log.info(f"Password verification for {login} failed")
        return False
    log.debug("Authentication successed")
    return user


def get_project_role(
    db: Session, project_id: int, user_id: int
) -> auth_models.Permission | None:
    return db.get(  # type: ignore
        auth_models.Permission, {"user_id": user_id, "project_id": project_id}
    )
