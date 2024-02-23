import os

# TODO: Remove development credentials
__postgres_user = os.environ.get("POSTGRES_USER", "dev")
__postgres_password = os.environ.get("POSTGRES_PASSWORD", "dev")
__postgres_port = 5432
__postgres_host = "localhost"

# "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{__postgres_user}:{__postgres_password}\
@{__postgres_host}:{__postgres_port}/db"

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "f939271c362c032d65dc2668b134c399b129ec54a826f4ffd9a26ebaad83213"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DOCUMENT_FOLDER = os.path.join(os.getcwd(), "..", "files", "documents")
LOGO_FOLDER = os.path.join(os.getcwd(), "..", "files", "logos")


ALLOWED_DOCUMENT_MIME_TYPES = [
    "application/pdf",  # .pdf
    "application/msword"  # .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
]

ALLOWED_DOCUMENT_EXTENCIONS = [".docx", ".doc", ".pdf"]

ALLOWED_LOGO_MIME_TYPES = [
    "image/png",  # .png
    "image/jpeg",  # .jpg .jpeg
]

ALLOWED_LOGO_EXTENCIONS = [".png", ".jpg", ".jpeg"]

# later change all incoming logos to size x size square JPG images to save space
LOGO_SIZE = 400
