import logging

from app import schemas
from app.config import config
from app.db import crud
from app.db.session import SessionLocal
from app.utils.role import Role
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:

    # Admin Account
    account = crud.account.get_by_name(db, name=config.FIRST_SUPERUSER)
    if not account:
        account_in = schemas.AccountCreate(
            name=config.FIRST_SUPERUSER,
            description="Admin account",
        )
        crud.account.create(db, obj_in=account_in)

    # Create Admin
    user = crud.user.get_by_email(db, email=config.FIRST_SUPERUSER)
    if not user:
        account = crud.account.get_by_name(db, name=config.FIRST_SUPERUSER)
        user_in = schemas.UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            full_name="Some Admin",
            account_id=account.id,
        )
        user = crud.user.create(db, obj_in=user_in)

    # Create Role If They Don't Exist
    user_role = crud.role.get_by_name(db, name=Role.USER["name"])
    if not user_role:
        user_role_in = schemas.RoleCreate(name=Role.USER["name"], description=Role.USER["description"])
        crud.role.create(db, obj_in=user_role_in)

    admin_role = crud.role.get_by_name(db, name=Role.ADMIN["name"])
    if not admin_role:
        admin_role_in = schemas.RoleCreate(name=Role.ADMIN["name"], description=Role.ADMIN["description"])
        crud.role.create(db, obj_in=admin_role_in)

    # Assign admin role to user
    user_role = crud.user_role.get_by_user_id(db, user_id=user.id)
    if not user_role:
        role = crud.role.get_by_name(db, name=Role.ADMIN["name"])
        user_role_in = schemas.UserRoleCreate(user_id=user.id, role_id=role.id)
        crud.user_role.create(db, obj_in=user_role_in)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
