from app import entities, schemas
from app.core import auth
from app.db import crud
from app.db.session import get_db
from app.utils.role import Role
from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=schemas.UserRole)
def assign_user_role_to_existing_user(
    *,
    db: Session = Depends(get_db),
    user_role_in: schemas.UserRoleCreate,
    current_user: entities.User = Depends(auth.get_current_active_user),
) -> entities.UserRole:
    """Assign a role to an existing user"""
    user_role = crud.user_role.get_by_user_id(db, user_id=user_role_in.user_id)
    if user_role:
        raise HTTPException(status_code=409, detail="User has already been assigned to a role.")

    return crud.user_role.create(db, obj_in=user_role_in)


@router.put("/{user_id}", response_model=schemas.UserRole)
def update_user_role(
    *,
    db: Session = Depends(get_db),
    user_id: UUID4,
    user_role_in: schemas.UserRoleUpdate,
    current_user: entities.User = Security(
        auth.get_current_active_user,
        scopes=[Role.ADMIN["name"]],
    ),
) -> entities.UserRole:
    """Update an existing user role."""
    user_role = crud.user_role.get_by_user_id(db, user_id=user_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="There are no roles assigned to this user.")

    return crud.user_role.update(db, db_obj=user_role, obj_in=user_role_in)
