from uuid import uuid4

from app.entities.base import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID


class Role(Base):
    """Database entity: role"""

    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String(100), index=True)
    description = Column(Text)
