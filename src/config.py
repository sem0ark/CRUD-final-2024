import os

# TODO: Remove development credentials
__postgres_user = os.environ.get("POSTGRES_USER", "dev")
__postgres_password = os.environ.get("POSTGRES_PASSWORD", "dev")
__postgres_port = 5432
__postgres_host = "localhost"

# "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URL: str = f"postgresql+psycopg2://{__postgres_user}:{__postgres_password}\
@{__postgres_host}:{__postgres_port}/db"

SECRET_KEY = os.environ.get("SECRET_KEY", "1234")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
