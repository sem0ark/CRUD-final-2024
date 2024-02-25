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
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VERSION=1.7.1

# System deps: poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="$POETRY_HOME/:$PATH"

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --no-cache-dir poetry==${POETRY_VERSION} --quiet \
    && pip install psycopg2

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /code/

# Project initialization:
WORKDIR /code/
RUN poetry install --only=main --no-interaction --no-ansi

# Use Unprivileged Containers
# https://testdriven.io/blog/docker-best-practices/#order-dockerfile-commands-appropriately
RUN addgroup --system app && adduser --system --group app
USER app

# Creating folders, and files for a project:
COPY ./src /code/src
WORKDIR /code

CMD ["poetry", "run", "python", "-m", "src.main"]

# just doesn't work for some reason
# CMD ["poetry", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
