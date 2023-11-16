FROM python:3

EXPOSE 8001

WORKDIR /cityheroes

COPY pyproject.toml poetry.lock /cityheroes/

# Установка зависимостей poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . /cityheroes/

# RUN poetry run python manage.py makemigrations

# RUN poetry run python manage.py migrate

CMD ["poetry", "run", "python", "manage.py", "runserver"]