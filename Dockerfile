FROM python:3.10-alpine

SHELL [ "/bin/ash", "-c"]

EXPOSE 8000

RUN apk update && apk upgrade && \
    apk add --no-cache bash curl && \
    apk add --no-cache libc-dev libffi-dev openssl-dev gcc && \
    apk add --no-cache build-base mariadb-dev && \
    apk add --no-cache docker-compose

RUN pip install --upgrade pip

RUN adduser -D itsoda && chmod 777 /opt /run

WORKDIR /itsoda

RUN mkdir /itsoda/static && mkdir /itsoda/media && chown -R itsoda:itsoda /itsoda && chmod 777 /itsoda

COPY --chown=itsoda:itsoda . .

COPY pyproject.toml poetry.lock /itsoda/

RUN curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    | tar -C /usr/local/bin -xzvf - \
    && rm -f dockerize-linux-amd64-v0.6.1.tar.gz

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi