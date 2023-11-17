FROM python:3.10

EXPOSE 8000

WORKDIR /cityheroes

COPY pyproject.toml poetry.lock /cityheroes/

# Установка зависимостей poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . /cityheroes/

CMD ["poetry", "run", "python", "manage.py", "runserver", "127.0.0.1:8000"]