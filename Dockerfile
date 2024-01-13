FROM python:3.11

EXPOSE 8002

ENV PYTHONUNBUFFERED=1

WORKDIR /habitual_life

COPY pyproject.toml poetry.lock /habitual_life/

RUN pip3 install poetry && poetry install --no-cache

COPY . .
