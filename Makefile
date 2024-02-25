RUN = poetry run

lint:
	${RUN} ruff format ./src ./tests
	${RUN} ruff check --fix ./src ./tests
	${RUN} mypy ./src ./tests

test:
	${RUN} ruff format ./src ./tests
	${RUN} mypy ./src ./tests
	${RUN} ruff check ./src ./tests --fix
	${RUN} pytest --cov=src tests/

test-ci:
	${RUN} ruff format ./src ./tests
	${RUN} mypy ./src ./tests
	${RUN} ruff check ./src ./tests --fix
	${RUN} pytest --cov=src tests/

dev:
	docker compose up -d db-postgres
	${RUN} python -m src.main

build:
	docker build -t backend-image .

run-compose:
	docker compose up -d db-postgres
	docker compose up -d web

stop-compose:
	docker compose stop

stop-compose-clear:
	docker compose down --volumes --rmi=local
