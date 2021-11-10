FROM python:3.9 as build

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install --no-install-recommends -y make && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir poetry

WORKDIR /docs

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install

COPY docs/ ./

RUN make html

# Bitnami/nginx ensures that we do not run the container as root.
FROM bitnami/nginx:1.21 as deploy
COPY --from=build /docs/_build/html /usr/share/nginx/html
COPY nginx.conf /opt/bitnami/nginx/conf/server_blocks/nginx.conf
