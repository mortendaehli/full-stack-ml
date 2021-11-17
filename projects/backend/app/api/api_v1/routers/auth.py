from datetime import timedelta
from typing import Any

from app import schemas
from app.config import config
from app.core import security
from app.db import crud
from app.db.session import get_db
from app.utils.role import Role
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def oauth2_password_grant_to_get_bearer_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth 2.0 Password Grant to fetch a Bearer token for the user.

    Requires password and username.

    Fixme: This should not be used for any production system!
        Ref: \n
        https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow \n
        https://oauth.net/2/grant-types/password/
    """
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.JWT_EXPIRES)
    if not user.user_role:
        role = Role.USER
    else:
        role = user.user_role.role.name
    token_payload = {
        "id": str(user.id),
        "role": role,
        "account_id": str(user.account_id),
    }
    return {
        "access_token": security.create_access_token(token_payload, expires_delta=access_token_expires),
        "token_type": "bearer",
    }
