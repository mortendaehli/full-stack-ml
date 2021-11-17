from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class AccountBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    current_subscription_ends: Optional[datetime]
    plan_id: Optional[UUID4]
    is_active: Optional[bool] = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        ORM-mode enables models to be created from arbitrary class instances such as nitiating a Pydantic model from a
        SQLAlchemy object.
        """

        orm_mode = True


class Account(AccountInDBBase):
    pass


class AccountInDB(AccountInDBBase):
    pass
