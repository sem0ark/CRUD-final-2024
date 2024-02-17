RUN = poetry run

.PHONY = help test run clean

lint:
	${RUN} ruff format ./src ./test
	${RUN} ruff check --fix ./src ./test
	${RUN} mypy ./src ./test

test:
	${RUN} ruff check ./src --fix
	${RUN} ruff check ./test --fix
	${RUN} pytest

run:
	${RUN} python ./src/main.py
