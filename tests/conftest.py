import os
from io import BytesIO
from typing import Callable, Generator

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import text as sa_text
from sqlalchemy.orm import Session, sessionmaker

import src.auth.dao as auth_dao
import src.auth.dto as auth_dto
import src.auth.utils as auth_utils
import src.document.dao as document_dao
import src.document.models as document_models
import src.logo.dao as logo_dao
import src.project.dao as project_dao
import src.project.dto as project_dto
import src.project.models as project_models
import src.services.file_service as file_service
import src.user.dao as user_dao
import src.user.dto as user_dto
import src.user.models as user_models
from src.main import app
from src.shared.config import SQLALCHEMY_TEST_DATABASE_URL
from src.shared.database import get_db
from src.shared.logs import log

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
    project_data_list: list[project_models.Project],
) -> auth_dto.Token:
    participant = make_user("participant_test_user")
    for project in project_data_list:
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


@pytest.fixture(scope="function")
def authorized_users(
    db: Session,
    main_user: user_models.User,
    participant_user: user_models.User,
) -> list[user_models.User]:
    return [
        main_user,
        participant_user,
    ]


@pytest.fixture(scope="function")
def authorized_users_token(
    make_token: Callable[[str], user_models.User],
    main_user_token: auth_dto.Token,
    participant_user_token: auth_dto.Token,
) -> list[auth_dto.Token]:
    return [
        main_user_token,
        participant_user_token,
    ]


@pytest.fixture(scope="function")
def authorized_users_token_header(
    make_token: Callable[[str], user_models.User],
    main_user_token_header: dict[str, str],
    participant_user_token_header: dict[str, str],
) -> list[dict[str, str]]:
    return [
        main_user_token_header,
        participant_user_token_header,
    ]


@pytest.fixture(scope="function")
def all_users(
    db: Session,
    main_user: user_models.User,
    participant_user: user_models.User,
    unauthorized_user: user_models.User,
) -> list[user_models.User]:
    return [
        main_user,
        participant_user,
        unauthorized_user,
    ]


@pytest.fixture(scope="function")
def all_users_token(
    make_token: Callable[[str], user_models.User],
    main_user_token: auth_dto.Token,
    participant_user_token: auth_dto.Token,
    unauthorized_user_token: auth_dto.Token,
) -> list[auth_dto.Token]:
    return [
        main_user_token,
        participant_user_token,
        unauthorized_user_token,
    ]


@pytest.fixture(scope="function")
def all_users_token_header(
    make_token: Callable[[str], user_models.User],
    main_user_token_header: dict[str, str],
    participant_user_token_header: dict[str, str],
    unauthorized_user_token_header: dict[str, str],
) -> list[dict[str, str]]:
    return [
        main_user_token_header,
        participant_user_token_header,
        unauthorized_user_token_header,
    ]


# Test environment configuration
TOTAL_PROJECTS = 3


@pytest.fixture(scope="function")
def project_data_list(
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
def project_data(
    project_data_list: list[project_models.Project],
) -> project_models.Project:
    return project_data_list[0]


@pytest.fixture(scope="function")
def document_data(
    db: Session, project_data: project_models.Project
) -> Generator[document_models.Document, None, None]:
    document = BytesIO(b"Testing Document (1)")
    document_name = "some Data 123.pdf"

    db_document = document_dao.create_document(db, project_data, document_name)
    file_service.save_document(document, db_document.id)

    yield db_document

    try:
        file_service.delete_document_by_id(db_document.id)
        document_dao.delete_document(db, db_document.id)
    except FileNotFoundError:
        log.warning("Failed to remove the document from the fixture")


# files


@pytest.fixture(scope="session")
def good_upload_file():
    document = BytesIO(b"Testing Document (1)")
    document_name = "some Data 123.pdf"
    upload_file = UploadFile(file=document, filename=document_name)
    return upload_file


@pytest.fixture(scope="session")
def good_upload_file_2():
    document = BytesIO(b"Testing Document (2)")
    document_name = "some Data 124.pdf"
    upload_file = UploadFile(file=document, filename=document_name)
    return upload_file


@pytest.fixture(scope="session")
def bad_upload_file():
    document = BytesIO(b"Some document cotents")
    document_name = "important document.txt"
    upload_file = UploadFile(file=document, filename=document_name)
    return upload_file


# logos
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.jpg")


@pytest.fixture(scope="function")
def logo_file(
    project_data: project_models.Project,
    db: Session,
) -> Generator[str, None, None]:
    logo_id = logo_dao.create_logo(db, project_data)
    file_service.save_image(open(image_path, "rb"), logo_id)
    yield logo_id
    try:
        file_service.delete_document_by_id(logo_id)
        logo_dao.delete_logo(db, project_data)
    except FileNotFoundError:
        log.warning("Failed to remove the logo from the fixture")


@pytest.fixture(scope="session")
def good_upload_logo():
    upload_file = UploadFile(file=open(image_path, "rb"), filename="sample.jpg")
    return upload_file
