FROM python:3.10.13

SHELL [ "/bin/bash", "-c"]

EXPOSE 8000

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash itsoda && chmod 777 /opt /run

WORKDIR /itsoda

RUN mkdir /itsoda/static && mkdir /itsoda/media && chown -R itsoda:itsoda /itsoda && chmod 777 /itsoda

COPY media/user_images/no-profile.png /itsoda/media/user_images/no-profile.png

COPY --chown=itsoda:itsoda . .

COPY pyproject.toml poetry.lock /itsoda/

RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi
