from typing import List

from app import entities, schemas
from app.db import crud
from app.db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.Role])
def get_all_user_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[entities.Role]:
    """Get all user roles"""
    return crud.role.get_multi(db, skip=skip, limit=limit)
