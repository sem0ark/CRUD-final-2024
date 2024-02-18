RUN = poetry run

lint:
	${RUN} ruff format ./src ./test
	${RUN} ruff check --fix ./src ./test
	${RUN} mypy ./src ./test

test:
	${RUN} ruff check ./src --fix
	${RUN} ruff check ./test --fix
	${RUN} pytest

dev:
	${RUN} python ./src/main.py

build:
	docker build -t backend-image .

run-docker:
	docker run -d --name backend -p 80:8000 backend-image

stop-docker:
	docker stop backend
	docker rm backend

stop-docker-clear:
	docker stop backend
	docker rm backend
	docker rmi backend-image

run-compose:
	docker compose up -d db
	docker compose up -d web

stop-compose:
	docker compose stop

stop-compose-clear:
	docker compose down --volumes
