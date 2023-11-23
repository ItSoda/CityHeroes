FROM python:3.10-slim-bullseye as builder

WORKDIR /usr

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create true && poetry install --only main

FROM python:3.10-slim-bullseye as compiler

EXPOSE 8000

WORKDIR /usr/cityheroes

COPY --from=builder /usr /usr
COPY . .

ENV PATH="/usr/cityheroes/.venv/bin:$PATH"
ENV PYTHONPATH="/usr/cityheroes:$PYTHONPATH"

CMD ["sh", "-c", "gunicorn CityHeroes.wsgi:application -b :8000"]