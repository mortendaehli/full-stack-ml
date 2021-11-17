from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.core.security import get_password_hash, verify_password
from app.entities import Account, Role, User, UserRole
from app.entities.base import Base
from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic.types import UUID4
from sqlalchemy.orm import Session

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Basic CRUD and listing operations. To be extended for other needs below:

        :param model: The SQLAlchemy model Base
        :type model: Type[ModelType]
        """
        self.model = model

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Read multiple records from the database for a given model/table"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, *, id: UUID4) -> Optional[ModelType]:
        """Todo: Consider if the id name makes for a problem with the Python namespace...?"""
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Account]:
        return db.query(self.model).filter(Account.name == name).first()


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(self.model).filter(Role.name == name).first()


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            account_id=obj_in.account_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def get_by_account_id(
        self,
        db: Session,
        *,
        account_id: UUID4,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        return db.query(self.model).filter(User.account_id == account_id).offset(skip).limit(limit).all()


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: UUID4) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.user_id == user_id).first()


account = CRUDAccount(Account)
role = CRUDRole(Role)
user = CRUDUser(User)
user_role = CRUDUserRole(UserRole)
