import datetime
from uuid import uuid4

from app.entities.base import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    """Database entity: user"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    full_name = Column(String(255), index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(13), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    account_id = Column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=True)

    user_role = relationship("UserRole", back_populates="users", uselist=False)
    account = relationship("Account", back_populates="users")
