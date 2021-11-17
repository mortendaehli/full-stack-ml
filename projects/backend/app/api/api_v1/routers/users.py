from typing import List

from app import entities, schemas
from app.config import config
from app.core import auth
from app.db import crud
from app.db.session import get_db
from app.utils.role import Role
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> List[entities.User]:
    """Retrieve all user. Requires admin role."""
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User)
def create_new_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> entities.User:
    """Create new user. Requires admin role."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=409, detail="The user already exists.")

    return crud.user.create(db, obj_in=user_in)


@router.put("/me", response_model=schemas.User)
def update_current_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserUpdate,
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.User:
    """Update current user"""
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if user_in.phone_number is not None:
        user_in.phone_number = user_in.phone_number
    if user_in.full_name is not None:
        user_in.full_name = user_in.full_name
    if user_in.email is not None:
        user_in.email = user_in.email

    return crud.user.update(db, db_obj=current_user, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def get_current_user(
    *,
    db: Session = Depends(get_db),
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.User:
    """Get current user."""
    return schemas.User.from_orm(current_user)


@router.post("/open", response_model=schemas.User)
def register_new_user(
    *,
    db: Session = Depends(get_db),
    account_in: schemas.UserRegister,
) -> entities.User:
    """
    Create new user without the need to be logged in.

    This is closed for now.
    """
    if not config.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=account_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=account_in.password,
        email=account_in.email,
        full_name=account_in.full_name,
        phone_number=account_in.phone_number,
    )

    return crud.user.create(db, obj_in=user_in)


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(
    *,
    db: Session = Depends(get_db),
    user_id: UUID4,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> entities.User:
    """Get a user by id if Role == Role.ADMIN"""
    return crud.user.get(db, id=user_id)


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: UUID4,
    user_in: schemas.UserUpdate,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> entities.User:
    """Update a user given Role == Role.ADMIN"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")

    return crud.user.update(db, db_obj=user, obj_in=user_in)
