RUN = poetry run

lint:
	${RUN} ruff format ./src ./tests
	${RUN} ruff check --fix ./src ./tests
	${RUN} mypy ./src ./tests

test:
	${RUN} ruff format ./src ./tests
	mypy ./src ./tests
	${RUN} ruff check ./src ./tests --fix
	# https://stackoverflow.com/questions/29377853/how-can-i-use-environment-variables-in-docker-compose
	make stop-compose-clear-full
	docker compose --env-file ./.env.test up -d db
	export TEST=1 && ${RUN} pytest --cov=src tests/ -vv -o log_cli=true


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


dev-local:
	make stop-compose
	docker compose --env-file ./.env up -d db
	poetry run uvicorn src.main:app --host "0.0.0.0" --port 8000 --reload

dev-container:
	make stop-compose-clear-full
	docker compose --env-file ./.env up -d db
	docker compose --env-file ./.env up -d web
	docker compose logs web -f
