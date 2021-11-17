# Backend

The backend requires environmental variables, and it is recommended to develop using Docker Compose.

Note that this README assumes you are in the repository root full-stack-ml/

## Docker develop and test
```bash
docker-compose up -d
```

Note: this will run alembic migrations before starting.

# Developer notes:

## Make new Alembic db revision for migration.
Initial Alembic db init
```bash
docker-compose run backend alembic revision --autogenerate -m "init"
```

Further changes can be specified manually using:
```bash
docker-compose run backend alembic revision -m "<revision name>"
```
Or automatically:
```bash
docker-compose run backend alembic revision --autogenerate -m "<revision name>"
```

See [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html) for additional info.

## Export OpenAPI spec. and generate API for frontend:
This is only done when developing when you make changes to the backend API.

This will generate TypeScript Axios API stubs for the frontend.

1. Export the OpenAPI yaml spec.
2. Generate Frontend API stubs with axios and typescript.

```bash
docker-compose run backend python scripts/export_openapi.py
echo "servers:" >> projects/backend/openapi.yaml
echo "  - url: /api/v1" >> projects/backend/openapi.yaml

docker run --rm \
    -v ${PWD}:/local \
    --user $(id -u):$(id -g) \
    openapitools/openapi-generator-cli:v5.3.0 generate \
    -i /local/projects/backend/openapi.yaml \
    -g typescript-axios \
    -o /local/projects/frontend/src/api
```

## Note on slow Poetry update:
If poetry update is slow on MacOS. If you have the same issue then try using Alpine linux Docker with a volume mount.

```bash
docker run -it --mount type=bind,source="$(pwd)",target=/code python:3.9 bash
```
```bash
apt-get update
cd code
pip install poetry
poetry update
exit()
```