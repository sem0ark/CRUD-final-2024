RUN = poetry run

lint:
	${RUN} ruff format ./src ./tests
	${RUN} ruff check --fix ./src ./tests
	${RUN} mypy ./src ./tests

test:
	${RUN} ruff format ./src ./tests
	${RUN} mypy ./src ./tests
	${RUN} ruff check ./src ./tests --fix
	# https://stackoverflow.com/questions/29377853/how-can-i-use-environment-variables-in-docker-compose
	make stop-compose-clear-full
	docker compose --env-file ./.env.test up -d db
	export TEST='1' && ${RUN} pytest --cov=src tests/ -vv --lf -o log_cli=true


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
	make stop-compose-clear-full
	make run-compose
	docker compose logs web -f
