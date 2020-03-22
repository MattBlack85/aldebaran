# aldebaran
covid-19 pandemic JSON API

## hard dependencies
The only hard dependencies required are `pipenv` and `direnv`(https://direnv.net/)

NOTE: if you are willing to use pip or load ENV vars by hand you won't need any of those.

## Setup the project
run `make bootstrap` to create the virtual environment and install the dependencies
create a new file .envrc from .envrc.EXAMPLE and use the following values:
```
export DB_PORT=9432
export DB_NAME=covid_test
export DB_PASSWORD=password
export DB_USER=aldebaran
export DB_HOST=localhost
export DEBUG=true
export PGPASSWORD=password
```

## Run the API
make sure the DB is up, `make db-up`

run `make start-aldebaran-local` and starlette should start the service
