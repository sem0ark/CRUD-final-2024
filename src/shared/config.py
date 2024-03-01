import os

from dotenv import load_dotenv

# load information into environment variables
# TODO: move configuration to Docker Secrets
load_dotenv(".env.test" if os.environ.get("TEST", False) else ".env")

# used direct access, so in case env variable is not available, throw an error
__postgres_user = os.environ["POSTGRES_USER"]
__postgres_password = os.environ["POSTGRES_PASSWORD"]
__postgres_port = os.environ["POSTGRES_PORT"]
__postgres_host = (
    os.environ["POSTGRES_HOST"]
    if not os.environ.get("RUN_LOCAL", False)
    else "localhost"
)
__postgres_db = os.environ["POSTGRES_DB"]

# "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{__postgres_user}:{__postgres_password}\
@{__postgres_host}:{__postgres_port}/{__postgres_db}"

SQLALCHEMY_TEST_DATABASE_URL: str = f"postgresql+psycopg2://{__postgres_user}:{__postgres_password}\
@{__postgres_host}:{__postgres_port}/test"


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# we direct to folders from the config location
FILE_FOLDER = os.path.join("/", "code", "files")

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
