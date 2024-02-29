from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.auth.models as auth_models
import src.project.dao as project_dao
import src.user.dependencies as user_deps
import src.user.models as user_models
from src.shared.database import get_db
from src.shared.logs import log

# https://stackoverflow.com/questions/68668417/
#   is-it-possible-to-pass-path-arguments-into-fastapi-dependency-functions


def project_role(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
) -> auth_models.Permission:
    project_role = project_dao.get_project_role(db, project_id, current_user.id)

    log.debug(
        f"Received project role {project_role.type if project_role else None} \
for user {current_user.login} on project id {project_id}"
    )

    if not project_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have access to the project",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return project_role


def is_project_owner(
    project_role: auth_models.Permission = Depends(project_role),
) -> bool:
    log.debug("User is trying to access owner-role action")

    if project_role.type != auth_models.PermissionType.owner:
        log.debug("User failed to access owner-role action")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the project owner",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# implemented for readability
def is_project_participant(
    _project_role: auth_models.PermissionType = Depends(project_role),
) -> bool:
    return True
