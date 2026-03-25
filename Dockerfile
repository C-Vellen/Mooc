FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=mooc.mooc.settings

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --only main

COPY . .

CMD ["gunicorn", "mooc.mooc.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]