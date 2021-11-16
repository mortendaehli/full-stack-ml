# syntax=docker/dockerfile:1
FROM python:3.9 as dev

ARG USER_ID=1000
ARG USER_GROUP=1000

ARG INSTALL_DEV=false

ENV PYTHONUNBUFFERED=1

RUN addgroup --gid $USER_GROUP newuser \
    && adduser --uid $USER_ID --gid $USER_GROUP --system newuser



RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install --no-install-recommends -y postgresql-client && \
  rm -rf /var/lib/apt/lists/*

RUN pip install poetry && poetry config virtualenvs.create false

WORKDIR /code


COPY --chown=newuser:newuser projects/backend/pyproject.toml projects/backend/poetry.lock ./

RUN bash -c "if [ INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

USER $USER_ID
ENV PYTHONPATH=/code

FROM dev as build

COPY --chown=newuser:newuser projects/backend/ ./

ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["api"]
