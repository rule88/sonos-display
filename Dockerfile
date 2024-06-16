FROM python:3.12-slim-bookworm

RUN apt-get update
RUN apt-get install -y --no-install-recommends curl
RUN apt-get clean

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY ./pyproject.toml ./poetry.lock* ./
COPY ./app ./

RUN poetry install --no-root --no-dev --no-interaction

ENV TZ=Europe/Amsterdam
ENV PYTHONUNBUFFERED=1

CMD ["python","./index.py"]
