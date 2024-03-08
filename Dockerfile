# installation from https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
# image from https://hub.docker.com/_/python
FROM python:3.10-slim as builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # PYTHONDONTWRITEBYTECODE=1 \
  # PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=0 \
  POETRY_VIRTUALENVS_IN_PROJECT=0 \
  POETRY_VERSION=1.7.1

# System deps: poetry
RUN apt-get update \
    && apt-get -y install libpq-dev gcc netcat-traditional \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} --quiet \
    && pip install psycopg2

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /code/

# Project initialization:
WORKDIR /code/
RUN poetry install --only=main --no-interaction --no-ansi

# Creating folders, and files for a project:
# COPY ./src /code/src
COPY entrypoint.sh ./alembic.ini /code
COPY ./alembic /code/alembic
COPY ./src /code/src
WORKDIR /code

# Use Unprivileged Containers
# https://testdriven.io/blog/docker-best-practices/#order-dockerfile-commands-appropriately
RUN chmod +x /code/entrypoint.sh && \
    addgroup --system --gid 1001 app && \
    adduser  --system -h /code --uid 1001 --group app && \
    mkdir -p /code/files/documents && mkdir -p /code/files/logos && chown -R 1001:1001 /code/files
USER 1001

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
# CMD ["poetry", "run", "python", "-m", "src.main"]
