ACTIVATE_VENV = pipenv run

.PHONY:
	black-format \
	black-format-check \
	bootstrap \
	cheeseshop \
	db-up \
	db-down \
	isort \
	isort-check \
	nuke-venv \
	start-aldebaran \
	start-aldebaran-local \
	test \

black-format:
	@$(ACTIVATE_VENV) black . -S -l 99

black-format-check:
	@$(ACTIVATE_VENV) black . -S -l 99

bootstrap: nuke-venv cheeseshop

cheeseshop:
	@pipenv install --dev

db-up:
	@docker run -d --name aldebaran_test -p 9432:5432 -e POSTGRES_DB=covid_test -e POSTGRES_USER=aldebaran -e POSTGRES_PASSWORD=password --rm timescale/timescaledb:latest-pg11

db-down:
	@docker stop aldebaran_test

db-init:
	@sleep 5 && psql -U aldebaran --port 9432 -h 0.0.0.0 covid_test -a -f ./covid.sql
	@psql -U aldebaran --port 9432 -h 0.0.0.0 covid_test -c "\copy corona FROM ./tests/testdb.csv CSV;"

db-setup: db-down db-up db-init

isort:
	@$(ACTIVATE_VENV) isort . --recursive -tc

isort-check:
	@$(ACTIVATE_VENV) isort . --recursive --check-only -tc -q

nuke-venv:
	@pipenv --rm;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 1 ]; then\
		echo Skipping virtualenv removal;\
	fi

start-aldebaran:
	@export PGPASSWORD=$$DB_PASSWORD && psql -U $$DB_USER --port $$DB_PORT -h $$DB_HOST $$DB_NAME -a -f ./covid.sql
	@uvicorn aldebaran.ignition:app --host 0.0.0.0 --port 8080 --log-config logconfig.ini

start-aldebaran-local:
	@export PGPASSWORD=$$DB_PASSWORD && psql -U $$DB_USER --port $$DB_PORT -h $$DB_HOST $$DB_NAME -a -f ./covid.sql
	@uvicorn aldebaran.ignition:app --host 0.0.0.0 --port 8080

test: db-setup
	@$(ACTIVATE_VENV) pytest -s

test-circle: db-init
	@$(ACTIVATE_VENV) pytest -s
