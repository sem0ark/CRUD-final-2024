RUN = poetry run

lint:
	${RUN} ruff format ./src ./tests
	${RUN} ruff check --fix ./src ./tests
	${RUN} mypy ./src ./tests

test:
	${RUN} ruff format ./src ./tests
	${RUN} mypy ./src ./tests
	${RUN} ruff check ./src ./tests --fix
	export RUN_LOCAL='1' && ${RUN} pytest --cov=src tests/


build:
	docker build -t backend-image .

run-compose:
	docker compose up -d db
	docker compose up -d web

stop-compose:
	docker compose stop

stop-compose-clear:
	docker compose down --rmi=local

stop-compose-clear-full:
	docker compose down --volumes --rmi=local

dev:
	make stop-compose-clear
	make run-compose
	docker compose logs web -f
