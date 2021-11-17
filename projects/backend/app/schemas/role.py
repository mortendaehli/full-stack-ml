from typing import Optional

from pydantic import UUID4, BaseModel


class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: UUID4

    class Config:
        """
        ORM-mode enables models to be created from arbitrary class instances such as nitiating a Pydantic model from a
        SQLAlchemy object.
        """

        orm_mode = True


class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass
