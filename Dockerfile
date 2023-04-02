FROM python:3.11-alpine3.17
LABEL maintainer="serhiikarnaukh"

ENV PYTHONUNBUFFERED 1

COPY ./req.txt /req.txt
COPY . /app


WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps\
    build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /req.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol


ENV PATH="/py/bin:$PATH"

USER app
