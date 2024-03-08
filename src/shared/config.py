import os

from dotenv import load_dotenv

# load information into environment variables
# TODO: move configuration to Docker Secrets
RUN_TEST = bool(os.environ.get("TEST", False))

load_dotenv(".env.test" if RUN_TEST else ".env")


# General config

RUN_LOCAL = bool(os.environ.get("RUN_LOCAL", False))
RUN_CONTAINER = bool(os.environ.get("RUN_CONTAINER", False))  # run in the container
RUN_CLOUD = bool(os.environ.get("RUN_CLOUD", False))  # run in the container


# Database

# used direct access, so in case env variable is not available, throw an error
__postgres_user = os.environ["POSTGRES_USER"]
__postgres_password = os.environ["POSTGRES_PASSWORD"]
__postgres_port = os.environ["POSTGRES_PORT"]
__postgres_host = "localhost" if RUN_LOCAL else os.environ["POSTGRES_HOST"]
__postgres_db = os.environ["POSTGRES_DB"]

# "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{__postgres_user}:{__postgres_password}\
@{__postgres_host}:{__postgres_port}/{__postgres_db}"

# Auth

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Files

# we direct to folders from the config location
FILE_FOLDER = ""

if RUN_LOCAL:
    FILE_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "files"
    )

if RUN_CONTAINER:
    FILE_FOLDER = os.path.join("/", "code", "files")

if RUN_CLOUD:
    FILE_FOLDER = os.environ["S3_BUCKET"]

DOCUMENT_FOLDER = os.path.join(FILE_FOLDER, "documents")
LOGO_FOLDER = os.path.join(FILE_FOLDER, "logos")


# File processing

ALLOWED_DOCUMENT_MIME_TYPES = [
    "application/pdf",  # .pdf
    "application/msword",  # .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
]

ALLOWED_DOCUMENT_EXTENCIONS = [".docx", ".doc", ".pdf"]

ALLOWED_LOGO_MIME_TYPES = [
    "image/png",  # .png
    "image/jpeg",  # .jpg .jpeg
]

ALLOWED_LOGO_EXTENCIONS = [".png", ".jpg", ".jpeg"]

# later change all incoming logos to "size x size" square JPG images to save space
LOGO_SIZE = 200
