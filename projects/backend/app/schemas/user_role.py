from typing import Optional

from app.schemas.role import Role
from pydantic import UUID4, BaseModel


class UserRoleBase(BaseModel):
    user_id: Optional[UUID4]
    role_id: Optional[UUID4]


class UserRoleCreate(UserRoleBase):
    user_id: UUID4
    role_id: UUID4


class UserRoleUpdate(BaseModel):
    role_id: UUID4


class UserRoleInDBBase(UserRoleBase):
    role: Role

    class Config:
        """
        ORM-mode enables models to be created from arbitrary class instances such as nitiating a Pydantic model from a
        SQLAlchemy object.
        """

        orm_mode = True


class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass
