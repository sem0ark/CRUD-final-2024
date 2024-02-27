from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.permission.models import Permission, PermissionType
from src.project.model import Project
from src.shared.logs import log
from src.user.models import User


def grant_access_to_user(db: Session, project: Project, user: User):
    log.debug(
        f"Giving user[{user.id}, {user.login}] \
access to project [{project.id}, {project.name}]"
    )
    try:
        a = Permission(permission=PermissionType.participant.value)
        a.user = user
        project.users.append(a)
        db.commit()
        db.refresh(project)
    except IntegrityError:
        db.rollback()
        return None
    return project
