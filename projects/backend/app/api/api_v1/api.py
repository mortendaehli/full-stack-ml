from app.api.api_v1.routers import accounts, auth, predict, roles, user_roles, users
from app.config import config
from fastapi import APIRouter

api_router = APIRouter(prefix=config.API_V1_STR)

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(user_roles.router, prefix="/user-roles", tags=["User Roles"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(predict.router, prefix="/predict", tags=["Machine Learning"])
