FROM python:3.8-alpine

RUN apk update
RUN apk add libffi-dev make g++ linux-headers postgresql-dev postgresql
RUN mkdir /app

WORKDIR /app

RUN pip install pipenv==2018.11.26

COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN pipenv install --system

COPY ./aldebaran /app/aldebaran
COPY ./Makefile /app
COPY ./covid.sql /app
COPY ./logconfig.ini /app

# Entrypoint for docker
ENTRYPOINT ["make"]
CMD ["start-aldebaran"]
