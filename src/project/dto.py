from pydantic import BaseModel, ConfigDict, Field

import src.project.models as project_models
from src.shared.dto import BaseTimestamp


class ProjectCreate(BaseModel):
    name: str = Field(max_length=200)
    description: str = ""


class ProjectUpdate(BaseModel):
    name: str | None = Field(max_length=200, default=None)
    description: str | None = None


class ProjectInfo(ProjectCreate):
    id: int


class Project(ProjectInfo, BaseTimestamp):
    model_config = ConfigDict(from_attributes=True)


class ProjectListing(BaseModel):
    projects: list[Project]


def project(db_project: project_models.Project) -> Project:
    # project_documents = list(db_project.documents) if db_project.documents else []

    return Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        created_at=db_project.created_at,
        updated_at=db_project.updated_at,
    )


# TODO: search for a better solution of
#   transforming SQLAlchemy model into Pydantic schema
def project_info(db_project: project_models.Project) -> ProjectInfo:
    return ProjectInfo(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
    )
