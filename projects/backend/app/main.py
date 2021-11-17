import uvicorn
from app.api.api_v1.api import api_router
from app.config import config
from app.core.celery_app import celery_app
from app.db.session import get_db
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

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


@app.get("/api/v1/health", tags=["Generic"])
async def health_check():
    """Check API backend health."""
    return {"message": "success"}


@app.get("/api/v1/task", tags=["Generic"])
async def example_task():
    """Dummy task to test the Celery Queue."""
    celery_app.send_task("app.worker.test_celery", args=["Hello World"])

    return {"message": "success"}


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
