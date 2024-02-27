from pydantic import BaseModel, ConfigDict, Field

from src.document.dto import Document, document
from src.project.model import Project as ProjectModel


class ProjectCreate(BaseModel):
    name: str = Field(max_length=200)
    description: str = ""


class ProjectUpdate(BaseModel):
    name: str | None = Field(max_length=200, default=None)
    description: str | None = None


class ProjectInfo(ProjectCreate):
    id: int
    logo_id: str | None


class Project(ProjectInfo):
    documents: list[Document]

    model_config = ConfigDict(from_attributes=True)


class ProjectListing(BaseModel):
    projects: list[Project]


def project(db_project: ProjectModel) -> Project:
    project_documents = list(db_project.documents) if db_project.documents else []

    return Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
        documents=list(map(document, project_documents)),
    )


# TODO: search for a better solution of
#   transforming SQLAlchemy model into Pydantic schema
def project_info(db_project: ProjectModel) -> ProjectInfo:
    return ProjectInfo(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
    )
