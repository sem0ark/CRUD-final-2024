from ..data import models, schemas


def render_document(document: models.Document) -> schemas.Document:
    return schemas.Document(id=document.id, name=document.name)


def render_project(db_project: models.Project) -> schemas.Project:
    project_documents = list(db_project.documents) if db_project.documents else []

    return schemas.Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
        documents=list(map(render_document, project_documents)),
    )


# TODO: search for a better solution of
#   transforming SQLAlchemy model into Pydantic schema
def render_project_info(db_project: models.Project) -> schemas.ProjectInfo:
    return schemas.ProjectInfo(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        logo_id=db_project.logo_id,
    )
