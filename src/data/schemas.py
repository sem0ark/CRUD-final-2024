from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    name: str = Field(max_length=200)


class Document(DocumentCreate):
    id: str

    # class Config:
    #     orm_mode = True
    # replacement for pydantic 2
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str = Field(max_length=200)
    description: str = ""


class ProjectInfo(ProjectCreate):
    id: int
    logo_id: str | None


class Project(ProjectInfo):
    documents: list[Document]

    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    login: str = Field(max_length=200)


class UserCreate(UserBase):
    password: str = Field(
        min_length=6, description="Password should be at least 6 characters long"
    )


class User(UserBase):
    id: int

    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)
