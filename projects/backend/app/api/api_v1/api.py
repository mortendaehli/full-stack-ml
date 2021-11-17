from app.api.api_v1.routers import accounts, auth, roles, user_roles, users
from app.config import config
from fastapi import APIRouter

api_router = APIRouter(prefix=config.API_V1_STR)

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(user_roles.router, prefix="/user-roles", tags=["user-roles"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
