# Backend

## Local test run with uvicorn
```bash
uvicorn app.main:app --reload
```

## Docker develop and test
```bash
docker build -t backend -f projects/backend/Dockerfile .
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


## Export OpenAPI spec. and generate API for frontend:
This is only done when developing. Could create a shell script for this, but no need.

1. Create an image for the generator.
2. Export the OpenAPI yaml spec.
3. Generate Frontend API stubs with axios and typescript.

Run from project root /full-stack-ml
```bash

docker build -t openapi -f projects/backend/Dockerfile .

docker run --rm  \
  -v ${PWD}/projects/backend:/code  \
  --user $(id -u):$(id -g)  \
  --entrypoint /bin/bash  \
  --env-file .env  \
  openapi -c "python scripts/export_openapi.py"

docker run --rm \
    -v ${PWD}:/local \
    --user $(id -u):$(id -g) \
    openapitools/openapi-generator-cli:v5.3.0 generate \
    -i /local/projects/backend/openapi.yaml \
    -g typescript-axios \
    -o /local/projects/frontend/src/api \
    --global-property skipFormModel=false
```