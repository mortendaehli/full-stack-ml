from app.api.api_v1.routers import auth, users
from app.config import config
from app.core.auth import get_current_active_user
from fastapi import APIRouter, Depends

api_router_v1 = APIRouter()

api_router_v1.include_router(auth.auth_router, prefix=config.API_V1_STR, tags=["auth"])
api_router_v1.include_router(
    users.users_router, prefix=config.API_V1_STR, tags=["users"], dependencies=[Depends(get_current_active_user)]
)
