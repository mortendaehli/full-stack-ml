# Sphinx Docs
This is a sphinx documentation demo for this project

## Local development and build
Navigate to /docs and create a new Poetry environment: 

```bash
poetry shell
poetry install
```

## Install python requirements
Install the required python modules

## Local development using Docker
```bash
docker build --target build -t docs-dev .
```

## Local deploy using Docker and nginx
Alternatively you can build and run it as a nginx web service in docker:
```bash
docker build -t docs-nginx .
docker run -dp 8080:8080 docs-nginx
```