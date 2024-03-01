from io import BytesIO
from typing import Callable, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import text as sa_text
from sqlalchemy.orm import Session, sessionmaker

import src.auth.dao as auth_dao
import src.auth.dto as auth_dto
import src.auth.utils as auth_utils
import src.document.dao as document_dao
import src.project.dao as project_dao
import src.project.dto as project_dto
import src.project.models as project_models
import src.user.dao as user_dao
import src.user.dto as user_dto
import src.user.models as user_models
from src.main import app
from src.services import file_service
from src.shared.config import SQLALCHEMY_TEST_DATABASE_URL
from src.shared.database import get_db

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# instance will be the session

# https://fastapi.tiangolo.com/advanced/testing-dependencies/
# https://testdriven.io/blog/fastapi-crud/


def get_test_db() -> Generator[Session, None, None]:
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="module")
def client():
    c = TestClient(app)
    yield c


@pytest.fixture(scope="module")
def db() -> Generator[Session, None, None]:
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


table_names = [
    "users",
    "projects",
    "documents",
    "permissions",
]


@pytest.fixture(scope="function", autouse=True)
def truncate_table(db: Session) -> None:
    for table_name in table_names:
        db.execute(sa_text(f"""TRUNCATE TABLE {table_name} CASCADE"""))
    db.commit()


# Authentication configuration


@pytest.fixture(scope="module")
def make_user(db: Session) -> Callable[[str], user_models.User]:
    def factory(login: str) -> user_models.User:
        db_user = user_dao.create_user(
            db,
            user_dto.UserDB(
                login=login,
                hashed_password=auth_utils.get_password_hash("C0mplex P455w0rd"),
            ),
        )

        if not db_user:
            raise TypeError(f"Failed to create user {login}")

        return db_user

    return factory


@pytest.fixture(scope="module")
def make_token() -> Callable[[user_models.User], auth_dto.Token]:
    def factory(user: user_models.User) -> auth_dto.Token:
        return auth_utils.login_user(user)

    return factory


# Users


@pytest.fixture(scope="function")
def main_user(make_user: Callable[[str], user_models.User]) -> auth_dto.Token:
    return make_user("main_test_user")


@pytest.fixture(scope="function")
def main_user_token(
    make_token: Callable[[str], user_models.User], main_user: user_models.User
) -> auth_dto.Token:
    return make_token(main_user)


@pytest.fixture(scope="function")
def main_user_token_header(
    make_token: Callable[[str], user_models.User], main_user: user_models.User
) -> dict[str, str]:
    token = make_token(main_user)
    return {"Authorization": f"{token.token_type} {token.access_token}"}


@pytest.fixture(scope="function")
def unauthorized_user(make_user: Callable[[str], user_models.User]) -> auth_dto.Token:
    return make_user("unauthorized_test_user")


@pytest.fixture(scope="function")
def unauthorized_user_token(
    make_token: Callable[[str], user_models.User], unauthorized_user: user_models.User
) -> auth_dto.Token:
    return make_token(unauthorized_user)


@pytest.fixture(scope="function")
def unauthorized_user_token_header(
    make_token: Callable[[str], user_models.User], unauthorized_user: user_models.User
) -> dict[str, str]:
    token = make_token(unauthorized_user)
    return {"Authorization": f"{token.token_type} {token.access_token}"}


@pytest.fixture(scope="function")
def participant_user(
    make_user: Callable[[str], user_models.User],
    db: Session,
    project_data: list[project_models.Project],
) -> auth_dto.Token:
    participant = make_user("participant_test_user")
    for project in project_data:
        auth_dao.grant_access_to_user(db, project, participant)
    return participant


@pytest.fixture(scope="function")
def participant_user_token(
    make_token: Callable[[str], user_models.User], participant_user: user_models.User
) -> auth_dto.Token:
    return make_token(participant_user)


@pytest.fixture(scope="function")
def participant_user_token_header(
    make_token: Callable[[str], user_models.User], participant_user: user_models.User
) -> dict[str, str]:
    token = make_token(participant_user)
    return {"Authorization": f"{token.token_type} {token.access_token}"}


# Test environment configuration
TOTAL_PROJECTS = 3


@pytest.fixture(scope="function")
def project_data(
    db: Session, main_user: user_models.User
) -> list[project_models.Project]:
    project_schemas = [
        project_dto.ProjectCreate(name=f"Testing Project ({i})")
        for i in range(1, TOTAL_PROJECTS + 1)
    ]
    return [
        project_dao.create_project(db, project, main_user)
        for project in project_schemas
    ]


@pytest.fixture(scope="function")
def document_data(
    db: Session, project: project_models.Project
) -> list[project_models.Project]:
    document = BytesIO(b"Testing Document (1)")
    document_name = "some Data 123.pdf"
    document_objects = []

    db_document = document_dao.create_document(db, project, document_name)
    file_service.save_document(document, db_document.id)
    document_objects.append(db_document)

    return document_objects
