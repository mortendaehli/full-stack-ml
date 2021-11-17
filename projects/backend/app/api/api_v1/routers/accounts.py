from typing import List

from app import entities, schemas
from app.core import auth
from app.db import crud
from app.db.session import get_db
from app.utils.role import Role
from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.Account])
def get_all_accounts(
    *,
    db: Session = Depends(get_db),
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> List[entities.Account]:
    """List all account if Role == Role.ADMIN"""
    return crud.account.get_multi(db, skip=0, limit=100)


@router.get("/me", response_model=schemas.Account)
def get_account_current_user(
    *,
    db: Session = Depends(get_db),
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.Account:
    """Get current active user account"""
    return crud.account.get(db, id=current_user.account_id)


@router.post("/", response_model=schemas.Account)
def create_account_for_current_user(
    *,
    db: Session = Depends(get_db),
    account_in: schemas.AccountCreate,
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.Account:
    """Create account for current user."""
    account = crud.account.get_by_name(db, name=account_in.name)
    if account:
        raise HTTPException(status_code=409, detail="Account already exists.")

    return crud.account.create(db, obj_in=account_in)


@router.put("/{account_id}", response_model=schemas.Account)
def update_account(
    *,
    db: Session = Depends(get_db),
    account_id: UUID4,
    account_in: schemas.AccountUpdate,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> entities.Account:
    """Update an account. Requires admin role"""
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    return crud.account.update(db, db_obj=account, obj_in=account_in)


@router.post("/{account_id}/users", response_model=schemas.User)
def add_account_to_user(
    *,
    db: Session = Depends(get_db),
    account_id: UUID4,
    user_id: UUID4,
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.User:
    """Add account to user"""
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    user_in = schemas.UserUpdate(account_id=account_id)
    return crud.user.update(db, db_obj=user, obj_in=user_in)


@router.get("/{account_id}/users", response_model=List[schemas.User])
def get_users_for_account(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    account_id: UUID4,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> List[entities.User]:
    """
    Retrieve users for an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    return crud.user.get_by_account_id(db, account_id=account_id, skip=skip, limit=limit)


@router.get("/users/me", response_model=List[schemas.Account])
def get_current_user_accounts(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> List[entities.User]:
    """
    Retrieve users for own account.
    """
    account = crud.account.get(db, id=current_user.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    return crud.user.get_by_account_id(db, account_id=account.id, skip=skip, limit=limit)
