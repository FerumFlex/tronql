FROM python:3.11-slim AS compile-image

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends build-essential gcc -y \
    && pip install --upgrade pip && pip install poetry==1.3.1 \
    && poetry export --without-hashes -f requirements.txt --with dev | pip install -r /dev/stdin

FROM python:3.11-slim AS build-image
COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
RUN  \
    groupadd app && useradd --home-dir=/app --gid=app app \
    && chown -R app:app /app
USER app
COPY --chown=app:app . /app/
