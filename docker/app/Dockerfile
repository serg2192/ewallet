# Python version can be specified in compose file etc.
ARG PY_VERSION
FROM python:${PY_VERSION:-3.8.2}-alpine as prod
LABEL maintainer="Sergey Ondrin(ondrinsa@rambler.ru)"

ENV APP_DIR '/opt/app'

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        libffi-dev \
        musl-dev \
    && apk add --no-cache \
        postgresql-libs \
        postgresql-dev

WORKDIR $APP_DIR

COPY ./requirements/devel.txt $APP_DIR
RUN pip install --no-cache --upgrade pip \
    && pip install --no-cache -U -r $APP_DIR/devel.txt --no-cache
RUN apk --purge del --no-cache .build-deps