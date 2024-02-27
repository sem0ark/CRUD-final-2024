from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.permission.models import Permission, PermissionType
from src.project.dao import get_project_role
from src.shared.database import get_db
from src.shared.logs import log
from src.user.dependencies import get_current_user
from src.user.models import User

# https://stackoverflow.com/questions/68668417/
#   is-it-possible-to-pass-path-arguments-into-fastapi-dependency-functions


def project_role(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Permission:
    project_role = get_project_role(db, project_id, current_user.id)

    log.debug(
        f"Received project role {project_role} \
for user {current_user.login} on project id {project_id}"
    )

    if not project_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have access to the project",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return project_role


def is_project_owner(project_role: Permission = Depends(project_role)) -> bool:
    log.debug("User is trying to access owner-role action")

    if project_role.type != PermissionType.owner.value:
        log.debug("User failed to access owner-role action")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the project owner",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# implemented for readability
def is_project_participant(
    _project_role: PermissionType = Depends(project_role),
) -> bool:
    return True
