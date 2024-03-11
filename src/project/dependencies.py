from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.project.dao as project_dao
import src.project.models as project_models
import src.user.dependencies as user_deps
import src.user.models as user_models
from src.shared.database import get_db
from src.shared.logs import log


def get_project_by_id(
    project_id: int, db: Session = Depends(get_db)
) -> project_models.Project:
    db_project = project_dao.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_project


# https://stackoverflow.com/questions/68668417/
#   is-it-possible-to-pass-path-arguments-into-fastapi-dependency-functions


def project_role(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(user_deps.get_current_user),
) -> project_models.Permission:
    project_role = project_dao.get_project_role(db, project_id, current_user.id)

    if not project_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have access to the project",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return project_role


def is_project_owner(
    project_role: project_models.Permission = Depends(project_role),
) -> bool:
    log.debug("User is trying to access owner-role action")

    if project_role.type != project_models.PermissionType.owner:
        log.info("User failed to access owner-role action")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the project owner",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# implemented for readability
def is_project_participant(
    _project_role: project_models.PermissionType = Depends(project_role),
) -> bool:
    log.debug("User has access to project")
    return True
