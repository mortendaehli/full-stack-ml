from io import StringIO

import uvicorn
import yaml
from app.api.api_v1.api import api_router_v1
from app.config import config
from app.core.celery_app import celery_app
from app.db.session import get_db
from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI(title=config.PROJECT_NAME, openapi_url=f"{config.API_V1_STR}/openapi.json", root_path="/")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = get_db()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/", status_code=307, response_class=Response)
async def docs_redirect():
    """Redirect base URL to docs."""
    return RedirectResponse(url="/docs")


@app.get("/api/v1/health")
async def health_check():
    return {"message": "success"}


@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}


@app.get("/api/v1/openapi.yaml", include_in_schema=False)
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type="text/yaml")


# Routers
app.include_router(api_router_v1)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
