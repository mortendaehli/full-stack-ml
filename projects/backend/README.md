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
If poetry update is too slow, try run it in Alpine linux with a volume mount.

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